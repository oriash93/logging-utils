import logging
import os
from dataclasses import dataclass
from typing import TypeAlias

LogLevel: TypeAlias = int | str

DEFAULT_LOG_LEVEL: LogLevel = logging.INFO
DEFAULT_LOG_FORMAT: str = "%(asctime)s - %(name)s  - %(levelname)s [%(filename)s:%(lineno)d] - %(message)s"
DEFAULT_LOG_FILENAME: str = "app.log"


@dataclass
class LogFileConfig:
    """
    Configuration settings for the log file handler.

    Attributes:
        log_file_level (LogLevel | None): The logging level for file logging.
            If not set, it defaults to the logger's level.
        log_filename (str): Path to the log file. Defaults to "app.log".
        max_bytes (int): Maximum size (in bytes) before rotating the log file.
            Defaults to 1 MiB (1 * 1024 * 1024).
        backup_count (int): Number of backup files to keep after rotation.
            Defaults to 5.
    """

    log_file_level: LogLevel | None = None
    log_filename: str = DEFAULT_LOG_FILENAME
    max_bytes: int = 1 * 1024 * 1024
    backup_count: int = 5


def _get_timezone_converter(timezone: str):
    from datetime import datetime
    from zoneinfo import ZoneInfo

    return lambda *args: datetime.now(tz=ZoneInfo(timezone)).timetuple()


def setup_logger(
    name: str,
    log_level: LogLevel | None = None,
    log_format: str = DEFAULT_LOG_FORMAT,
    enable_log_file: bool = False,
    log_file_config: LogFileConfig = LogFileConfig(),
) -> logging.Logger:
    """
    Sets up a logger with customizable settings for both console and file logging.

    Args:
        name (str): Name of the logger.
        log_level (LogLevel | None): Logging level for the logger. If not set, defaults to
            the environment variable `LOG_LEVEL` or `logging.INFO`.
        log_format (str): The log message format. Defaults to `DEFAULT_LOG_FORMAT`.
        enable_log_file (bool): If True, enables file logging. Defaults to False.
        log_file_config (LogFileConfig): Configuration for file logging, including
            filename, file log level, max bytes per file, and backup count.

    Returns:
        logging.Logger: The configured logger instance.
    """
    if not log_level:
        log_level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    log_formatter = logging.Formatter(log_format)
    if TZ := os.getenv("TZ"):
        log_formatter.converter = _get_timezone_converter(TZ)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    if enable_log_file:
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            filename=log_file_config.log_filename,
            maxBytes=log_file_config.max_bytes,
            backupCount=log_file_config.backup_count,
        )
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_file_config.log_file_level or log_level)
        logger.addHandler(file_handler)

    return logger
