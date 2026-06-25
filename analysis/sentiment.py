"""Deterministic in-memory sentiment helpers for message records."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable as IterableCollection
from typing import Any

from analysis.preprocessing import tokenize_text
from logger.logger import log_critical_error


MESSAGE_FIELD = "message"
NORMALIZED_MESSAGE_FIELD = "message_normalized"
PREPROCESSED_MESSAGE_FIELD = "message_preprocessed"
TOKEN_FIELD = "message_tokens"
SENTIMENT_LABEL_FIELD = "sentiment_label"
SENTIMENT_SCORE_FIELD = "sentiment_score"
SENTIMENT_POSITIVE_TOKEN_COUNT_FIELD = "sentiment_positive_token_count"
SENTIMENT_NEGATIVE_TOKEN_COUNT_FIELD = "sentiment_negative_token_count"
POSITIVE_LABEL = "positive"
NEGATIVE_LABEL = "negative"
NEUTRAL_LABEL = "neutral"

POSITIVE_TOKENS = frozenset(
    {
        "alegria",
        "amo",
        "amor",
        "bien",
        "bonito",
        "buena",
        "bueno",
        "contenta",
        "contento",
        "encanta",
        "excelente",
        "feliz",
        "genial",
        "gracias",
        "gusta",
        "hermosa",
        "hermoso",
        "increible",
        "jaja",
        "jajaja",
        "lindo",
        "linda",
        "mejor",
        "perfecto",
        "preciosa",
        "precioso",
        "quiero",
        "sonrisa",
    },
)

NEGATIVE_TOKENS = frozenset(
    {
        "ansiedad",
        "asco",
        "cansada",
        "cansado",
        "dolor",
        "enojada",
        "enojado",
        "feo",
        "horrible",
        "llorar",
        "mal",
        "mala",
        "malo",
        "miedo",
        "odio",
        "peor",
        "perdon",
        "problema",
        "rabia",
        "raro",
        "triste",
    },
)


def analyze_text_sentiment(message: str) -> dict[str, int | str]:
    """Return deterministic lexicon sentiment for one message string."""
    try:
        if not isinstance(message, str):
            raise TypeError("Sentiment message text must be a string.")

        return _score_tokens(tokenize_text(message))
    except TypeError as error:
        _log_sentiment_error(
            error_type=type(error).__name__,
            error=error,
            function_name="analyze_text_sentiment",
        )
        raise


def enrich_message_record(record: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of a message record with deterministic sentiment fields."""
    try:
        _validate_record(record)
        sentiment = _score_tokens(_get_record_tokens(record))
        enriched_record = dict(record)
        enriched_record.update(sentiment)
        return enriched_record
    except (KeyError, TypeError) as error:
        _log_sentiment_error(
            error_type=type(error).__name__,
            error=error,
            function_name="enrich_message_record",
        )
        raise


def enrich_message_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return copied message records with deterministic sentiment fields."""
    try:
        validated_records = _validate_records(records)
        return [enrich_message_record(record) for record in validated_records]
    except TypeError as error:
        _log_sentiment_error(
            error_type=type(error).__name__,
            error=error,
            function_name="enrich_message_records",
        )
        raise


def calculate_sentiment_summary(
    records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Return aggregate sentiment counts for already fetched records."""
    try:
        enriched_records = enrich_message_records(records)
        label_counts: Counter[str] = Counter(
            record[SENTIMENT_LABEL_FIELD] for record in enriched_records
        )
        total_records = len(enriched_records)
        total_score = sum(
            record[SENTIMENT_SCORE_FIELD] for record in enriched_records
        )

        return {
            "total_messages": total_records,
            "average_sentiment_score": _safe_average(total_score, total_records),
            "sentiment_by_label": {
                NEGATIVE_LABEL: label_counts[NEGATIVE_LABEL],
                NEUTRAL_LABEL: label_counts[NEUTRAL_LABEL],
                POSITIVE_LABEL: label_counts[POSITIVE_LABEL],
            },
        }
    except (KeyError, TypeError) as error:
        _log_sentiment_error(
            error_type=type(error).__name__,
            error=error,
            function_name="calculate_sentiment_summary",
        )
        raise


def _validate_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(records, (str, bytes)) or not isinstance(records, IterableCollection):
        raise TypeError("Sentiment records must be iterable.")

    validated_records = list(records)
    for record in validated_records:
        _validate_record(record)

    return validated_records


def _validate_record(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise TypeError("Sentiment record must be a dictionary.")

    _get_record_tokens(record)


def _get_record_tokens(record: dict[str, Any]) -> list[str]:
    if TOKEN_FIELD in record:
        return _validate_token_list(record[TOKEN_FIELD])

    for field_name in (
        PREPROCESSED_MESSAGE_FIELD,
        NORMALIZED_MESSAGE_FIELD,
        MESSAGE_FIELD,
    ):
        if field_name in record:
            value = record[field_name]
            if not isinstance(value, str):
                raise TypeError(f"Field must be a string: {field_name}")

            return tokenize_text(value)

    raise KeyError(f"Missing required field: {MESSAGE_FIELD}")


def _validate_token_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise TypeError(f"Field must be a list of strings: {TOKEN_FIELD}")

    for token in value:
        if not isinstance(token, str):
            raise TypeError(f"Field must be a list of strings: {TOKEN_FIELD}")

    return list(value)


def _score_tokens(tokens: list[str]) -> dict[str, int | str]:
    positive_count = sum(1 for token in tokens if token in POSITIVE_TOKENS)
    negative_count = sum(1 for token in tokens if token in NEGATIVE_TOKENS)
    score = positive_count - negative_count

    return {
        SENTIMENT_LABEL_FIELD: _label_from_score(score),
        SENTIMENT_SCORE_FIELD: score,
        SENTIMENT_POSITIVE_TOKEN_COUNT_FIELD: positive_count,
        SENTIMENT_NEGATIVE_TOKEN_COUNT_FIELD: negative_count,
    }


def _label_from_score(score: int) -> str:
    if score > 0:
        return POSITIVE_LABEL

    if score < 0:
        return NEGATIVE_LABEL

    return NEUTRAL_LABEL


def _safe_average(total: int, count: int) -> float:
    if count == 0:
        return 0.0

    return total / count


def _log_sentiment_error(
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
