"""Database connection utilities."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DatabaseError, OperationalError, ProgrammingError


load_dotenv()


def _log_database_error(
    error_type: str,
    error: Exception,
    function_name: str,
) -> None:
    from logger.logger import log_critical_error

    log_critical_error(
        error_type=error_type,
        error_message=str(error),
        module_name=__name__,
        function_name=function_name,
        write_to_db=False,
    )


def get_database_url() -> str:
    """Return the PostgreSQL database URL from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    required_variables = {
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    }
    missing_variables = [
        name for name, value in required_variables.items() if not value
    ]

    if missing_variables:
        missing_text = ", ".join(missing_variables)
        raise ValueError(f"Missing database environment variables: {missing_text}")

    return (
        "postgresql+psycopg2://"
        f"{required_variables['POSTGRES_USER']}:"
        f"{required_variables['POSTGRES_PASSWORD']}@"
        f"{required_variables['POSTGRES_HOST']}:"
        f"{required_variables['POSTGRES_PORT']}/"
        f"{required_variables['POSTGRES_DB']}"
    )


def get_engine() -> Engine:
    """Create a SQLAlchemy engine."""
    return create_engine(get_database_url(), pool_pre_ping=True)


def test_connection() -> bool:
    """Return True when PostgreSQL accepts a simple query."""
    try:
        engine = get_engine()
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except ProgrammingError as error:
        _log_database_error("ProgrammingError", error, "test_connection")
    except OperationalError as error:
        _log_database_error("OperationalError", error, "test_connection")
    except DatabaseError as error:
        _log_database_error("DatabaseError", error, "test_connection")
    except Exception as error:
        _log_database_error(type(error).__name__, error, "test_connection")

    return False


def execute_schema(schema_path: str | Path = "db/schema.sql") -> None:
    """Execute the PostgreSQL schema file."""
    try:
        path = Path(schema_path)
        schema_sql = path.read_text(encoding="utf-8")
        engine = get_engine()
        with engine.begin() as connection:
            connection.execute(text(schema_sql))
    except ProgrammingError as error:
        _log_database_error("ProgrammingError", error, "execute_schema")
        raise
    except OperationalError as error:
        _log_database_error("OperationalError", error, "execute_schema")
        raise
    except DatabaseError as error:
        _log_database_error("DatabaseError", error, "execute_schema")
        raise
    except Exception as error:
        _log_database_error(type(error).__name__, error, "execute_schema")
        raise
