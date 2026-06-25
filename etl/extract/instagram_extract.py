"""Instagram Meta export extraction."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any

from logger.logger import log_critical_error


JsonData = dict[str, Any] | list[Any]


def extract_instagram_messages(file_path: str | Path) -> list[dict[str, Any]]:
    """Extract Instagram messages from Meta .json or .zip exports."""
    path = Path(file_path)

    try:
        if path.suffix.lower() == ".json":
            messages = extract_instagram_json_messages(path)
        elif path.suffix.lower() == ".zip":
            messages = extract_instagram_zip_messages(path)
        else:
            raise ValueError(f"Unsupported Instagram export file: {path}")
    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
        UnicodeError,
        ValueError,
        zipfile.BadZipFile,
    ) as error:
        _log_extract_error(type(error).__name__, error, "extract_instagram_messages")
        raise
    except Exception as error:
        _log_extract_error(type(error).__name__, error, "extract_instagram_messages")
        raise

    _print_messages(messages)
    return messages


def extract_instagram_json_messages(file_path: str | Path) -> list[dict[str, Any]]:
    """Extract raw message dictionaries from a Meta Instagram JSON file."""
    data = _load_json_file(Path(file_path))
    return _extract_messages_from_data(data)


def extract_instagram_zip_messages(file_path: str | Path) -> list[dict[str, Any]]:
    """Extract raw message dictionaries from JSON files inside a Meta ZIP export."""
    messages: list[dict[str, Any]] = []

    with zipfile.ZipFile(file_path) as archive:
        for member_name in _find_instagram_json_members(archive):
            with archive.open(member_name) as member_file:
                data = json.load(member_file)
            messages.extend(_extract_messages_from_data(data))

    if not messages:
        raise ValueError("No Instagram message records found in ZIP export.")

    return messages


def _load_json_file(file_path: Path) -> JsonData:
    with file_path.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    if not isinstance(data, (dict, list)):
        raise ValueError("Instagram JSON root must be an object or an array.")

    return data


def _extract_messages_from_data(data: JsonData) -> list[dict[str, Any]]:
    records = _find_message_records(data)
    if not records:
        raise ValueError("No Instagram message records found.")

    return [_copy_message_record(record) for record in records]


def _find_message_records(data: JsonData) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return _filter_instagram_records(data)

    if not isinstance(data, dict):
        return []

    messages = data.get("messages")
    if isinstance(messages, list):
        return _filter_instagram_records(messages)

    return []


def _filter_instagram_records(records: list[Any]) -> list[dict[str, Any]]:
    return [
        record
        for record in records
        if isinstance(record, dict)
        and "sender_name" in record
        and "timestamp_ms" in record
    ]


def _copy_message_record(record: dict[str, Any]) -> dict[str, Any]:
    copied_record = dict(record)
    copied_record["source"] = "instagram"
    return copied_record


def _find_instagram_json_members(archive: zipfile.ZipFile) -> list[str]:
    return [
        member.filename
        for member in archive.infolist()
        if not member.is_dir()
        and member.filename.lower().endswith(".json")
        and "/messages/" in f"/{member.filename.lower()}"
    ]


def _print_messages(messages: list[dict[str, Any]]) -> None:
    print(messages)


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
