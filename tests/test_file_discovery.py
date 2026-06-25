"""Unit tests for extraction source discovery."""

import pytest

from etl.extract.file_discovery import detect_source


def test_detect_source_whatsapp_txt(tmp_path) -> None:
    chat_path = tmp_path / "whatsapp" / "chat_export.txt"

    assert detect_source(chat_path) == "whatsapp"


def test_detect_source_instagram_json(tmp_path) -> None:
    instagram_path = tmp_path / "ig" / "messages.json"

    assert detect_source(instagram_path) == "instagram"


def test_detect_source_instagram_json_with_ig_prefix(tmp_path) -> None:
    instagram_path = tmp_path / "ig_message_1.json"

    assert detect_source(instagram_path) == "instagram"


def test_detect_source_instagram_zip(tmp_path) -> None:
    instagram_path = tmp_path / "instagram_export.zip"

    assert detect_source(instagram_path) == "instagram"


def test_detect_source_unknown_raises_value_error(tmp_path) -> None:
    unknown_path = tmp_path / "unknown" / "messages.csv"

    with pytest.raises(ValueError):
        detect_source(unknown_path)
