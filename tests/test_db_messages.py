"""Unit tests for read-only message database helpers."""

from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import DatabaseError

from db import messages
from db.queries import (
    COUNT_ALL_MESSAGES_QUERY,
    COUNT_KEYWORD_OCCURRENCES_QUERY,
    COUNT_MESSAGES_BY_SOURCE_QUERY,
    FETCH_MESSAGES_QUERY,
)


def test_fetch_messages_uses_parameterized_filters(monkeypatch) -> None:
    expected_timestamp = datetime(2026, 5, 29, 19, 30, tzinfo=timezone.utc)
    engine = _FakeEngine(
        [
            _FakeResult(
                rows=[
                    {
                        "id": 1,
                        "source": "instagram",
                        "sender": "Alice",
                        "message": "Hola",
                        "message_normalized": "hola",
                        "timestamp": expected_timestamp,
                        "created_at": expected_timestamp,
                    }
                ]
            )
        ]
    )
    monkeypatch.setattr(messages, "get_engine", lambda: engine)

    result = messages.fetch_messages(
        source="instagram",
        sender="Alice",
        start_timestamp=expected_timestamp,
        end_timestamp=expected_timestamp,
        limit=25,
        offset=5,
    )

    assert result[0]["sender"] == "Alice"
    query, parameters = engine.connection.executions[0]
    assert query is FETCH_MESSAGES_QUERY
    assert parameters == {
        "source": "instagram",
        "sender": "Alice",
        "start_timestamp": expected_timestamp,
        "end_timestamp": expected_timestamp,
        "limit": 25,
        "offset": 5,
    }


def test_fetch_messages_rejects_invalid_limit(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        messages,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(ValueError, match="limit must be between"):
        messages.fetch_messages(limit=0)

    assert logged_errors == ["ValueError"]


def test_count_all_messages_returns_integer(monkeypatch) -> None:
    engine = _FakeEngine([_FakeResult(rows=[{"message_count": 3}])])
    monkeypatch.setattr(messages, "get_engine", lambda: engine)

    assert messages.count_all_messages() == 3
    query, parameters = engine.connection.executions[0]
    assert query is COUNT_ALL_MESSAGES_QUERY
    assert parameters == {}


def test_count_messages_by_source_returns_rows(monkeypatch) -> None:
    engine = _FakeEngine(
        [_FakeResult(rows=[{"source": "instagram", "message_count": 2}])]
    )
    monkeypatch.setattr(messages, "get_engine", lambda: engine)

    assert messages.count_messages_by_source() == [
        {"source": "instagram", "message_count": 2}
    ]
    query, parameters = engine.connection.executions[0]
    assert query is COUNT_MESSAGES_BY_SOURCE_QUERY
    assert parameters == {}


def test_count_keyword_occurrences_escapes_like_wildcards(monkeypatch) -> None:
    engine = _FakeEngine([_FakeResult(rows=[{"occurrence_count": 1}])])
    monkeypatch.setattr(messages, "get_engine", lambda: engine)

    assert messages.count_keyword_occurrences("50%_ok") == 1
    query, parameters = engine.connection.executions[0]
    assert query is COUNT_KEYWORD_OCCURRENCES_QUERY
    assert parameters == {"keyword_pattern": "%50\\%\\_ok%"}


def test_query_errors_are_logged_and_reraised(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(messages, "get_engine", lambda: _FailingEngine())
    monkeypatch.setattr(
        messages,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(DatabaseError):
        messages.count_all_messages()

    assert logged_errors == ["DatabaseError"]


class _FakeResult:
    def __init__(self, rows: list[dict]) -> None:
        self.rows = rows

    def fetchall(self) -> list[dict]:
        return self.rows

    def fetchone(self) -> dict | None:
        if not self.rows:
            return None

        return self.rows[0]


class _FakeConnection:
    def __init__(self, results: list[_FakeResult]) -> None:
        self.results = results
        self.executions: list[tuple] = []

    def __enter__(self) -> "_FakeConnection":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def execute(self, query, parameters) -> _FakeResult:
        self.executions.append((query, parameters))
        return self.results.pop(0)


class _FakeEngine:
    def __init__(self, results: list[_FakeResult]) -> None:
        self.connection = _FakeConnection(results)

    def connect(self) -> _FakeConnection:
        return self.connection


class _FailingConnection:
    def __enter__(self) -> "_FailingConnection":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def execute(self, query, parameters) -> None:
        raise DatabaseError("SELECT", parameters, Exception("failure"))


class _FailingEngine:
    def connect(self) -> _FailingConnection:
        return _FailingConnection()
