"""Unit tests for dashboard helper logic."""

from datetime import datetime, timezone

import pytest

from app import dashboard


def test_prepare_dashboard_data_returns_metrics_sentiment_and_records() -> None:
    records = [
        {
            "sender": "Alice",
            "message": "Estoy feliz",
            "message_normalized": "estoy feliz",
            "timestamp": datetime(2026, 6, 8, 14, 30, tzinfo=timezone.utc),
            "source": "instagram",
        },
        {
            "sender": "Bob",
            "message": "Estoy triste",
            "message_normalized": "estoy triste",
            "timestamp": datetime(2026, 6, 8, 15, 0, tzinfo=timezone.utc),
            "source": "whatsapp",
        },
    ]

    result = dashboard.prepare_dashboard_data(records, top_token_limit=1)

    assert result["metrics"]["total_messages"] == 2
    assert result["metrics"]["messages_by_source"] == {
        "instagram": 1,
        "whatsapp": 1,
    }
    assert result["metrics"]["top_tokens"] == [{"token": "estoy", "count": 2}]
    assert result["sentiment"]["sentiment_by_label"] == {
        "negative": 1,
        "neutral": 0,
        "positive": 1,
    }
    assert [record["sentiment_label"] for record in result["records"]] == [
        "positive",
        "negative",
    ]
    assert "message_tokens" not in records[0]


def test_prepare_dashboard_data_accepts_empty_records() -> None:
    result = dashboard.prepare_dashboard_data([])

    assert result["records"] == []
    assert result["metrics"]["total_messages"] == 0
    assert result["sentiment"]["total_messages"] == 0


def test_dictionary_to_rows_preserves_dictionary_order() -> None:
    result = dashboard.dictionary_to_rows(
        {"instagram": 2, "whatsapp": 1},
        key_name="source",
    )

    assert result == [
        {"source": "instagram", "message_count": 2},
        {"source": "whatsapp", "message_count": 1},
    ]


def test_dashboard_error_is_logged(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        dashboard,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(TypeError, match="Dashboard records"):
        dashboard.prepare_dashboard_data("invalid")

    assert logged_errors == ["TypeError"]
