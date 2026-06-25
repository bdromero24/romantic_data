"""Deterministic in-memory metrics for already loaded message records."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable as IterableCollection
from datetime import datetime
from typing import Any

from logger.logger import log_critical_error


MESSAGE_FIELD = "message"
TOKEN_FIELD = "message_tokens"
PREPROCESSED_MESSAGE_FIELD = "message_preprocessed"
NORMALIZED_MESSAGE_FIELD = "message_normalized"
SENDER_FIELD = "sender"
SOURCE_FIELD = "source"
TIMESTAMP_FIELD = "timestamp"
MESSAGE_CHARACTER_COUNT_FIELD = "message_character_count"
MESSAGE_TOKEN_COUNT_FIELD = "message_token_count"
UNKNOWN_GROUP_VALUE = "unknown"
DEFAULT_TOP_TOKEN_LIMIT = 10


def enrich_message_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of a message record with deterministic metric fields."""
    try:
        _validate_record(record)
        enriched_record = dict(record)
        enriched_record[MESSAGE_CHARACTER_COUNT_FIELD] = len(
            _require_message_text(record),
        )
        enriched_record[MESSAGE_TOKEN_COUNT_FIELD] = len(_get_record_tokens(record))
        return enriched_record
    except (TypeError, KeyError) as error:
        _log_metrics_error(
            error_type=type(error).__name__,
            error=error,
            function_name="enrich_message_record",
        )
        raise


