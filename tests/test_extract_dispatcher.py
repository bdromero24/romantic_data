"""Unit tests for the extraction dispatcher."""

import json

from etl.extract.extract_dispatcher import extract_messages


def test_extract_messages_routes_whatsapp(tmp_path) -> None:
    chat_path = tmp_path / "whatsapp_chat.txt"
    chat_path.write_text(
        "5/29/2026, 19:45 - Alice: Hola\n",
        encoding="utf-8",
    )

    messages = extract_messages(chat_path)

    assert len(messages) == 1
    assert messages[0]["source"] == "whatsapp"
    assert messages[0]["message"] == "Hola"


def test_extract_messages_routes_instagram(tmp_path, capsys) -> None:
    instagram_path = tmp_path / "instagram_messages.json"
    instagram_path.write_text(
        json.dumps(
            {
                "messages": [
                    {
                        "sender_name": "Alice",
                        "timestamp_ms": 1700000000000,
                        "content": "Hola",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    messages = extract_messages(instagram_path)
    capsys.readouterr()

    assert len(messages) == 1
    assert messages[0]["source"] == "instagram"
    assert messages[0]["content"] == "Hola"
