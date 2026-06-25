"""Unit tests for centralized logger."""

from logger import logger as app_logger


def test_logger_writes_to_file(tmp_path, monkeypatch) -> None:
    log_file = tmp_path / "errors.txt"
    monkeypatch.setattr(app_logger, "LOG_FILE_PATH", log_file)

    file_logger = app_logger.get_file_logger()
    file_logger.critical("test critical error")

    assert log_file.exists()
    assert "test critical error" in log_file.read_text(encoding="utf-8")


def test_log_critical_error_does_not_crash_if_database_logging_fails(
    tmp_path,
    monkeypatch,
) -> None:
    log_file = tmp_path / "errors.txt"
    monkeypatch.setattr(app_logger, "LOG_FILE_PATH", log_file)

    def raise_database_error(*args, **kwargs) -> None:
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(
        app_logger,
        "_write_error_to_database",
        raise_database_error,
    )

    app_logger.log_critical_error(
        error_type="RuntimeError",
        error_message="failure",
        module_name="tests",
        function_name="test",
    )

    log_content = log_file.read_text(encoding="utf-8")
    assert "RuntimeError" in log_content
    assert "DatabaseLoggingError" in log_content


def test_log_file_is_created(tmp_path, monkeypatch) -> None:
    log_file = tmp_path / "nested" / "errors.txt"
    monkeypatch.setattr(app_logger, "LOG_FILE_PATH", log_file)

    app_logger.log_critical_error(
        error_type="ValueError",
        error_message="created",
        write_to_db=False,
    )

    assert log_file.exists()
