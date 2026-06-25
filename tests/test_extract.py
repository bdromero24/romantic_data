"""Unit tests for ETL JSON extraction."""

import json

import pandas as pd
import pytest

from etl import extract


def test_inspect_json_schema_detects_instagram() -> None:
    data = {
        "participants": [{"name": "A"}],
        "messages": [
            {
                "sender_name": "A",
                "timestamp_ms": 1700000000000,
                "content": "hello",
            }
        ],
    }

    schema = extract.inspect_json_schema(data)

    assert schema["detected_source"] == "instagram"
    assert schema["record_path"] == "messages"
    assert schema["record_count"] == 1
    assert "sender_name" in schema["record_keys"]


def test_load_instagram_json_returns_raw_dataframe(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(extract, "log_critical_error", lambda *args, **kwargs: None)
    json_path = tmp_path / "instagram.json"
    json_path.write_text(
        json.dumps(
            {
                "messages": [
                    {
                        "sender_name": "A",
                        "timestamp_ms": 1700000000000,
                        "content": "hello",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    dataframe = extract.load_instagram_json(json_path)

    assert isinstance(dataframe, pd.DataFrame)
    assert list(dataframe.columns) == [
        "sender_name",
        "timestamp_ms",
        "content",
    ]
    assert dataframe.loc[0, "content"] == "hello"


def test_load_whatsapp_json_returns_raw_dataframe(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(extract, "log_critical_error", lambda *args, **kwargs: None)
    json_path = tmp_path / "whatsapp.json"
    json_path.write_text(
        json.dumps(
            [
                {
                    "sender": "B",
                    "timestamp": "2026-05-29T12:00:00",
                    "message": "hola",
                }
            ]
        ),
        encoding="utf-8",
    )

    dataframe = extract.load_whatsapp_json(json_path)

    assert isinstance(dataframe, pd.DataFrame)
    assert list(dataframe.columns) == ["sender", "timestamp", "message"]
    assert dataframe.loc[0, "message"] == "hola"


def test_invalid_json_is_logged_and_raised(tmp_path, monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        extract,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )
    json_path = tmp_path / "invalid.json"
    json_path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        extract.load_json_file(json_path)

    assert logged_errors == ["JSONDecodeError"]


def test_unsupported_schema_is_logged_and_raised(
    tmp_path,
    monkeypatch,
) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        extract,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )
    json_path = tmp_path / "unsupported.json"
    json_path.write_text(
        json.dumps({"items": [{"id": 1}]}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        extract.load_conversation_json(json_path)

    assert logged_errors == ["UnsupportedSchemaError"]
