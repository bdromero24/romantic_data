"""Manual script to initialize the PostgreSQL schema."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.connection import execute_schema
from logger.logger import log_critical_error


def main() -> None:
    """Create database tables and indexes."""
    try:
        execute_schema()
        print("Database schema initialized successfully.")
    except Exception as error:
        log_critical_error(
            error_type=type(error).__name__,
            error_message=str(error),
            module_name=__name__,
            function_name="main",
        )
        print("Database schema initialization failed.")


if __name__ == "__main__":
    main()
