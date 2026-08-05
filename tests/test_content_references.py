"""Unit tests for manual content message reference extraction."""

from app.content_references import extract_configured_message_references


def test_configured_message_references_ignore_invalid_values() -> None:
    content = {
        "first_te_amo": {"message_id": 1},
        "invalid": {"message_id": None},
        "bool": {"message_id": True},
        "empty": {"message_id": ""},
        "featured_quotes": {"message_ids": [2, None, "", False, "x", 3]},
    }

    references = extract_configured_message_references(content)

    assert [reference.message_id for reference in references] == [1, 2, 3]
    assert [reference.config_path for reference in references] == [
        "ROMANTIC_CONTENT.first_te_amo.message_id",
        "ROMANTIC_CONTENT.featured_quotes.message_ids[0]",
        "ROMANTIC_CONTENT.featured_quotes.message_ids[5]",
    ]
