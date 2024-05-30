import csv
import json
import math
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Union

import boto3
import click
import deepdiff
import pandas as pd
import pyarrow.fs
import pyarrow.orc
import s3fs
from click.core import Context as ClickContext
from fastparquet import ParquetFile
from gable.client import CheckDataAssetDetailedResponseUnion, GableClient
from gable.helpers.data_asset_s3.logger import log_trace
from gable.helpers.data_asset_s3.native_s3_converter import NativeS3Converter
from gable.helpers.data_asset_s3.path_pattern_manager import (
    DATE_PLACEHOLDER_TO_REGEX,
    SUPPORTED_FILE_TYPES,
)
from gable.helpers.data_asset_s3.pattern_discovery import (
    discover_patterns_from_s3_bucket,
)
from gable.helpers.data_asset_s3.schema_profiler import get_data_profile_for_data_asset
from gable.helpers.emoji import EMOJI
from gable.openapi import (
    CheckComplianceDataAssetsS3Request,
    CheckDataAssetCommentMarkdownResponse,
    DataProfileFieldsMapping,
    ErrorResponse,
    IngestDataAssetResponse,
    RegisterDataAssetS3Request,
    ResponseType,
    S3Asset,
)
from loguru import logger

DEFAULT_NUM_ROWS_TO_SAMPLE = 1000
CHUNK_SIZE = 100
sniffer = csv.Sniffer()


@dataclass
class S3DetectionResult:
    schema: dict
    data_profile_map: Optional[DataProfileFieldsMapping] = None


def get_dfs_from_s3_files(
    s3_urls: list[str],
    row_sample_count: Optional[int] = None,
    s3_opts: Optional[dict] = None,
) -> list[tuple[pd.DataFrame, bool]]:
    """
    Read data from given S3 file urls (only CSV, JSON, and parquet currently supported) and return pandas DataFrames.
    Args:
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
        s3_opts (dict): S3 storage options. - only needed for tests using moto mocking
    Returns:
        list[tuple[pd.DataFrame, bool]]: List tuple of pandas DataFrames and a boolean indicating if the DataFrame has a predefined schema.
    """
    result = []
    num_rows_to_sample = row_sample_count or DEFAULT_NUM_ROWS_TO_SAMPLE
    for url in s3_urls:
        if df := read_s3_file(url, num_rows_to_sample, s3_opts):
            result.append(df)
    return result


