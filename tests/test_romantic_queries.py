"""Unit tests for romantic database helper behavior."""

from db import romantic_queries


def test_fetch_messages_by_ids_preserves_input_order(monkeypatch) -> None:
    rows = [
        {"id": 3, "sender": "Mar", "message": "Tercero"},
        {"id": 1, "sender": "David", "message": "Primero"},
    ]
    calls: list[dict[str, list[int]]] = []

    def fake_fetch_all_dicts(_query, _function_name, parameters):
        calls.append(parameters)
        return rows

    monkeypatch.setattr(
        romantic_queries,
        "_fetch_all_dicts",
        fake_fetch_all_dicts,
    )

    result = romantic_queries.fetch_messages_by_ids([1, 2, 3])

    assert calls == [{"message_ids": [1, 2, 3]}]
    assert [row["id"] for row in result] == [1, 3]


def test_fetch_messages_by_ids_ignores_none_and_empty_lists(monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(
        romantic_queries,
        "_fetch_all_dicts",
        lambda *_args, **_kwargs: calls.append("called"),
    )

    assert romantic_queries.fetch_messages_by_ids([]) == []
    assert romantic_queries.fetch_messages_by_ids([None]) == []
    assert calls == []


def test_fetch_sender_rhythm_passes_cutoff_parameter(monkeypatch) -> None:
    calls: list[dict[str, str | None]] = []

    def fake_fetch_all_dicts(_query, _function_name, parameters):
        calls.append(parameters)
        return [{"label": "Mar", "value": 12}]

    monkeypatch.setattr(
        romantic_queries,
        "_fetch_all_dicts",
        fake_fetch_all_dicts,
    )

    result = romantic_queries.fetch_sender_rhythm("2026-05-31")

    assert result == [{"label": "Mar", "value": 12}]
    assert calls == [{"max_date": "2026-05-31"}]


def test_count_hater_word_occurrences_passes_sender_and_pattern(monkeypatch) -> None:
    calls: list[dict[str, str]] = []

    def fake_fetch_one_dict(_query, _function_name, parameters):
        calls.append(parameters)
        return {"total_odio": "9"}

    monkeypatch.setattr(
        romantic_queries,
        "_fetch_one_dict",
        fake_fetch_one_dict,
    )

    result = romantic_queries.count_hater_word_occurrences("Mar")

    assert result == 9
    assert calls == [
        {
            "sender_name": "Mar",
            "pattern": r"\m(odio|hate)\M",
        }
    ]


def test_hater_word_query_counts_occurrences_from_normalized_message() -> None:
    query_text = str(romantic_queries.ROMANTIC_HATER_WORD_COUNT_QUERY)

    assert "regexp_count(message_normalized, :pattern, 1, 'i')" in query_text
    assert "AS total_odio" in query_text
    assert "sender = :sender_name" in query_text
    assert "message_normalized" in query_text
    assert "message ~" not in query_text
