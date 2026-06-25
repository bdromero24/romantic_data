"""Read-only database access helpers for stored messages."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.exc import DatabaseError, OperationalError, ProgrammingError

from db.connection import get_engine
from db.queries import (
    COUNT_ALL_MESSAGES_QUERY,
    COUNT_KEYWORD_OCCURRENCES_QUERY,
    COUNT_MESSAGES_BY_DAY_QUERY,
    COUNT_MESSAGES_BY_HOUR_QUERY,
    COUNT_MESSAGES_BY_SENDER_QUERY,
    COUNT_MESSAGES_BY_SOURCE_QUERY,
    FETCH_MESSAGES_QUERY,
)
from logger.logger import log_critical_error


DEFAULT_MESSAGE_LIMIT = 100
MAX_MESSAGE_LIMIT = 1000


def fetch_messages(
    source: str | None = None,
    sender: str | None = None,
    start_timestamp: datetime | None = None,
    end_timestamp: datetime | None = None,
    limit: int = DEFAULT_MESSAGE_LIMIT,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Return stored messages using optional database filters."""
    try:
        parameters = {
            "source": _optional_text_filter(source, "source"),
            "sender": _optional_text_filter(sender, "sender"),
            "start_timestamp": _optional_datetime_filter(
                start_timestamp,
                "start_timestamp",
            ),
            "end_timestamp": _optional_datetime_filter(
                end_timestamp,
                "end_timestamp",
            ),
            "limit": _validate_limit(limit),
            "offset": _validate_offset(offset),
        }
        rows = _fetch_all(FETCH_MESSAGES_QUERY, parameters)
        return [_row_to_dict(row) for row in rows]
    except ProgrammingError as error:
        _log_message_query_error("ProgrammingError", error, "fetch_messages")
        raise
    except OperationalError as error:
        _log_message_query_error("OperationalError", error, "fetch_messages")
        raise
    except DatabaseError as error:
        _log_message_query_error("DatabaseError", error, "fetch_messages")
        raise
    except ConnectionError as error:
        _log_message_query_error("ConnectionError", error, "fetch_messages")
        raise
    except Exception as error:
        _log_message_query_error(type(error).__name__, error, "fetch_messages")
        raise


def count_all_messages() -> int:
    """Return the total number of stored messages."""
    try:
        row = _fetch_one(COUNT_ALL_MESSAGES_QUERY)
        return int(_row_to_dict(row)["message_count"])
    except ProgrammingError as error:
        _log_message_query_error("ProgrammingError", error, "count_all_messages")
        raise
    except OperationalError as error:
        _log_message_query_error("OperationalError", error, "count_all_messages")
        raise
    except DatabaseError as error:
        _log_message_query_error("DatabaseError", error, "count_all_messages")
        raise
    except ConnectionError as error:
        _log_message_query_error("ConnectionError", error, "count_all_messages")
        raise
    except Exception as error:
        _log_message_query_error(type(error).__name__, error, "count_all_messages")
        raise


def count_messages_by_source() -> list[dict[str, Any]]:
    """Return message counts grouped by source."""
    return _run_grouped_count(COUNT_MESSAGES_BY_SOURCE_QUERY, "count_messages_by_source")


def count_messages_by_sender() -> list[dict[str, Any]]:
    """Return message counts grouped by sender."""
    return _run_grouped_count(COUNT_MESSAGES_BY_SENDER_QUERY, "count_messages_by_sender")


def count_messages_by_day() -> list[dict[str, Any]]:
    """Return message counts grouped by day."""
    return _run_grouped_count(COUNT_MESSAGES_BY_DAY_QUERY, "count_messages_by_day")


def count_messages_by_hour() -> list[dict[str, Any]]:
    """Return message counts grouped by hour."""
    return _run_grouped_count(COUNT_MESSAGES_BY_HOUR_QUERY, "count_messages_by_hour")


def count_keyword_occurrences(keyword: str) -> int:
    """Return the number of messages containing a literal keyword."""
    try:
        normalized_keyword = _validate_keyword(keyword)
        row = _fetch_one(
            COUNT_KEYWORD_OCCURRENCES_QUERY,
            {"keyword_pattern": f"%{_escape_like_pattern(normalized_keyword)}%"},
        )
        return int(_row_to_dict(row)["occurrence_count"])
    except ProgrammingError as error:
        _log_message_query_error(
            "ProgrammingError",
            error,
            "count_keyword_occurrences",
        )
        raise
    except OperationalError as error:
        _log_message_query_error(
            "OperationalError",
            error,
            "count_keyword_occurrences",
        )
        raise
    except DatabaseError as error:
        _log_message_query_error("DatabaseError", error, "count_keyword_occurrences")
        raise
    except ConnectionError as error:
        _log_message_query_error("ConnectionError", error, "count_keyword_occurrences")
        raise
    except Exception as error:
        _log_message_query_error(
            type(error).__name__,
            error,
            "count_keyword_occurrences",
        )
        raise


def _run_grouped_count(query: Any, function_name: str) -> list[dict[str, Any]]:
    try:
        rows = _fetch_all(query)
        return [_row_to_dict(row) for row in rows]
    except ProgrammingError as error:
        _log_message_query_error("ProgrammingError", error, function_name)
        raise
    except OperationalError as error:
        _log_message_query_error("OperationalError", error, function_name)
        raise
    except DatabaseError as error:
        _log_message_query_error("DatabaseError", error, function_name)
        raise
    except ConnectionError as error:
        _log_message_query_error("ConnectionError", error, function_name)
        raise
    except Exception as error:
        _log_message_query_error(type(error).__name__, error, function_name)
        raise


def _fetch_all(query: Any, parameters: dict[str, Any] | None = None) -> list[Any]:
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(query, parameters or {})
        return list(result.fetchall())


def _fetch_one(query: Any, parameters: dict[str, Any] | None = None) -> Any:
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(query, parameters or {})
        row = result.fetchone()

    if row is None:
        raise LookupError("Database query returned no rows.")

    return row


def _row_to_dict(row: Any) -> dict[str, Any]:
    if isinstance(row, dict):
        return dict(row)

    mapping = getattr(row, "_mapping", None)
    if mapping is not None:
        return dict(mapping)

    return dict(row)


def _optional_text_filter(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Message {field_name} filter must be a non-empty string.")

    return value.strip()


def _optional_datetime_filter(
    value: datetime | None,
    field_name: str,
) -> datetime | None:
    if value is None:
        return None

    if not isinstance(value, datetime):
        raise TypeError(f"Message {field_name} filter must be a datetime.")

    return value


def _validate_limit(limit: int) -> int:
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("Message query limit must be an integer.")

    if limit < 1 or limit > MAX_MESSAGE_LIMIT:
        raise ValueError(
            f"Message query limit must be between 1 and {MAX_MESSAGE_LIMIT}."
        )

    return limit


def _validate_offset(offset: int) -> int:
    if not isinstance(offset, int) or isinstance(offset, bool):
        raise TypeError("Message query offset must be an integer.")

    if offset < 0:
        raise ValueError("Message query offset must be greater than or equal to zero.")

    return offset


def _validate_keyword(keyword: str) -> str:
    if not isinstance(keyword, str) or not keyword.strip():
        raise ValueError("Keyword must be a non-empty string.")

    return keyword.strip()


def _escape_like_pattern(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def _log_message_query_error(
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