def read_s3_file(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> Optional[tuple[pd.DataFrame, bool]]:
    """
    Returns a tuple of pandas DataFrame and a boolean indicating if the DataFrame has a predefined schema.
    """
    try:
        if url.endswith(SUPPORTED_FILE_TYPES.CSV.value):
            logger.info(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            return get_csv_df(url, num_rows_to_sample, s3_opts), False
        elif url.endswith(SUPPORTED_FILE_TYPES.JSON.value):
            logger.info(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            df = pd.concat(
                pd.read_json(
                    url,
                    lines=True,
                    chunksize=CHUNK_SIZE,
                    nrows=num_rows_to_sample,
                    storage_options=s3_opts,
                ),
                ignore_index=True,
            )
            return flatten_json(df), False
        elif url.endswith(SUPPORTED_FILE_TYPES.PARQUET.value):
            logger.info(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            return get_parquet_df(url, num_rows_to_sample, s3_opts), True
        elif url.endswith(SUPPORTED_FILE_TYPES.ORC.value) or url.endswith(
            SUPPORTED_FILE_TYPES.ORC_SNAPPY.value
        ):
            logger.info(f"Reading {num_rows_to_sample} rows from S3 file: {url}")
            return get_orc_df(url, num_rows_to_sample, s3_opts), True
        else:
            logger.debug(f"Unsupported file format: {url}")
            return None
    except Exception as e:
        # Swallowing exceptions to avoid failing processing other files
        logger.opt(exception=e).error(f"Error reading file {url}: {e}")
        return None


def get_orc_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read ORC file from S3 and return a pandas DataFrame.
    """
    endpoint_override = (
        s3_opts.get("client_kwargs", {}).get("endpoint_url") if s3_opts else None
    )
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        raise click.ClickException("No AWS credentials found")
    filesystem = pyarrow.fs.S3FileSystem(
        endpoint_override=endpoint_override,
        access_key=credentials.access_key,
        secret_key=credentials.secret_key,
        session_token=credentials.token,
        region=boto3.Session().region_name,
    )
    bucket_and_path = strip_s3_bucket_prefix(url)
    with filesystem.open_input_file(bucket_and_path) as f:
        orcfile = pyarrow.orc.ORCFile(f)
        rows_per_stripe = orcfile.nrows / orcfile.nstripes
        stripes_to_sample = min(
            math.ceil(num_rows_to_sample / rows_per_stripe), orcfile.nstripes
        )
        logger.debug(
            f"Reading {stripes_to_sample} stripes from {url} (total rows: {orcfile.nrows}, total stripes: {orcfile.nstripes})"
        )
        return pyarrow.Table.from_batches(
            [orcfile.read_stripe(i) for i in range(stripes_to_sample)]
        ).to_pandas()


def get_parquet_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read Parquet file from S3 and return an empty pandas DataFrame with the schema.
    """
    parquet_file = ParquetFile(url, fs=s3fs.S3FileSystem(**(s3_opts or {})))
    # read default sample size rows in order to compute profile. Only 1 row is needed to compute schema
    return parquet_file.head(num_rows_to_sample)


def get_csv_df(
    url: str, num_rows_to_sample: int, s3_opts: Optional[dict] = None
) -> pd.DataFrame:
    """
    Read CSV file from S3 and return a pandas DataFrame. Special handling for CSV files with and without headers.
    """
    # Sample a small part of the CSV file to determine if there is a header
    sample_csv = pd.read_csv(url, nrows=10, storage_options=s3_opts).to_csv(index=False)
    has_header = sniffer.has_header(sample_csv)

    if has_header:
        df = pd.concat(
            pd.read_csv(
                url,
                chunksize=CHUNK_SIZE,
                nrows=num_rows_to_sample,
                storage_options=s3_opts,
            ),
            ignore_index=True,
        )
    else:
        df = pd.concat(
            pd.read_csv(
                url,
                header=None,
                chunksize=CHUNK_SIZE,
                nrows=num_rows_to_sample,
                storage_options=s3_opts,
            ),
            ignore_index=True,
        )
    return df


def flatten_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens any nested JSON data to a single column
    {"customerDetails": {"technicalContact": {"email": "...."}}}" => customerDetails.technicalContact.email
    """
    normalized_df = pd.json_normalize(df.to_dict(orient="records"))
    return drop_null_parents(normalized_df)


def drop_null_parents(df: pd.DataFrame) -> pd.DataFrame:
    # Identify null columns
    null_columns = {col for col in df.columns if df[col].isnull().all()}  # type: ignore

    # Identify nested columns
    parent_columns = {col for col in df.columns if "." in col}

    # For null parent columns, drop them if they will be represented by the nested columns
    columns_to_drop = [
        null_column
        for null_column in null_columns
        for parent_column in parent_columns
        if null_column != parent_column and null_column in parent_column
    ]
    return df.drop(columns=columns_to_drop)


def get_s3_client():
    return boto3.client("s3")


def append_s3_url_prefix(bucket_name: str, url: str) -> str:
    return "s3://" + bucket_name + "/" + url if not url.startswith("s3://") else url


def strip_s3_bucket_prefix(bucket_name: str) -> str:
    return bucket_name.removeprefix("s3://")


def extract_date_from_pattern(pattern: str) -> Optional[str]:
    """Extract date from pattern using regex."""
    match = re.search(r"\d{4}/\d{2}/\d{2}", pattern)
    return match.group(0) if match else None


def format_deepdiff_output(deepdiff_result):
    """
    Formats the deepdiff output for CLI display.
    """
    formatted_output = []

    # Handle changed values
    values_changed = deepdiff_result.get("values_changed", {})
    if values_changed:
        formatted_output.append("\nChanged values:")
        for key, details in values_changed.items():
            parsed = parse_diff_key(key)
            formatted_output.append(
                f"  - {parsed} Changed from '{details['old_value']}' to '{details['new_value']}'"
            )
    # Handle items added
    items_added = deepdiff_result.get("iterable_item_added", {})
    if items_added:
        formatted_output.append("\nItems added:")
        for key, value in items_added.items():
            formatted_output.append(
                f"  - {key}: Added '{value['name']}' of Type '{value['type']}'"
            )

    # Handle items removed
    items_removed = deepdiff_result.get("iterable_item_removed", {})
    if items_removed:
        formatted_output.append("\nItems removed:")
        for key, value in items_removed.items():
            formatted_output.append(
                f"  - {key}: Removed '{value['name']}' of Type '{value['type']}'"
            )

    return "\n".join(formatted_output)


def extract_date_from_filepath(filepath):
    # This regex assumes the date format in the filepath is something like '2024/04/10'
    match = re.search(DATE_PLACEHOLDER_TO_REGEX["{YYYY}/{MM}/{DD}"], filepath)
    if match:
        return datetime.strptime(match.group(1), "%Y/%m/%d").date()
    return None


def parse_diff_key(key: str) -> str:
    # This regex extracts the index and the attribute being compared
    match = re.search(r"\['fields'\]\[(\d+)\]\['(\w+)'\]", key)
    if match:
        attribute = match.group(2)
        return f"{attribute.capitalize()}"
    return "Unknown field"


def get_schemas_from_files(
    pattern: str, files_urls: list[str], row_sample_count: Optional[int]
) -> list[dict]:
    """Retrieve and convert data from S3 into Recap schemas."""
    dfs = get_dfs_from_s3_files(files_urls, row_sample_count)
    return [
        NativeS3Converter().to_recap(df, has_schema, pattern) for df, has_schema in dfs
    ]


def compare_schemas(
    schema1: list[dict],
    schema2: list[dict],
    pattern: str,
    first_date: Optional[str],
    second_date: Optional[str],
):
    """Compare two sets of schemas and log the differences."""
    for schema_h, schema_t in zip(schema1, schema2):
        diff = deepdiff.DeepDiff(schema_h, schema_t, ignore_order=True)
        if diff:
            formatted_results = format_deepdiff_output(diff)
            logger.info(
                f"Differences detected in {pattern} between {first_date} and {second_date}: \n{formatted_results}"
            )
        else:
            logger.info(
                f"No differences detected in {pattern} between {first_date} and {second_date}"
            )


def detect_s3_data_assets_history(
    bucket_name: str,
    include: list[str],
    row_sample_count: Optional[int] = None,
):
    client = get_s3_client()
    first_pattern = include[0]
    second_pattern = include[1]
    first_date = extract_date_from_pattern(first_pattern)
    second_date = extract_date_from_pattern(second_pattern)
    first_date_files = discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket_name),
        start_date=datetime(1970, 1, 1),
        end_date=None,
        include=[first_pattern],
        ignore_timeframe_bounds=True,
    )
    second_date_files = discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket_name),
        start_date=datetime(1970, 1, 1),
        end_date=None,
        include=[second_pattern],
        ignore_timeframe_bounds=True,
    )
    all_patterns = list(set(first_date_files.keys()) | set(second_date_files.keys()))
    if not all_patterns:
        raise click.ClickException(
            "No data assets found to compare! Use the --debug or --trace flags for more details."
        )
    for pattern in all_patterns:
        # Retrieve schemas for both dates
        schema_historical = get_schemas_from_files(
            pattern,
            [
                append_s3_url_prefix(bucket_name, file_url)
                for _, file_url in first_date_files.get(pattern, [])
            ],
            row_sample_count,
        )
        schema_today = get_schemas_from_files(
            pattern,
            [
                append_s3_url_prefix(bucket_name, file_url)
                for _, file_url in second_date_files.get(pattern, [])
            ],
            row_sample_count,
        )
        compare_schemas(
            schema_historical, schema_today, first_pattern, first_date, second_date
        )


def detect_s3_data_assets(
    bucket_name: str,
    skip_profiling: bool,
    lookback_days: int,
    row_sample_count: Optional[int],
    include: list[str],
) -> dict[str, S3DetectionResult]:
    """
    Detect data assets in S3 bucket.
    Args:
        bucket (str): S3 bucket name.
        lookback_days (int): Lookback days.
        row_sample_count (int): Number of rows to sample per S3 file.
        lookback_days: (int), number of days to look back from the latest day in the list of paths. For example
                if the latest path is 2024/01/02, and lookback_days is 3, then the paths return will have
                2024/01/02, 2024/01/01, 2023/12/31, and 2023/12/30. Default is 1
        skip_profiling (bool): Whether to compute data profiles.
    Returns:
        dict[str, S3DetectionResult]: Mapping of asset pattern to schema/data profiles.
    """
    schemas_and_profiles: dict[str, S3DetectionResult] = {}
    client = get_s3_client()
    patterns_to_urls = discover_patterns_from_s3_bucket(
        client,
        strip_s3_bucket_prefix(bucket_name),
        start_date=datetime.now() - timedelta(days=lookback_days),
        include=include,
        ignore_timeframe_bounds=False,
    )
    with ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda entry: (
                entry[0],
                get_merged_def_from_s3_files(
                    strip_s3_bucket_prefix(bucket_name),
                    entry[0],
                    set([url for _, url in entry[1]]),
                    row_sample_count,
                    skip_profiling,
                ),
            ),
            patterns_to_urls.items(),
        )
        schemas_and_profiles.update(
            {
                pattern: result
                for pattern, result in results
                if result and result.schema.get("fields", None)
            }
        )
    return schemas_and_profiles


def register_s3_data_assets(
    ctx: ClickContext,
    bucket_name: str,
    lookback_days: int,
    row_sample_count: Optional[int],
    include: list[str],
    dry_run: bool = False,
    skip_profiling: bool = False,
):
    pattern_to_schema_and_profiles = detect_s3_data_assets(
        bucket_name, skip_profiling, lookback_days, row_sample_count, include
    )
    if len(pattern_to_schema_and_profiles) == 0:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
        )

    logger.info(
        f"{EMOJI.GREEN_CHECK.value} {len(pattern_to_schema_and_profiles)} S3 data asset(s) found:"
    )

    for pattern, schema_and_profile in pattern_to_schema_and_profiles.items():
        logger.info(
            f"Pattern: {pattern}\nSchema: {json.dumps(schema_and_profile.schema, indent=4)}"
        )

    if dry_run:
        logger.info("Dry run mode. Data asset registration not performed.")
        return (
            IngestDataAssetResponse(message="", registered=[], success=True),
            True,
            200,
        )
    else:
        request = RegisterDataAssetS3Request(
            dry_run=dry_run,
            assets=[
                S3Asset(
                    schema=schema_and_profile.schema,
                    fieldNameToDataProfileMap=schema_and_profile.data_profile_map,
                    bucket=bucket_name,
                    pattern=pattern,
                )
                for pattern, schema_and_profile in pattern_to_schema_and_profiles.items()
            ],
        )
        # click doesn't let us specify the type of ctx.obj.client in the Context:
        client: GableClient = ctx.obj.client
        return client.post_data_asset_register_s3(request)


def check_compliance_s3_data_assets(
    ctx: ClickContext,
    response_type: ResponseType,
    bucket_name: str,
    lookback_days: int,
    include: list[str],
    skip_profiling: bool,
    row_sample_count: Optional[int],
) -> Union[
    ErrorResponse,
    CheckDataAssetCommentMarkdownResponse,
    list[CheckDataAssetDetailedResponseUnion],
]:
    pattern_to_result = detect_s3_data_assets(
        bucket_name, skip_profiling, lookback_days, row_sample_count, include
    )
    if len(pattern_to_result) == 0:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to check compliance! You can use the --debug or --trace flags for more details.",
        )

    request = CheckComplianceDataAssetsS3Request(
        assets=[
            S3Asset(
                schema=result.schema,
                fieldNameToDataProfileMap=result.data_profile_map,
                bucket=bucket_name,
                pattern=pattern,
            )
            for pattern, result in pattern_to_result.items()
        ],
        responseType=response_type,
    )
    client: GableClient = ctx.obj.client
    return client.post_check_compliance_data_assets_s3(request)


def get_merged_def_from_s3_files(
    bucket: str,
    event_name: str,
    s3_urls: set[str],
    row_sample_count: Optional[int] = None,
    skip_profiling: bool = False,
) -> Optional[S3DetectionResult]:
    """
    Get merged definition along with data profile from given S3 file urls (only CSV, JSON, and parquet currently supported).
    Args:
        bucket_name (str): S3 bucket name.
        event_name (str): Event name.
        s3_urls (list[str]): List of S3 URLs.
        row_sample_count (int): Number of rows to sample per S3 file.
    Returns:
        tuple[dict, Optional[DataProfileFieldsMapping]]: Merged definition and data profile if able to be computed.
    """
    urls = [append_s3_url_prefix(bucket, url) for url in s3_urls]
    dfs = get_dfs_from_s3_files(urls, row_sample_count)
    if len(dfs) > 0:
        schema = merge_schemas(
            [
                NativeS3Converter().to_recap(df, has_schema, event_name)
                for df, has_schema in dfs
                if len(df.columns) > 0
            ]
        )
        if skip_profiling:
            logger.debug(f"Skipping data profiling for event name: {event_name}")
            return S3DetectionResult(schema)
        else:
            profiles = get_data_profile_for_data_asset(
                schema, [df for df, _ in dfs], event_name
            )
            return S3DetectionResult(schema, profiles)


def merge_schemas(schemas: list[dict]) -> dict:
    """
    Merge multiple schemas into a single schema.
    Args:
        schemas (list[dict]): List of schemas.
    Returns:
        dict: Merged schema.
    """
    # Dictionary of final fields, will be turned into a struct type at the end
    result_dict: dict[str, dict] = {}
    for schema in schemas:
        if "fields" in schema:
            for field in schema["fields"]:
                field_name = field["name"]
                # If the field is not yet in the result, just add it
                if field_name not in result_dict:
                    result_dict[field_name] = field
                elif field != result_dict[field_name]:
                    # If both types are structs, recursively merge them
                    if (
                        field["type"] == "struct"
                        and result_dict[field_name]["type"] == "struct"
                    ):
                        result_dict[field_name] = {
                            "fields": merge_schemas([result_dict[field_name], field])[
                                "fields"
                            ],
                            "name": field_name,
                            "type": "struct",
                        }
                    else:
                        # Merge the two type into a union, taking into account that one or both of them
                        # may already be unions
                        result_types = (
                            result_dict[field_name]["types"]
                            if result_dict[field_name]["type"] == "union"
                            else [result_dict[field_name]]
                        )
                        field_types = (
                            field["types"] if field["type"] == "union" else [field]
                        )
                        result_dict[field_name] = {
                            "type": "union",
                            "types": get_distinct_dictionaries(
                                remove_names(result_types) + remove_names(field_types)
                            ),
                            "name": field_name,
                        }

    return {"fields": list(result_dict.values()), "type": "struct"}


def get_distinct_dictionaries(dictionaries: list[dict]) -> list[dict]:
    """
    Get distinct dictionaries from a list of dictionaries.
    Args:
        dictionaries (list[dict]): List of dictionaries.
    Returns:
        list[dict]: List of distinct dictionaries.
    """
    # Remove duplicates, use a list instead of a set to avoid
    # errors about unhashable types
    distinct = []
    for d in dictionaries:
        if d not in distinct:
            distinct.append(d)
    # Sort for testing so we have deterministic results
    return sorted(
        distinct,
        key=lambda x: x["type"],
    )


def remove_names(list: list[dict]) -> list[dict]:
    """
    Remove names from a list of dictionaries.
    Args:
        list (dict): List of dictionaries.
    Returns:
        dict: List of dictionaries without names.
    """
    for t in list:
        if "name" in t:
            del t["name"]
    return list
