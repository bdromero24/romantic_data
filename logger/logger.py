"""Centralized application logger."""

import logging

from logger.config import DEFAULT_SEVERITY, LOG_FILE_PATH, LOG_FORMAT


LOGGER_NAME = "chat_analysis_errors"


def get_file_logger() -> logging.Logger:
    """Return a configured file logger."""
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_logger = logging.getLogger(LOGGER_NAME)
    file_logger.setLevel(logging.CRITICAL)
    file_logger.propagate = False

    current_path = str(LOG_FILE_PATH.resolve())
    for handler in list(file_logger.handlers):
        if getattr(handler, "baseFilename", None) != current_path:
            file_logger.removeHandler(handler)
            handler.close()

    if not file_logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
        file_handler.setLevel(logging.CRITICAL)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        file_logger.addHandler(file_handler)

    return file_logger


def _write_error_to_database(
    error_type: str,
    error_message: str,
    module_name: str | None,
    function_name: str | None,
) -> None:
    from db.connection import get_engine
    from db.queries import INSERT_LOG_QUERY

    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(
            INSERT_LOG_QUERY,
            {
                "error_type": error_type,
                "error_message": error_message,
                "module_name": module_name,
                "function_name": function_name,
                "severity": DEFAULT_SEVERITY,
            },
        )


def log_critical_error(
    error_type: str,
    error_message: str,
    module_name: str | None = None,
    function_name: str | None = None,
    write_to_db: bool = True,
) -> None:
    """Write critical errors to file and optionally to PostgreSQL."""
    file_logger = get_file_logger()
    log_message = (
        f"error_type={error_type} | "
        f"module_name={module_name} | "
        f"function_name={function_name} | "
        f"message={error_message}"
    )
    file_logger.critical(log_message)

    if not write_to_db:
        return

    try:
        _write_error_to_database(
            error_type=error_type,
            error_message=error_message,
            module_name=module_name,
            function_name=function_name,
        )
    except Exception as error:
        file_logger.critical(
            "error_type=DatabaseLoggingError | "
            f"module_name={__name__} | "
            "function_name=log_critical_error | "
            f"message={error}"
        )
