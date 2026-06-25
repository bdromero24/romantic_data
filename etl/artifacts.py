"""Persistence helpers for ETL staging artifacts."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from logger.logger import log_critical_error


SUPPORTED_STAGES = frozenset({"extracted", "transformed"})
SUPPORTED_FILE_FORMATS = frozenset({"parquet", "csv"})
STAGING_ROOT = Path("data") / "staging"


def ensure_directory(path: str | Path) -> Path:
    """Create a directory when missing and return it as a Path."""
    try:
        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    except Exception as error:
        _log_artifact_error(type(error).__name__, error, "ensure_directory")
        raise


def build_artifact_path(
    stage: str,
    source: str,
    file_format: str = "parquet",
) -> Path:
    """Build a timestamped artifact path under data/staging."""
    normalized_stage = _validate_stage(stage)
    normalized_format = _validate_file_format(file_format)
    source_name = _sanitize_path_token(source, "source")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = (
        f"{normalized_stage}_{source_name}_{timestamp}.{normalized_format}"
    )

    return STAGING_ROOT / normalized_stage / filename


def save_records(records: list[dict[str, Any]], output_path: str | Path) -> Path:
    """Save ETL records to a supported artifact file."""
    try:
        _validate_records(records)
        path = Path(output_path)
        file_format = _validate_file_format(path.suffix.lstrip("."))
        ensure_directory(path.parent)

        dataframe = pd.DataFrame(records)
        if file_format == "parquet":
            _require_pyarrow()
            dataframe.to_parquet(path, index=False, engine="pyarrow")
            return path

        dataframe.to_csv(path, index=False)
        return path
    except Exception as error:
        _log_artifact_error(type(error).__name__, error, "save_records")
        raise


def load_records(input_path: str | Path) -> list[dict[str, Any]]:
    """Load ETL records from a supported artifact file."""
    try:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Artifact file does not exist: {path}")

        file_format = _validate_file_format(path.suffix.lstrip("."))
        if file_format == "parquet":
            _require_pyarrow()
            dataframe = pd.read_parquet(path, engine="pyarrow")
        else:
            dataframe = pd.read_csv(path)

        return dataframe.to_dict(orient="records")
    except Exception as error:
        _log_artifact_error(type(error).__name__, error, "load_records")
        raise


def save_stage_output(
    records: list[dict[str, Any]],
    stage: str,
    source: str,
    file_format: str = "parquet",
) -> Path:
    """Save ETL stage records to the conventional staging location."""
    output_path = build_artifact_path(
        stage=stage,
        source=source,
        file_format=file_format,
    )
    return save_records(records, output_path)


def _validate_stage(stage: str) -> str:
    normalized_stage = stage.strip().lower()
    if normalized_stage not in SUPPORTED_STAGES:
        supported = ", ".join(sorted(SUPPORTED_STAGES))
        raise ValueError(f"Unsupported ETL artifact stage: {stage}. Use: {supported}.")

    return normalized_stage


def _validate_file_format(file_format: str) -> str:
    normalized_format = file_format.strip().lower()
    if normalized_format not in SUPPORTED_FILE_FORMATS:
        supported = ", ".join(sorted(SUPPORTED_FILE_FORMATS))
        raise ValueError(
            f"Unsupported ETL artifact file format: {file_format}. "
            f"Use: {supported}."
        )

    return normalized_format


def _validate_records(records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError("Cannot save an empty ETL artifact record list.")

    if not all(isinstance(record, dict) for record in records):
        raise TypeError("ETL artifact records must be dictionaries.")


def _sanitize_path_token(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Artifact {field_name} must be a non-empty string.")

    token = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower())
    token = token.strip("_")
    if not token:
        raise ValueError(f"Artifact {field_name} must include letters or numbers.")

    return token


def _require_pyarrow() -> None:
    try:
        import pyarrow  # noqa: F401
    except ImportError as error:
        raise ImportError(
            "Parquet artifact support requires pyarrow. "
            "Install project dependencies with: "
            ".\\venv\\Scripts\\python.exe -m pip install -r requirements.txt"
        ) from error


def _log_artifact_error(
    error_type: str,
    error: Exception,
    function_name: str,
) -> None:
    log_critical_error(
        error_type=error_type,
        error_message=str(error),
        module_name=__name__,
        function_name=function_name,
    )
