"""Export message_id to message_key mapping for content_config.py."""

from __future__ import annotations

import csv
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
MAPPING_FIELDS = (
    "config_path",
    "message_id",
    "message_key",
    "sender",
    "message",
    "timestamp",
)


def main() -> None:
    """Write configured message key mapping to a CSV file."""
    try:
        references = extract_configured_message_references(ROMANTIC_CONTENT)
        rows_by_id = _fetch_messages_by_id(
            [
                reference.message_id
                for reference in references
                if reference.message_id is not None
            ]
        )
        mapping_rows = [
            _build_mapping_row(reference, rows_by_id)
            for reference in references
            if reference.message_id is not None
        ]
        output_path = _write_mapping(mapping_rows)
        print(f"Total IDs configurados encontrados: {len(mapping_rows)}")
        print(f"Mapping generado en: {output_path}")
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

    query = text(
        """
        SELECT id, sender, message, timestamp, message_key
        FROM messages
        WHERE id IN :message_ids
        """
    ).bindparams(bindparam("message_ids", expanding=True))
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(query, {"message_ids": message_ids})
        return {
            int(row._mapping["id"]): dict(row._mapping)
            for row in result.fetchall()
        }


def _build_mapping_row(
    reference: Any,
    rows_by_id: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    row = rows_by_id.get(reference.message_id, {})
    timestamp = row.get("timestamp")
    return {
        "config_path": reference.config_path,
        "message_id": reference.message_id,
        "message_key": row.get("message_key"),
        "sender": row.get("sender"),
        "message": row.get("message"),
        "timestamp": timestamp.isoformat()
        if hasattr(timestamp, "isoformat")
        else timestamp,
    }


def _write_mapping(rows: list[dict[str, Any]]) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = BACKUP_DIR / f"content_config_message_key_mapping_{suffix}.csv"

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=MAPPING_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def _log_script_error(error_type: str, error: Exception) -> None:
    log_critical_error(
        error_type=error_type,
        error_message=str(error),
        module_name=__name__,
        function_name="main",
    )


if __name__ == "__main__":
    main()
