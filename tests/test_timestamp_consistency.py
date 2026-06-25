"""Unit tests for transformed timestamp diagnostics."""

from datetime import datetime, timedelta, timezone

from scripts.validate_timestamp_consistency import (
    validate_timestamp_consistency,
)


BOGOTA_TIMEZONE = timezone(timedelta(hours=-5))


def test_validate_timestamp_consistency_passes_for_correct_pipeline_dates() -> None:
    diagnostics = validate_timestamp_consistency(
        [
            _record(datetime(2025, 10, 10, 8, 0, tzinfo=BOGOTA_TIMEZONE), "hola"),
            _record(
                datetime(2026, 2, 20, 14, 34, tzinfo=BOGOTA_TIMEZONE),
                "suficiente amor",
            ),
            _record(
                datetime(2026, 4, 23, 23, 13, tzinfo=BOGOTA_TIMEZONE),
                "te amo",
            ),
            _record(
                datetime(2026, 6, 12, 11, 30, tzinfo=BOGOTA_TIMEZONE),
                "te amo",
            ),
            _record(datetime(2026, 6, 21, 17, 1, tzinfo=BOGOTA_TIMEZONE), "fin"),
        ]
    )

    assert diagnostics["passed"] is True
    assert diagnostics["string_timestamp_count"] == 0
    assert diagnostics["naive_timestamp_count"] == 0
    assert diagnostics["out_of_range_count"] == 0
    assert diagnostics["suspicious_month_count"] == 0
    assert diagnostics["is_sorted"] is True
    assert diagnostics["monthly_counts"] == {
        "2025-10": 1,
        "2026-02": 1,
        "2026-04": 1,
        "2026-06": 2,
    }
    assert diagnostics["first_te_amo_timestamp"] == datetime(
        2026,
        4,
        23,
        23,
        13,
        tzinfo=BOGOTA_TIMEZONE,
    )


def test_validate_timestamp_consistency_fails_for_ambiguous_string_timestamp() -> None:
    diagnostics = validate_timestamp_consistency(
        [
            {
                "timestamp": "2026-06-12 11:30:00",
                "message_normalized": "te amo",
            }
        ]
    )

    assert diagnostics["passed"] is False
    assert diagnostics["invalid_timestamp_count"] == 1
    assert diagnostics["string_timestamp_count"] == 1


def test_validate_timestamp_consistency_fails_for_inverted_future_month() -> None:
    diagnostics = validate_timestamp_consistency(
        [
            _record(
                datetime(2026, 12, 6, 11, 30, tzinfo=BOGOTA_TIMEZONE),
                "te amo",
            )
        ]
    )

    assert diagnostics["passed"] is False
    assert diagnostics["out_of_range_count"] == 1
    assert diagnostics["suspicious_month_count"] == 1


def _record(timestamp: datetime, message_normalized: str) -> dict:
    return {
        "sender": "Alice",
        "message": message_normalized,
        "message_normalized": message_normalized,
        "timestamp": timestamp,
        "source": "whatsapp",
    }
