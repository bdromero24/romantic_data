"""Validate transformed ETL timestamp consistency."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from etl.artifacts import load_records


BOGOTA_TIMEZONE = timezone(timedelta(hours=-5))
MIN_EXPECTED_TIMESTAMP = datetime(2025, 10, 10, tzinfo=BOGOTA_TIMEZONE)
MAX_EXPECTED_TIMESTAMP = datetime(2026, 6, 21, 23, 59, 59, tzinfo=BOGOTA_TIMEZONE)
INVERTED_FUTURE_MONTHS = {8, 12}
TE_AMO_PATTERN = re.compile(r"(?<!\w)te\s+amo(?!\w)")


def validate_timestamp_consistency(
    records: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    """Return deterministic timestamp diagnostics for transformed records."""
    materialized_records = list(records)
    timestamps = [_get_timestamp(record) for record in materialized_records]

    invalid_timestamp_count = sum(
        not isinstance(timestamp, datetime) for timestamp in timestamps
    )
    string_timestamp_count = sum(
        isinstance(timestamp, str) for timestamp in timestamps
    )
    naive_timestamp_count = sum(
        isinstance(timestamp, datetime) and timestamp.tzinfo is None
        for timestamp in timestamps
    )

    valid_timestamps = [
        timestamp
        for timestamp in timestamps
        if isinstance(timestamp, datetime) and timestamp.tzinfo is not None
    ]
    local_timestamps = [
        timestamp.astimezone(BOGOTA_TIMEZONE)
        for timestamp in valid_timestamps
    ]

    out_of_range_count = sum(
        timestamp < MIN_EXPECTED_TIMESTAMP
        or timestamp > MAX_EXPECTED_TIMESTAMP
        for timestamp in local_timestamps
    )
    suspicious_month_count = sum(
        timestamp.year == 2026 and timestamp.month in INVERTED_FUTURE_MONTHS
        for timestamp in local_timestamps
    )
    ambiguous_day_month_count = sum(
        timestamp.day <= 12 and timestamp.month <= 12
        for timestamp in local_timestamps
    )
    is_sorted = local_timestamps == sorted(local_timestamps)
    monthly_counts = _count_by_month(local_timestamps)
    first_te_amo_timestamp = _find_first_te_amo_timestamp(materialized_records)

    passed = all(
        [
            invalid_timestamp_count == 0,
            string_timestamp_count == 0,
            naive_timestamp_count == 0,
            out_of_range_count == 0,
            suspicious_month_count == 0,
            is_sorted,
        ]
    )

    return {
        "total_records": len(materialized_records),
        "invalid_timestamp_count": invalid_timestamp_count,
        "string_timestamp_count": string_timestamp_count,
        "naive_timestamp_count": naive_timestamp_count,
        "out_of_range_count": out_of_range_count,
        "suspicious_month_count": suspicious_month_count,
        "ambiguous_day_month_count": ambiguous_day_month_count,
        "is_sorted": is_sorted,
        "monthly_counts": dict(sorted(monthly_counts.items())),
        "first_te_amo_timestamp": first_te_amo_timestamp,
        "passed": passed,
    }


def load_and_validate_artifact(input_path: str | Path) -> dict[str, Any]:
    """Load a transformed artifact and return timestamp diagnostics."""
    return validate_timestamp_consistency(load_records(input_path))


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for timestamp diagnostics."""
    parser = argparse.ArgumentParser(
        description="Validate transformed ETL timestamps.",
    )
    parser.add_argument(
        "input_path",
        help="Transformed ETL artifact path, parquet or csv.",
    )
    return parser


def main() -> None:
    """Run timestamp diagnostics from the command line."""
    parser = build_argument_parser()
    arguments = parser.parse_args()
    diagnostics = load_and_validate_artifact(arguments.input_path)

    for key, value in diagnostics.items():
        print(f"{key}: {value}")

    if not diagnostics["passed"]:
        raise SystemExit(1)


def _get_timestamp(record: dict[str, Any]) -> Any:
    return record.get("timestamp")


def _count_by_month(timestamps: Iterable[datetime]) -> Counter[str]:
    return Counter(timestamp.strftime("%Y-%m") for timestamp in timestamps)


def _find_first_te_amo_timestamp(
    records: Iterable[dict[str, Any]],
) -> datetime | None:
    candidates: list[datetime] = []

    for record in records:
        message_normalized = str(record.get("message_normalized", "")).lower()
        if TE_AMO_PATTERN.search(message_normalized) is None:
            continue

        timestamp = record.get("timestamp")
        if isinstance(timestamp, datetime) and timestamp.tzinfo is not None:
            candidates.append(timestamp.astimezone(BOGOTA_TIMEZONE))

    if not candidates:
        return None

    return min(candidates)


if __name__ == "__main__":
    main()
