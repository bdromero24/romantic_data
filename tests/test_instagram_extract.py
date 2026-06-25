"""Unit tests for Instagram Meta export extraction."""

import json
import zipfile

import pytest

from etl.extract.instagram_extract import (
    extract_instagram_json_messages,
    extract_instagram_messages,
    extract_instagram_zip_messages,
)


def test_extract_instagram_json_messages_returns_dictionaries(tmp_path) -> None:
    json_path = tmp_path / "instagram_messages.json"
    json_path.write_text(
        json.dumps(
            {
                "participants": [{"name": "Alice"}, {"name": "Bob"}],
                "messages": [
                    {
                        "sender_name": "Alice",
                        "timestamp_ms": 1700000000000,
                        "content": "hello",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    messages = extract_instagram_json_messages(json_path)

    assert messages == [
        {
            "sender_name": "Alice",
            "timestamp_ms": 1700000000000,
            "content": "hello",
            "source": "instagram",
        }
    ]


def test_extract_instagram_messages_prints_to_console(tmp_path, capsys) -> None:
    json_path = tmp_path / "instagram_messages.json"
    json_path.write_text(
        json.dumps(
            {
                "messages": [
                    {
                        "sender_name": "Alice",
                        "timestamp_ms": 1700000000000,
                        "content": "hello",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    messages = extract_instagram_messages(json_path)
    captured_output = capsys.readouterr()

    assert messages[0]["source"] == "instagram"
    assert "Alice" in captured_output.out
    assert "instagram" in captured_output.out


def test_extract_instagram_zip_messages_reads_json_members(tmp_path) -> None:
    zip_path = tmp_path / "instagram_export.zip"
    message_data = {
        "messages": [
            {
                "sender_name": "Bob",
                "timestamp_ms": 1700000001000,
                "content": "from zip",
            }
        ]
    }

    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr(
            "your_instagram_activity/messages/inbox/chat/message_1.json",
            json.dumps(message_data),
        )
        archive.writestr("connections/followers.json", json.dumps({"items": []}))

    messages = extract_instagram_zip_messages(zip_path)

    assert messages == [
        {
            "sender_name": "Bob",
            "timestamp_ms": 1700000001000,
            "content": "from zip",
            "source": "instagram",
        }
    ]


def test_extract_instagram_invalid_json_logs_and_raises(
    tmp_path,
    monkeypatch,
) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        "etl.extract.instagram_extract.log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )
    json_path = tmp_path / "instagram_messages.json"
    json_path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        extract_instagram_messages(json_path)

    assert logged_errors == ["JSONDecodeError"]
