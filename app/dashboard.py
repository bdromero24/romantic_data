"""Reusable dashboard helpers for already fetched message records."""

from __future__ import annotations

from typing import Any, Iterable

from analysis.metrics import calculate_message_metrics, enrich_message_records
from analysis.preprocessing import preprocess_message_records
from analysis.sentiment import (
    calculate_sentiment_summary,
    enrich_message_records as enrich_sentiment_records,
)
from logger.logger import log_critical_error


DEFAULT_TOP_TOKEN_LIMIT = 10


def prepare_dashboard_data(
    records: Iterable[dict[str, Any]],
    top_token_limit: int = DEFAULT_TOP_TOKEN_LIMIT,
) -> dict[str, Any]:
    """Return copied records and summaries needed by the Streamlit dashboard."""
    try:
        source_records = _validate_records(records)
        preprocessed_records = preprocess_message_records(source_records)
        metric_records = enrich_message_records(preprocessed_records)
        analyzed_records = enrich_sentiment_records(metric_records)

        return {
            "records": analyzed_records,
            "metrics": calculate_message_metrics(
                preprocessed_records,
                top_token_limit=top_token_limit,
            ),
            "sentiment": calculate_sentiment_summary(preprocessed_records),
        }
    except (TypeError, ValueError, KeyError) as error:
        _log_dashboard_error(
            error_type=type(error).__name__,
            error=error,
            function_name="prepare_dashboard_data",
        )
        raise


def dictionary_to_rows(
    values: dict[str, int],
    key_name: str,
    value_name: str = "message_count",
) -> list[dict[str, Any]]:
    """Convert grouped metric dictionaries into stable tabular rows."""
    if not isinstance(values, dict):
        error = TypeError("Dashboard grouped values must be a dictionary.")
        _log_dashboard_error(
            error_type=type(error).__name__,
            error=error,
            function_name="dictionary_to_rows",
        )
        raise error

    return [
        {key_name: key, value_name: count}
        for key, count in values.items()
    ]


def _validate_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(records, (str, bytes)):
        raise TypeError("Dashboard records must be an iterable of dictionaries.")

    try:
        validated_records = list(records)
    except TypeError as error:
        raise TypeError(
            "Dashboard records must be an iterable of dictionaries."
        ) from error

    for record in validated_records:
        if not isinstance(record, dict):
            raise TypeError("Dashboard records must contain only dictionaries.")

    return [dict(record) for record in validated_records]


def _log_dashboard_error(
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
