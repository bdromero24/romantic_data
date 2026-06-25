"""Unit tests for deterministic sentiment analysis helpers."""

from datetime import datetime, timezone

import pytest

from analysis import sentiment


def test_analyze_text_sentiment_supports_spanish_accents() -> None:
    result = sentiment.analyze_text_sentiment(
        "Estoy feliz, qu\u00e9 d\u00eda tan incre\u00edble!"
    )

    assert result == {
        "sentiment_label": "positive",
        "sentiment_score": 2,
        "sentiment_positive_token_count": 2,
        "sentiment_negative_token_count": 0,
    }


def test_analyze_text_sentiment_returns_neutral_for_balanced_message() -> None:
    result = sentiment.analyze_text_sentiment("bien pero triste")

    assert result["sentiment_label"] == "neutral"
    assert result["sentiment_score"] == 0


def test_enrich_message_record_preserves_original_fields() -> None:
    timestamp = datetime(2026, 6, 8, 14, 30, tzinfo=timezone.utc)
    record = {
        "sender": "Alice",
        "message": "Me encanta este d\u00eda",
        "message_tokens": ["me", "encanta", "este", "dia"],
        "timestamp": timestamp,
        "source": "instagram",
    }

    result = sentiment.enrich_message_record(record)

    assert result == {
        "sender": "Alice",
        "message": "Me encanta este d\u00eda",
        "message_tokens": ["me", "encanta", "este", "dia"],
        "timestamp": timestamp,
        "source": "instagram",
        "sentiment_label": "positive",
        "sentiment_score": 1,
        "sentiment_positive_token_count": 1,
        "sentiment_negative_token_count": 0,
    }
    assert "sentiment_label" not in record


def test_enrich_message_records_accepts_non_preprocessed_records() -> None:
    records = [
        {"sender": "Alice", "message": "Todo bien", "source": "whatsapp"},
        {"sender": "Bob", "message": "Estoy triste", "source": "instagram"},
        {"sender": "Carol", "message": "", "source": "whatsapp"},
    ]

    result = sentiment.enrich_message_records(records)

    assert [record["sentiment_label"] for record in result] == [
        "positive",
        "negative",
        "neutral",
    ]
    assert "sentiment_label" not in records[0]


def test_calculate_sentiment_summary_returns_label_counts() -> None:
    records = [
        {"message": "feliz genial"},
        {"message": "triste"},
        {"message": "hola"},
    ]

    result = sentiment.calculate_sentiment_summary(records)

    assert result == {
        "total_messages": 3,
        "average_sentiment_score": 1 / 3,
        "sentiment_by_label": {
            "negative": 1,
            "neutral": 1,
            "positive": 1,
        },
    }


def test_calculate_sentiment_summary_accepts_empty_records() -> None:
    result = sentiment.calculate_sentiment_summary([])

    assert result == {
        "total_messages": 0,
        "average_sentiment_score": 0.0,
        "sentiment_by_label": {
            "negative": 0,
            "neutral": 0,
            "positive": 0,
        },
    }


def test_sentiment_error_is_logged(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        sentiment,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(KeyError, match="Missing required field"):
        sentiment.enrich_message_record({"sender": "Alice"})

    assert logged_errors == ["KeyError"]


def test_enrich_message_record_logs_invalid_tokens(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        sentiment,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(TypeError, match="Field must be a list of strings"):
        sentiment.enrich_message_record({"message": "Hola", "message_tokens": "hola"})

    assert logged_errors == ["TypeError"]
