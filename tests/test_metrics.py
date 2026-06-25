"""Unit tests for deterministic analysis metrics."""

from datetime import datetime, timezone

import pytest

from analysis import metrics


def test_enrich_message_record_preserves_original_fields() -> None:
    timestamp = datetime(2026, 6, 8, 14, 30, tzinfo=timezone.utc)
    record = {
        "sender": "Alice",
        "message": "Hola mundo",
        "message_tokens": ["hola", "mundo"],
        "timestamp": timestamp,
        "source": "instagram",
    }

    result = metrics.enrich_message_record(record)

    assert result == {
        "sender": "Alice",
        "message": "Hola mundo",
        "message_tokens": ["hola", "mundo"],
        "timestamp": timestamp,
        "source": "instagram",
        "message_character_count": 10,
        "message_token_count": 2,
    }
    assert "message_character_count" not in record
    assert "message_token_count" not in record


def test_enrich_message_records_accepts_non_preprocessed_records() -> None:
    records = [
        {"sender": "Alice", "message": "Hola mundo", "source": "whatsapp"},
        {"sender": "Bob", "message": "", "source": "instagram"},
    ]

    result = metrics.enrich_message_records(records)

    assert [record["message_character_count"] for record in result] == [10, 0]
    assert [record["message_token_count"] for record in result] == [2, 0]
    assert "message_character_count" not in records[0]


def test_calculate_message_metrics_returns_aggregate_counts() -> None:
    records = [
        {
            "sender": "Alice",
            "message": "Hola mundo",
            "message_tokens": ["hola", "mundo"],
            "timestamp": datetime(2026, 6, 8, 14, 30, tzinfo=timezone.utc),
            "source": "instagram",
        },
        {
            "sender": "Alice",
            "message": "Hola otra vez",
            "message_tokens": ["hola", "otra", "vez"],
            "timestamp": datetime(2026, 6, 8, 15, 45, tzinfo=timezone.utc),
            "source": "whatsapp",
        },
        {
            "sender": "Bob",
            "message": "",
            "message_tokens": [],
            "timestamp": datetime(2026, 6, 9, 14, 0, tzinfo=timezone.utc),
            "source": "whatsapp",
        },
    ]

    result = metrics.calculate_message_metrics(records, top_token_limit=2)

    assert result == {
        "total_messages": 3,
        "total_characters": 23,
        "total_tokens": 5,
        "average_message_character_count": 23 / 3,
        "average_message_token_count": 5 / 3,
        "messages_by_sender": {"Alice": 2, "Bob": 1},
        "messages_by_source": {"instagram": 1, "whatsapp": 2},
        "messages_by_day": {"2026-06-08": 2, "2026-06-09": 1},
        "messages_by_hour": {"14": 2, "15": 1},
        "top_tokens": [
            {"token": "hola", "count": 2},
            {"token": "mundo", "count": 1},
        ],
    }


def test_count_messages_by_field_groups_missing_values_as_unknown() -> None:
    records = [
        {"sender": "Alice", "message": "Uno"},
        {"sender": "", "message": "Dos"},
        {"message": "Tres"},
    ]

    result = metrics.count_messages_by_field(records, "sender")

    assert result == {"Alice": 1, "unknown": 2}


def test_calculate_message_metrics_accepts_empty_records() -> None:
    result = metrics.calculate_message_metrics([])

    assert result == {
        "total_messages": 0,
        "total_characters": 0,
        "total_tokens": 0,
        "average_message_character_count": 0.0,
        "average_message_token_count": 0.0,
        "messages_by_sender": {},
        "messages_by_source": {},
        "messages_by_day": {},
        "messages_by_hour": {},
        "top_tokens": [],
    }


def test_metrics_error_is_logged(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        metrics,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(KeyError, match="Missing required field"):
        metrics.enrich_message_record({"sender": "Alice"})

    assert logged_errors == ["KeyError"]


def test_calculate_message_metrics_logs_invalid_timestamp(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        metrics,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(TypeError, match="Field must be a datetime"):
        metrics.calculate_message_metrics(
            [{"message": "Hola", "timestamp": "2026-06-08"}],
        )

    assert logged_errors == ["TypeError"]
