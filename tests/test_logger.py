import logging.handlers
import unittest
from unittest.mock import patch, MagicMock
import logging
from typing import Any
import os
from src import DEFAULT_LOG_FORMAT, setup_logger, LogFileConfig, DEFAULT_LOG_LEVEL


class TestSetupLogger(unittest.TestCase):
    def setUp(self):
        self.test_logger_name = "test_logger"

    def tearDown(self):
        if self.test_logger:
            self.test_logger.handlers.clear()

    def test_logger_default_values(self):
        self.test_logger = setup_logger(name=self.test_logger_name)

        self.assertEqual(self.test_logger.name, self.test_logger_name)
        self.assertEqual(self.test_logger.level, DEFAULT_LOG_LEVEL)

    def test_logger_name_and_level(self):
        log_level = logging.DEBUG
        self.test_logger = setup_logger(name=self.test_logger_name, log_level=log_level)

        self.assertEqual(self.test_logger.name, self.test_logger_name)
        self.assertEqual(self.test_logger.level, log_level)

    def test_logger_has_stream_handler(self):
        log_level = logging.WARNING
        self.test_logger = setup_logger(name=self.test_logger_name, log_level=log_level)

        stream_handler = next(
            handler for handler in self.test_logger.handlers if isinstance(handler, logging.StreamHandler)
        )
        self.assertIsNotNone(stream_handler)
        self.assertIsNotNone(stream_handler.formatter)
        self.assertEqual(stream_handler.level, log_level)

    def test_logger_disable_log_file_true(self):
        self.test_logger = setup_logger(name=self.test_logger_name, disable_log_file=True)

        has_file_handler = any(
            isinstance(handler, logging.handlers.RotatingFileHandler) for handler in self.test_logger.handlers
        )
        self.assertFalse(has_file_handler)

    def test_logger_disable_log_file_false(self):
        self.test_logger = setup_logger(name=self.test_logger_name, disable_log_file=False)

        file_handler = next(
            handler
            for handler in self.test_logger.handlers
            if isinstance(handler, logging.handlers.RotatingFileHandler)
        )
        self.assertIsNotNone(file_handler)
        self.assertIsNotNone(file_handler.formatter)
        self.assertEqual(file_handler.level, DEFAULT_LOG_LEVEL)

    def test_logger_disable_log_file_false_params(self):
        self.test_logger = setup_logger(
            name=self.test_logger_name,
            disable_log_file=False,
            log_file_config=LogFileConfig(file_path="test.log", max_bytes=3_000, backup_count=1),
        )

        file_handler = next(
            handler
            for handler in self.test_logger.handlers
            if isinstance(handler, logging.handlers.RotatingFileHandler)
        )
        self.assertIsNotNone(file_handler)
        self.assertIsNotNone(file_handler.formatter)
        self.assertIn("test.log", file_handler.baseFilename)
        self.assertEqual(file_handler.maxBytes, 3_000)
        self.assertEqual(file_handler.backupCount, 1)
        self.assertEqual(file_handler.level, DEFAULT_LOG_LEVEL)

    def test_log_formatter_keeps_default_converter_when_no_timezone_set(self):
        import time

        self.test_logger = setup_logger(name=self.test_logger_name)
        for handler in self.test_logger.handlers:
            formatter = handler.formatter
            self.assertEqual(formatter.converter, time.localtime)

    @patch.dict(os.environ, {"TZ": "Asia/Jerusalem"})
    def test_log_formatter_timezone_config_set_correctly(self):
        import time

        self.test_logger = setup_logger(name=self.test_logger_name)
        for handler in self.test_logger.handlers:
            formatter = handler.formatter
            self.assertNotEqual(formatter.converter, time.localtime)


if __name__ == "__main__":
    unittest.main()
