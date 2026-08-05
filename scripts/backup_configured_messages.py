"""Backup manually configured romantic message IDs from PostgreSQL."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import bindparam, text
from sqlalchemy.exc import DatabaseError, ProgrammingError


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.content_config import ROMANTIC_CONTENT
from app.content_references import extract_configured_message_references
from db.connection import get_engine
from logger.logger import log_critical_error


BACKUP_DIR = PROJECT_ROOT / "data" / "backups"
BACKUP_FIELDS = (
    "config_path",
    "message_id",
    "source",
    "sender",
    "message",
    "message_normalized",
    "timestamp",
    "created_at",
    "message_key",
    "found_in_database",
)


def main() -> None:
    """Create CSV and JSON backups for configured message IDs."""
    try:
        references = extract_configured_message_references(ROMANTIC_CONTENT)
        rows_by_id = _fetch_messages_by_id(
            [
                reference.message_id
                for reference in references
                if reference.message_id is not None
            ]
        )
        backup_rows = [_build_backup_row(reference, rows_by_id) for reference in references]
        csv_path, json_path = _write_backups(backup_rows)

        found_count = sum(1 for row in backup_rows if row["found_in_database"])
        print(f"Total IDs configurados encontrados: {len(references)}")
        print(f"Total encontrados en DB: {found_count}")
        print(f"Total no encontrados: {len(references) - found_count}")
        print(f"Backup generado en: {csv_path}")
        print(f"Backup generado en: {json_path}")
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


def _fetch_messages_by_id(message_ids: list[int]) -> dict[int, dict[str, Any]]:
    if not message_ids:
        return {}

    engine = get_engine()
    available_columns = _get_message_columns(engine)
    created_at_select = (
        "created_at" if "created_at" in available_columns else "NULL AS created_at"
    )
    message_key_select = (
        "message_key"
        if "message_key" in available_columns
        else "NULL AS message_key"
    )
    query = text(
        f"""
        SELECT id,
               source,
               sender,
               message,
               message_normalized,
               timestamp,
               {created_at_select},
               {message_key_select}
        FROM messages
        WHERE id IN :message_ids
        """
    ).bindparams(bindparam("message_ids", expanding=True))
    with engine.connect() as connection:
        result = connection.execute(query, {"message_ids": message_ids})
        return {
            int(row._mapping["id"]): dict(row._mapping)
            for row in result.fetchall()
        }


def _get_message_columns(engine: Any) -> set[str]:
    query = text(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = :table_name
        """
    )
    with engine.connect() as connection:
        result = connection.execute(query, {"table_name": "messages"})
        return {str(row._mapping["column_name"]) for row in result.fetchall()}


def _build_backup_row(
    reference: Any,
    rows_by_id: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    row = rows_by_id.get(reference.message_id)
    if row is None:
        return {
            "config_path": reference.config_path,
            "message_id": reference.message_id,
            "source": None,
            "sender": None,
            "message": None,
            "message_normalized": None,
            "timestamp": None,
            "created_at": None,
            "message_key": None,
            "found_in_database": False,
        }

    return {
        "config_path": reference.config_path,
        "message_id": reference.message_id,
        "source": row.get("source"),
        "sender": row.get("sender"),
        "message": row.get("message"),
        "message_normalized": row.get("message_normalized"),
        "timestamp": _serialize_datetime(row.get("timestamp")),
        "created_at": _serialize_datetime(row.get("created_at")),
        "message_key": row.get("message_key"),
        "found_in_database": True,
    }


def _write_backups(rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = BACKUP_DIR / f"configured_messages_backup_{suffix}.csv"
    json_path = BACKUP_DIR / f"configured_messages_backup_{suffix}.json"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=BACKUP_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return csv_path, json_path


def _serialize_datetime(value: Any) -> str | None:
    if value is None:
        return None

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return str(value)


def _log_script_error(error_type: str, error: Exception) -> None:
    log_critical_error(
        error_type=error_type,
        error_message=str(error),
        module_name=__name__,
        function_name="main",
    )


if __name__ == "__main__":
    main()
