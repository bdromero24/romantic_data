"""Unit tests for database connection utilities.

Run with:
    pytest tests/
"""

from sqlalchemy.exc import OperationalError

from db import connection as db_connection


def test_get_database_url_returns_string(monkeypatch) -> None:
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg2://user:password@localhost:5432/database",
    )

    database_url = db_connection.get_database_url()

    assert isinstance(database_url, str)
    assert database_url.startswith("postgresql+psycopg2://")


def test_test_connection_returns_boolean(monkeypatch) -> None:
    monkeypatch.setattr(db_connection, "get_engine", lambda: _FakeEngine())

    result = db_connection.test_connection()

    assert isinstance(result, bool)
    assert result is True


def test_database_connection_errors_are_handled(monkeypatch) -> None:
    def raise_operational_error() -> None:
        raise OperationalError("SELECT 1", {}, Exception("failure"))

    monkeypatch.setattr(db_connection, "get_engine", raise_operational_error)
    monkeypatch.setattr(db_connection, "_log_database_error", lambda *args: None)

    result = db_connection.test_connection()

    assert result is False


class _FakeConnection:
    def __enter__(self) -> "_FakeConnection":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None

    def execute(self, query) -> None:
        return None


class _FakeEngine:
    def connect(self) -> _FakeConnection:
        return _FakeConnection()
