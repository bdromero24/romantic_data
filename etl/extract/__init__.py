"""Safe extraction utilities for conversation exports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal, TypedDict

import pandas as pd

from logger.logger import log_critical_error


JsonSource = Literal["instagram", "whatsapp", "unsupported"]
JsonData = dict[str, Any] | list[Any]


class JsonSchemaInspection(TypedDict):
    """Minimal schema summary for dynamic JSON inspection."""

    root_type: str
    top_level_keys: list[str]
    record_path: str | None
    record_count: int
    record_keys: list[str]
    detected_source: JsonSource


INSTAGRAM_SCHEMA_KEYS: frozenset[str] = frozenset(
    {"sender_name", "timestamp_ms"}
)
WHATSAPP_SCHEMA_KEYS: frozenset[str] = frozenset(
    {
        "author",
        "date",
        "datetime",
        "from",
        "message",
        "sender",
        "text",
        "timestamp",
    }
)


def load_json_file(file_path: str | Path) -> JsonData:
    """Load a JSON file and log file or parsing errors."""
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)
    except FileNotFoundError as error:
        _log_extract_error("FileNotFoundError", error, "load_json_file")
        raise
    except json.JSONDecodeError as error:
        _log_extract_error("JSONDecodeError", error, "load_json_file")
        raise
    except OSError as error:
        _log_extract_error("OSError", error, "load_json_file")
        raise
    except Exception as error:
        _log_extract_error(type(error).__name__, error, "load_json_file")
        raise

    if not isinstance(data, (dict, list)):
        error = ValueError("JSON root must be an object or an array.")
        _log_extract_error("UnsupportedSchemaError", error, "load_json_file")
        raise error

    return data


def inspect_json_schema(data: JsonData) -> JsonSchemaInspection:
    """Inspect an unknown JSON structure without transforming records."""
    records, record_path = _find_message_records(data)
    record_keys = _collect_record_keys(records)

    top_level_keys: list[str] = []
    if isinstance(data, dict):
        top_level_keys = sorted(str(key) for key in data.keys())

    return {
        "root_type": type(data).__name__,
        "top_level_keys": top_level_keys,
        "record_path": record_path,
        "record_count": len(records),
        "record_keys": record_keys,
        "detected_source": detect_json_source(data),
    }


def detect_json_source(data: JsonData) -> JsonSource:
    """Detect Instagram or WhatsApp JSON exports from record-level keys."""
    records, _ = _find_message_records(data)
    record_keys = set(_collect_record_keys(records))

    if INSTAGRAM_SCHEMA_KEYS.issubset(record_keys):
        return "instagram"

    if record_keys.intersection(WHATSAPP_SCHEMA_KEYS):
        return "whatsapp"

    return "unsupported"


def load_instagram_json(file_path: str | Path) -> pd.DataFrame:
    """Load Instagram JSON records into a raw DataFrame."""
    data = load_json_file(file_path)
    source = detect_json_source(data)

    if source != "instagram":
        _raise_unsupported_schema("load_instagram_json", source)

    return _records_to_dataframe(data)


def load_whatsapp_json(file_path: str | Path) -> pd.DataFrame:
    """Load WhatsApp JSON records into a raw DataFrame."""
    data = load_json_file(file_path)
    source = detect_json_source(data)

    if source != "whatsapp":
        _raise_unsupported_schema("load_whatsapp_json", source)

    return _records_to_dataframe(data)


def load_conversation_json(file_path: str | Path) -> pd.DataFrame:
    """Load a supported conversation JSON export into a raw DataFrame."""
    data = load_json_file(file_path)
    source = detect_json_source(data)

    if source == "unsupported":
        _raise_unsupported_schema("load_conversation_json", source)

    return _records_to_dataframe(data)


def _records_to_dataframe(data: JsonData) -> pd.DataFrame:
    records, _ = _find_message_records(data)

    if not records:
        error = ValueError("No message records found in JSON data.")
        _log_extract_error(
            "UnsupportedSchemaError",
            error,
            "_records_to_dataframe",
        )
        raise error

    return pd.DataFrame(records)


def _find_message_records(data: JsonData) -> tuple[list[dict[str, Any]], str | None]:
    if isinstance(data, list):
        return _filter_dict_records(data), "$"

    if not isinstance(data, dict):
        return [], None

    for key in ("messages", "chat", "conversation"):
        value = data.get(key)
        if isinstance(value, list):
            return _filter_dict_records(value), key

    for key, value in data.items():
        if isinstance(value, list) and _filter_dict_records(value):
            return _filter_dict_records(value), str(key)

    return [], None


def _filter_dict_records(records: list[Any]) -> list[dict[str, Any]]:
    return [record for record in records if isinstance(record, dict)]


def _collect_record_keys(records: list[dict[str, Any]]) -> list[str]:
    keys: set[str] = set()
    for record in records:
        keys.update(str(key) for key in record.keys())

    return sorted(keys)


def _raise_unsupported_schema(function_name: str, detected_source: str) -> None:
    error = ValueError(
        f"Unsupported JSON schema for this loader: {detected_source}."
    )
    _log_extract_error("UnsupportedSchemaError", error, function_name)
    raise error


def _log_extract_error(
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
