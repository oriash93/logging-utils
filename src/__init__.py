import logging
import os
import sys
from dataclasses import dataclass

from typing_extensions import TypeAlias

if sys.version_info >= (3, 10):
    LogLevel: TypeAlias = int | str
else:
    from typing import Union

    LogLevel: TypeAlias = Union[int, str]


DEFAULT_LOG_LEVEL: LogLevel = os.getenv("LOG_LEVEL", logging.INFO)
DEFAULT_LOG_FORMAT: str = "%(asctime)s - %(name)s  - %(levelname)s [%(filename)s:%(lineno)d] - %(message)s"


@dataclass
class LogFileConfig:
    file_path: str = "app.log"
    max_bytes: int = 1 * 1024 * 1024  # 1 MiB
    backup_count: int = 5


def setup_logger(
    name: str,
    log_level: LogLevel = DEFAULT_LOG_LEVEL,
    log_format: str = DEFAULT_LOG_FORMAT,
    disable_log_file: bool = False,
    log_file_config: LogFileConfig = LogFileConfig(),
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    log_formatter = logging.Formatter(log_format)

    if TZ := os.getenv("TZ"):
        from datetime import datetime
        from zoneinfo import ZoneInfo

        TZ_CONVERTER = lambda *args: datetime.now(tz=ZoneInfo(TZ)).timetuple()  # type: ignore
        log_formatter.converter = TZ_CONVERTER

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    if not disable_log_file:
        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(
            filename=log_file_config.file_path,
            maxBytes=log_file_config.max_bytes,
            backupCount=log_file_config.backup_count,
        )
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

    return logger
