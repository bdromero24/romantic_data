"""Unit tests for static landing data loading."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.static_landing_data import (
    MISSING_STATIC_DATA_MESSAGE,
    load_static_landing_data,
)


def test_load_static_landing_data_reads_json_object(tmp_path: Path) -> None:
    static_data_path = tmp_path / "landing_data.json"
    static_data_path.write_text(
        json.dumps({"hero": {"title": "Nuestra historia"}}),
        encoding="utf-8",
    )

    assert load_static_landing_data(str(static_data_path)) == {
        "hero": {"title": "Nuestra historia"}
    }


def test_load_static_landing_data_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match=MISSING_STATIC_DATA_MESSAGE):
        load_static_landing_data(str(tmp_path / "missing.json"))


def test_load_static_landing_data_rejects_non_object(tmp_path: Path) -> None:
    static_data_path = tmp_path / "landing_data.json"
    static_data_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="Static landing data must be a JSON object"):
        load_static_landing_data(str(static_data_path))
