"""Unit tests for ETL loading."""

from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import DatabaseError

from db.queries import INSERT_MESSAGE_QUERY
from etl import load


def test_load_messages_inserts_transformed_records(monkeypatch) -> None:
    engine = _FakeEngine([1, 1])
    monkeypatch.setattr(load, "get_engine", lambda: engine)

    result = load.load_messages(
        [
            _message_record(sender="Alice"),
            _message_record(sender="Bob"),
        ]
    )

    assert result == {
        "received": 2,
        "inserted": 2,
        "skipped_duplicates": 0,
    }
    assert len(engine.connection.executions) == 2
    query, parameters = engine.connection.executions[0]
    assert query is INSERT_MESSAGE_QUERY
    assert parameters["sender"] == "Alice"


def test_load_messages_counts_duplicate_skips(monkeypatch) -> None:
    engine = _FakeEngine([1, 0])
    monkeypatch.setattr(load, "get_engine", lambda: engine)

    result = load.load_messages(
        [
            _message_record(sender="Alice"),
            _message_record(sender="Alice"),
        ]
    )

    assert result == {
        "received": 2,
        "inserted": 1,
        "skipped_duplicates": 1,
    }


def test_load_messages_requires_transformed_fields(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        load,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(KeyError, match="Missing transformed message fields"):
        load.load_messages([{"sender": "Alice"}])

    assert logged_errors == ["KeyError"]


def test_load_messages_rejects_empty_records(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(
        load,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(ValueError, match="No transformed message records"):
        load.load_messages([])

    assert logged_errors == ["ValueError"]


def test_load_messages_logs_and_reraises_database_errors(monkeypatch) -> None:
    logged_errors: list[str] = []
    monkeypatch.setattr(load, "get_engine", lambda: _FailingEngine())
    monkeypatch.setattr(
        load,
        "log_critical_error",
        lambda error_type, **kwargs: logged_errors.append(error_type),
    )

    with pytest.raises(DatabaseError):
        load.load_messages([_message_record(sender="Alice")])

    assert logged_errors == ["DatabaseError"]


def test_load_messages_from_artifact_loads_records_then_database(
    monkeypatch,
    tmp_path,
) -> None:
    records = [_message_record(sender="Alice")]
    monkeypatch.setattr(load, "load_messages", lambda loaded: {"received": len(loaded)})

    from etl import artifacts

    path = tmp_path / "records.parquet"
    artifacts.save_records(records, path)

    assert load.load_messages_from_artifact(path) == {"received": 1}


def _message_record(sender: str) -> dict:
    return {
        "sender": sender,
        "message": "Hola",
        "message_normalized": "hola",
        "timestamp": datetime(2026, 5, 29, 19, 30, tzinfo=timezone.utc),
        "source": "instagram",
    }


class _FakeResult:
    def __init__(self, rowcount: int) -> None:
        self.rowcount = rowcount


class _FakeConnection:
    def __init__(self, rowcounts: list[int]) -> None:
        self.rowcounts = rowcounts
        self.executions: list[tuple] = []

    def execute(self, query, parameters) -> _FakeResult:
        self.executions.append((query, parameters))
        return _FakeResult(self.rowcounts.pop(0))


class _FakeTransaction:
    def __init__(self, connection: _FakeConnection) -> None:
        self.connection = connection

    def __enter__(self) -> _FakeConnection:
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None


class _FakeEngine:
    def __init__(self, rowcounts: list[int]) -> None:
        self.connection = _FakeConnection(rowcounts)

    def begin(self) -> _FakeTransaction:
        return _FakeTransaction(self.connection)


class _FailingConnection:
    def execute(self, query, parameters) -> None:
        raise DatabaseError("INSERT", parameters, Exception("failure"))


class _FailingEngine:
    def begin(self) -> _FakeTransaction:
        return _FakeTransaction(_FailingConnection())
