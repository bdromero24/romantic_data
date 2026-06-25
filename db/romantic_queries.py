"""Read-only romantic landing database helpers."""

from __future__ import annotations

from typing import Any

from sqlalchemy.exc import DatabaseError, OperationalError, ProgrammingError
from sqlalchemy.sql.elements import TextClause

from db.connection import get_engine
from db.queries import (
    ROMANTIC_AVERAGE_DAILY_MESSAGES_QUERY,
    ROMANTIC_CONVERSATION_STARTER_QUERY,
    ROMANTIC_FAVORITE_HOUR_QUERY,
    ROMANTIC_FIRST_MESSAGE_QUERY,
    ROMANTIC_FIRST_PATTERN_MESSAGE_QUERY,
    ROMANTIC_HATER_WORD_COUNT_QUERY,
    ROMANTIC_HOURLY_RHYTHM_QUERY,
    ROMANTIC_MESSAGE_BY_ID_QUERY,
    ROMANTIC_MONTHLY_RHYTHM_QUERY,
    ROMANTIC_PATTERN_COUNT_QUERY,
    ROMANTIC_PATTERN_MESSAGES_QUERY,
    ROMANTIC_PEAK_DAY_QUERY,
    ROMANTIC_PEAK_MONTH_QUERY,
    ROMANTIC_SENDER_RHYTHM_QUERY,
    ROMANTIC_SUMMARY_QUERY,
    ROMANTIC_MESSAGES_BY_IDS_QUERY,
    ROMANTIC_WEEKDAY_RHYTHM_QUERY,
    ROMANTIC_WORD_COUNTS_QUERY,
)
from logger.logger import log_critical_error


HATER_WORD_PATTERN = r"\m(odio|hate)\M"


def fetch_romantic_summary() -> dict[str, Any]:
    """Return high-level counts for the romantic landing."""
    return _fetch_one_dict(ROMANTIC_SUMMARY_QUERY, "fetch_romantic_summary")


def fetch_first_message() -> dict[str, Any] | None:
    """Return the first valid stored message."""
    return _fetch_optional_one_dict(
        ROMANTIC_FIRST_MESSAGE_QUERY,
        "fetch_first_message",
    )


def fetch_message_by_id(message_id: int) -> dict[str, Any] | None:
    """Return one valid stored message by ID."""
    parameters = {"message_id": _validate_message_id(message_id)}
    return _fetch_optional_one_dict(
        ROMANTIC_MESSAGE_BY_ID_QUERY,
        "fetch_message_by_id",
        parameters,
    )


def fetch_messages_by_ids(message_ids: list[int]) -> list[dict[str, Any]]:
    """Return valid stored messages by IDs preserving the input order."""
    valid_message_ids = _validate_message_ids(message_ids)
    if not valid_message_ids:
        return []

    rows = _fetch_all_dicts(
        ROMANTIC_MESSAGES_BY_IDS_QUERY,
        "fetch_messages_by_ids",
        {"message_ids": valid_message_ids},
    )
    records_by_id = {row["id"]: row for row in rows}
    return [
        records_by_id[message_id]
        for message_id in valid_message_ids
        if message_id in records_by_id
    ]


def count_pattern_occurrences(pattern: str) -> int:
    """Return message count for a normalized-text regex pattern."""
    parameters = {"pattern": _validate_pattern(pattern)}
    row = _fetch_one_dict(
        ROMANTIC_PATTERN_COUNT_QUERY,
        "count_pattern_occurrences",
        parameters,
    )
    return int(row["occurrence_count"])


def count_hater_word_occurrences(sender_name: str) -> int:
    """Return how many times her valid messages contain odio or hate."""
    parameters = {
        "sender_name": _validate_sender_name(sender_name),
        "pattern": HATER_WORD_PATTERN,
    }
    row = _fetch_one_dict(
        ROMANTIC_HATER_WORD_COUNT_QUERY,
        "count_hater_word_occurrences",
        parameters,
    )
    return int(row["total_odio"])


def fetch_first_pattern_message(pattern: str) -> dict[str, Any] | None:
    """Return the first valid message matching a normalized-text pattern."""
    parameters = {"pattern": _validate_pattern(pattern)}
    return _fetch_optional_one_dict(
        ROMANTIC_FIRST_PATTERN_MESSAGE_QUERY,
        "fetch_first_pattern_message",
        parameters,
    )


def fetch_pattern_messages(pattern: str, limit: int) -> list[dict[str, Any]]:
    """Return valid original messages matching a normalized-text pattern."""
    parameters = {
        "pattern": _validate_pattern(pattern),
        "limit": _validate_limit(limit),
    }
    return _fetch_all_dicts(
        ROMANTIC_PATTERN_MESSAGES_QUERY,
        "fetch_pattern_messages",
        parameters,
    )


def fetch_peak_day() -> dict[str, Any] | None:
    """Return the day with the most valid messages."""
    return _fetch_optional_one_dict(ROMANTIC_PEAK_DAY_QUERY, "fetch_peak_day")


