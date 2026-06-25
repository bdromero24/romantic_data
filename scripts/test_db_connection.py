"""Manual script to test the PostgreSQL connection."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from db.connection import test_connection
from logger.logger import log_critical_error


def main() -> None:
    """Print database connection status."""
    try:
        if test_connection():
            print("Database connection successful.")
            return

        print("Database connection failed.")
    except Exception as error:
        log_critical_error(
            error_type=type(error).__name__,
            error_message=str(error),
            module_name=__name__,
            function_name="main",
        )
        print("Database connection failed.")


if __name__ == "__main__":
    main()
