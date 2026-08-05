"""Backfill deterministic message keys for existing messages."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import DatabaseError, ProgrammingError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.connection import get_engine
from etl.message_key import build_message_key
from logger.logger import log_critical_error


SELECT_MISSING_KEYS_QUERY = text(
    """
    SELECT id, source, sender, message_normalized, timestamp
    FROM messages
    WHERE message_key IS NULL
    ORDER BY id ASC
    """
)

UPDATE_MESSAGE_KEY_QUERY = text(
    """
    UPDATE messages
    SET message_key = :message_key
    WHERE id = :message_id
      AND message_key IS NULL
    """
)

DUPLICATE_MESSAGE_KEYS_QUERY = text(
    """
    SELECT message_key, COUNT(*) AS duplicate_count
    FROM messages
    WHERE message_key IS NOT NULL
    GROUP BY message_key
    HAVING COUNT(*) > 1
    ORDER BY duplicate_count DESC, message_key ASC
    """
)

CREATE_UNIQUE_INDEX_QUERY = text(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS ux_messages_message_key
    ON messages (message_key)
    """
)


def main() -> None:
    """Backfill message_key and create the unique index when safe."""
    try:
        engine = get_engine()
        with engine.begin() as connection:
            rows = [
                dict(row._mapping)
                for row in connection.execute(SELECT_MISSING_KEYS_QUERY)
            ]
            updated_count = 0
            for row in rows:
                result = connection.execute(
                    UPDATE_MESSAGE_KEY_QUERY,
                    {
                        "message_id": row["id"],
                        "message_key": build_message_key(row),
                    },
                )
                updated_count += max(result.rowcount or 0, 0)

            duplicate_rows = [
                dict(row._mapping)
                for row in connection.execute(DUPLICATE_MESSAGE_KEYS_QUERY)
            ]
            if not duplicate_rows:
                connection.execute(CREATE_UNIQUE_INDEX_QUERY)

        print(f"Registros sin message_key: {len(rows)}")
        print(f"Registros actualizados: {updated_count}")
        print(f"Duplicados detectados: {len(duplicate_rows)}")
        if duplicate_rows:
            print("Indice unico no creado: hay message_key duplicados.")
        else:
            print("Indice unico validado/creado: ux_messages_message_key")
    except ProgrammingError as error:
        _log_script_error("ProgrammingError", error)
        raise
    except DatabaseError as error:
        _log_script_error("DatabaseError", error)
        raise
    except ConnectionError as error:
        _log_script_error("ConnectionError", error)
        raise
    except Exception as error:
        _log_script_error(type(error).__name__, error)
        raise


def _log_script_error(error_type: str, error: Exception) -> None:
    log_critical_error(
        error_type=error_type,
        error_message=str(error),
        module_name=__name__,
        function_name="main",
    )


if __name__ == "__main__":
    main()