def fetch_peak_month() -> dict[str, Any] | None:
    """Return the month with the most valid messages."""
    return _fetch_optional_one_dict(ROMANTIC_PEAK_MONTH_QUERY, "fetch_peak_month")


def fetch_favorite_hour() -> dict[str, Any] | None:
    """Return the hour with the most valid messages."""
    return _fetch_optional_one_dict(
        ROMANTIC_FAVORITE_HOUR_QUERY,
        "fetch_favorite_hour",
    )


def fetch_conversation_starter() -> dict[str, Any] | None:
    """Return the sender who started most conversation days."""
    return _fetch_optional_one_dict(
        ROMANTIC_CONVERSATION_STARTER_QUERY,
        "fetch_conversation_starter",
    )


def fetch_average_daily_messages() -> float:
    """Return the average valid messages per conversation day."""
    row = _fetch_one_dict(
        ROMANTIC_AVERAGE_DAILY_MESSAGES_QUERY,
        "fetch_average_daily_messages",
    )
    return float(row["avg_daily_messages"] or 0)


def fetch_hourly_rhythm() -> list[dict[str, Any]]:
    """Return message counts grouped by hour."""
    return _fetch_all_dicts(ROMANTIC_HOURLY_RHYTHM_QUERY, "fetch_hourly_rhythm")


def fetch_weekday_rhythm() -> list[dict[str, Any]]:
    """Return message counts grouped by ISO weekday."""
    return _fetch_all_dicts(ROMANTIC_WEEKDAY_RHYTHM_QUERY, "fetch_weekday_rhythm")


def fetch_monthly_rhythm() -> list[dict[str, Any]]:
    """Return message counts grouped by month."""
    return _fetch_all_dicts(ROMANTIC_MONTHLY_RHYTHM_QUERY, "fetch_monthly_rhythm")


def fetch_sender_rhythm(max_date: str | None = None) -> list[dict[str, Any]]:
    """Return valid message counts grouped by sender."""
    return _fetch_all_dicts(
        ROMANTIC_SENDER_RHYTHM_QUERY,
        "fetch_sender_rhythm",
        {"max_date": max_date},
    )


def fetch_romantic_word_counts(limit: int) -> list[dict[str, Any]]:
    """Return counts for romantic words from normalized messages."""
    return _fetch_all_dicts(
        ROMANTIC_WORD_COUNTS_QUERY,
        "fetch_romantic_word_counts",
        {"limit": _validate_limit(limit)},
    )


def _fetch_all_dicts(
    query: TextClause,
    function_name: str,
    parameters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    try:
        engine = get_engine()
        with engine.connect() as connection:
            result = connection.execute(query, parameters or {})
            return [_row_to_dict(row) for row in result.fetchall()]
    except ProgrammingError as error:
        _log_query_error("ProgrammingError", error, function_name)
        raise
    except OperationalError as error:
        _log_query_error("OperationalError", error, function_name)
        raise
    except DatabaseError as error:
        _log_query_error("DatabaseError", error, function_name)
        raise
    except ConnectionError as error:
        _log_query_error("ConnectionError", error, function_name)
        raise
    except Exception as error:
        _log_query_error(type(error).__name__, error, function_name)
        raise


def _fetch_one_dict(
    query: TextClause,
    function_name: str,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row = _fetch_optional_one_dict(query, function_name, parameters)
    if row is None:
        raise LookupError("Romantic query returned no rows.")

    return row


def _fetch_optional_one_dict(
    query: TextClause,
    function_name: str,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    rows = _fetch_all_dicts(query, function_name, parameters)
    if not rows:
        return None

    return rows[0]


def _row_to_dict(row: Any) -> dict[str, Any]:
    if isinstance(row, dict):
        return dict(row)

    mapping = getattr(row, "_mapping", None)
    if mapping is not None:
        return dict(mapping)

    return dict(row)


def _validate_pattern(pattern: str) -> str:
    if not isinstance(pattern, str) or not pattern.strip():
        raise ValueError("Romantic pattern must be a non-empty string.")

    return pattern.strip()


def _validate_sender_name(sender_name: str) -> str:
    if not isinstance(sender_name, str) or not sender_name.strip():
        raise ValueError("Romantic sender name must be a non-empty string.")

    return sender_name.strip()


def _validate_limit(limit: int) -> int:
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("Romantic query limit must be an integer.")

    if limit < 1 or limit > 50:
        raise ValueError("Romantic query limit must be between 1 and 50.")

    return limit


def _validate_message_id(message_id: int) -> int:
    if not isinstance(message_id, int) or isinstance(message_id, bool):
        raise TypeError("Romantic message ID must be an integer.")

    if message_id < 1:
        raise ValueError("Romantic message ID must be positive.")

    return message_id


def _validate_message_ids(message_ids: list[int]) -> list[int]:
    if not isinstance(message_ids, list):
        raise TypeError("Romantic message IDs must be a list.")

    valid_message_ids: list[int] = []
    for message_id in message_ids:
        if message_id is None:
            continue
        valid_message_ids.append(_validate_message_id(message_id))

    return valid_message_ids


def _log_query_error(
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