def enrich_message_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return copied message records with metric fields."""
    try:
        validated_records = _validate_records(records)
        return [enrich_message_record(record) for record in validated_records]
    except TypeError as error:
        _log_metrics_error(
            error_type=type(error).__name__,
            error=error,
            function_name="enrich_message_records",
        )
        raise


def calculate_message_metrics(
    records: Iterable[dict[str, Any]],
    top_token_limit: int = DEFAULT_TOP_TOKEN_LIMIT,
) -> dict[str, Any]:
    """Return aggregate metrics for already fetched or preprocessed records."""
    try:
        validated_records = _validate_records(records)
        validated_top_token_limit = _validate_top_token_limit(top_token_limit)
        enriched_records = [
            _build_internal_metric_record(record)
            for record in validated_records
        ]
        total_messages = len(enriched_records)
        total_characters = sum(
            record[MESSAGE_CHARACTER_COUNT_FIELD]
            for record in enriched_records
        )
        total_tokens = sum(
            record[MESSAGE_TOKEN_COUNT_FIELD]
            for record in enriched_records
        )

        return {
            "total_messages": total_messages,
            "total_characters": total_characters,
            "total_tokens": total_tokens,
            "average_message_character_count": _safe_average(
                total_characters,
                total_messages,
            ),
            "average_message_token_count": _safe_average(
                total_tokens,
                total_messages,
            ),
            "messages_by_sender": _count_by_field(
                enriched_records,
                SENDER_FIELD,
            ),
            "messages_by_source": _count_by_field(
                enriched_records,
                SOURCE_FIELD,
            ),
            "messages_by_day": _count_by_timestamp_part(
                enriched_records,
                "day",
            ),
            "messages_by_hour": _count_by_timestamp_part(
                enriched_records,
                "hour",
            ),
            "top_tokens": _top_tokens(
                enriched_records,
                validated_top_token_limit,
            ),
        }
    except (TypeError, KeyError, ValueError) as error:
        _log_metrics_error(
            error_type=type(error).__name__,
            error=error,
            function_name="calculate_message_metrics",
        )
        raise


def count_messages_by_field(
    records: Iterable[dict[str, Any]],
    field_name: str,
) -> dict[str, int]:
    """Return deterministic message counts grouped by one record field."""
    try:
        validated_records = _validate_records(records)
        if not isinstance(field_name, str) or not field_name.strip():
            raise ValueError("Metric field name must be a non-empty string.")

        return _count_by_field(validated_records, field_name.strip())
    except (TypeError, ValueError) as error:
        _log_metrics_error(
            error_type=type(error).__name__,
            error=error,
            function_name="count_messages_by_field",
        )
        raise


def _build_internal_metric_record(record: dict[str, Any]) -> dict[str, Any]:
    _validate_record(record)
    metric_record = dict(record)
    metric_record[MESSAGE_CHARACTER_COUNT_FIELD] = len(_require_message_text(record))
    metric_record[MESSAGE_TOKEN_COUNT_FIELD] = len(_get_record_tokens(record))
    metric_record["_metric_tokens"] = _get_record_tokens(record)
    return metric_record


def _validate_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(records, (str, bytes)) or not isinstance(records, IterableCollection):
        raise TypeError("Metric records must be iterable.")

    validated_records = list(records)
    for record in validated_records:
        _validate_record(record)

    return validated_records


def _validate_record(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError("Metric record must be a dictionary.")

    _require_message_text(record)


def _require_message_text(record: dict[str, Any]) -> str:
    if MESSAGE_FIELD not in record:
        raise KeyError(f"Missing required field: {MESSAGE_FIELD}")

    message = record[MESSAGE_FIELD]
    if not isinstance(message, str):
        raise TypeError(f"Field must be a string: {MESSAGE_FIELD}")

    return message


def _get_record_tokens(record: dict[str, Any]) -> list[str]:
    if TOKEN_FIELD in record:
        return _validate_token_list(record[TOKEN_FIELD])

    token_source = _get_token_source_text(record)
    if not token_source:
        return []

    return token_source.split()


def _get_token_source_text(record: dict[str, Any]) -> str:
    for field_name in (
        PREPROCESSED_MESSAGE_FIELD,
        NORMALIZED_MESSAGE_FIELD,
        MESSAGE_FIELD,
    ):
        if field_name in record:
            value = record[field_name]
            if not isinstance(value, str):
                raise TypeError(f"Field must be a string: {field_name}")

            return value

    return ""


def _validate_token_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise TypeError(f"Field must be a list of strings: {TOKEN_FIELD}")

    for token in value:
        if not isinstance(token, str):
            raise TypeError(f"Field must be a list of strings: {TOKEN_FIELD}")

    return list(value)


def _count_by_field(records: list[dict[str, Any]], field_name: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for record in records:
        raw_value = record.get(field_name, UNKNOWN_GROUP_VALUE)
        group_value = _string_group_value(raw_value)
        counts[group_value] += 1

    return dict(sorted(counts.items()))


def _string_group_value(value: Any) -> str:
    if value is None:
        return UNKNOWN_GROUP_VALUE

    if isinstance(value, str):
        stripped_value = value.strip()
        return stripped_value if stripped_value else UNKNOWN_GROUP_VALUE

    return str(value)


def _count_by_timestamp_part(
    records: list[dict[str, Any]],
    timestamp_part: str,
) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for record in records:
        timestamp = record.get(TIMESTAMP_FIELD)
        if timestamp is None:
            continue

        if not isinstance(timestamp, datetime):
            raise TypeError(f"Field must be a datetime: {TIMESTAMP_FIELD}")

        if timestamp_part == "day":
            counts[timestamp.date().isoformat()] += 1
        elif timestamp_part == "hour":
            counts[f"{timestamp.hour:02d}"] += 1
        else:
            raise ValueError(f"Unsupported timestamp metric: {timestamp_part}")

    return dict(sorted(counts.items()))


def _top_tokens(
    records: list[dict[str, Any]],
    top_token_limit: int,
) -> list[dict[str, Any]]:
    token_counts: Counter[str] = Counter()
    for record in records:
        token_counts.update(record["_metric_tokens"])

    sorted_tokens = sorted(
        token_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )
    return [
        {"token": token, "count": count}
        for token, count in sorted_tokens[:top_token_limit]
    ]


def _validate_top_token_limit(top_token_limit: int) -> int:
    if not isinstance(top_token_limit, int) or isinstance(top_token_limit, bool):
        raise TypeError("Top token limit must be an integer.")

    if top_token_limit < 0:
        raise ValueError("Top token limit must be greater than or equal to zero.")

    return top_token_limit


def _safe_average(total: int, count: int) -> float:
    if count == 0:
        return 0.0

    return total / count


def _log_metrics_error(
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
