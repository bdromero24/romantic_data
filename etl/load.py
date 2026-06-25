"""Load transformed ETL records into PostgreSQL."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from sqlalchemy.exc import DatabaseError, ProgrammingError

from db.connection import get_engine
from db.queries import INSERT_MESSAGE_QUERY
from logger.logger import log_critical_error


REQUIRED_MESSAGE_FIELDS = (
    "sender",
    "message",
    "message_normalized",
    "timestamp",
    "source",
)


def load_messages(records: Iterable[dict[str, Any]]) -> dict[str, int]:
    """Insert transformed message records and return load counters."""
    try:
        validated_records = [_validate_record(record) for record in records]
        if not validated_records:
            raise ValueError("No transformed message records were provided.")

        inserted_count = 0
        engine = get_engine()
        with engine.begin() as connection:
            for record in validated_records:
                result = connection.execute(INSERT_MESSAGE_QUERY, record)
                inserted_count += max(result.rowcount or 0, 0)

        return {
            "received": len(validated_records),
            "inserted": inserted_count,
            "skipped_duplicates": len(validated_records) - inserted_count,
        }
    except ProgrammingError as error:
        _log_load_error("ProgrammingError", error, "load_messages")
        raise
    except DatabaseError as error:
        _log_load_error("DatabaseError", error, "load_messages")
        raise
    except ConnectionError as error:
        _log_load_error("ConnectionError", error, "load_messages")
        raise
    except Exception as error:
        _log_load_error(type(error).__name__, error, "load_messages")
        raise


def load_messages_from_artifact(input_path: str | Path) -> dict[str, int]:
    """Load staged transformed records from disk into PostgreSQL."""
    from etl.artifacts import load_records

    records = load_records(input_path)
    return load_messages(records)


def _validate_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise TypeError("Each transformed message record must be a dictionary.")

    missing_fields = [
        field for field in REQUIRED_MESSAGE_FIELDS if field not in record
    ]
    if missing_fields:
        missing_text = ", ".join(missing_fields)
        raise KeyError(f"Missing transformed message fields: {missing_text}")

    if not isinstance(record["sender"], str) or not record["sender"]:
        raise TypeError("Transformed message sender must be a non-empty string.")

    if not isinstance(record["source"], str) or not record["source"]:
        raise TypeError("Transformed message source must be a non-empty string.")

    if record["message"] is not None and not isinstance(record["message"], str):
        raise TypeError("Transformed message text must be a string or None.")

    if (
        record["message_normalized"] is not None
        and not isinstance(record["message_normalized"], str)
    ):
        raise TypeError(
            "Transformed normalized message text must be a string or None."
        )

    if not isinstance(record["timestamp"], datetime):
        raise TypeError("Transformed message timestamp must be a datetime.")

    return {field: record[field] for field in REQUIRED_MESSAGE_FIELDS}


def _log_load_error(
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
