import logging
import logging.handlers
import os
import time
import unittest
from unittest.mock import patch

from src import LogFileConfig, setup_logger


class TestLoggingUtils(unittest.TestCase):
    def setUp(self):
        self.test_logger_name = "test_logger"
        self.test_log_level = logging.DEBUG
        self.default_log_level = logging.INFO

    def tearDown(self):
        if self.test_logger:
            self.test_logger.handlers.clear()
        logging.shutdown()

    def test_setup_logger_with_default_parameters(self):
        self.test_logger = setup_logger(name=self.test_logger_name)

        self.assertEqual(self.test_logger.name, self.test_logger_name)
        self.assertEqual(self.test_logger.level, self.default_log_level)

    def test_setup_logger_with_name_and_log_level(self):
        self.test_logger = setup_logger(name=self.test_logger_name, log_level=self.test_log_level)

        self.assertEqual(self.test_logger.name, self.test_logger_name)
        self.assertEqual(self.test_logger.level, self.test_log_level)

    def test_setup_logger_set_log_level_via_env_variable(self):
        with patch.dict(os.environ, {"LOG_LEVEL": str(self.test_log_level)}):
            self.test_logger = setup_logger(name=self.test_logger_name, log_level=self.test_log_level)

        self.assertEqual(self.test_logger.name, self.test_logger_name)
        self.assertEqual(self.test_logger.level, self.test_log_level)

    def test_setup_logger_has_stream_handler(self):
        self.test_logger = setup_logger(name=self.test_logger_name, log_level=self.test_log_level)

        stream_handler: logging.StreamHandler = self._find_handler_by_type(logging.StreamHandler)  # type: ignore
        self.assertIsNotNone(stream_handler)
        self.assertIsNotNone(stream_handler.formatter)
        self.assertEqual(stream_handler.level, self.test_log_level)

    def test_setup_logger_disable_log_file_true_no_file_handler(self):
        self.test_logger = setup_logger(name=self.test_logger_name, disable_log_file=True)

        file_handler = self._find_handler_by_type(logging.handlers.RotatingFileHandler)
        self.assertIsNone(file_handler)

    def test_setup_logger_file_handler_with_default_config(self):
        self.test_logger = setup_logger(name=self.test_logger_name, disable_log_file=False)

        file_handler: logging.handlers.RotatingFileHandler = self._find_handler_by_type(logging.handlers.RotatingFileHandler)  # type: ignore
        self.assertIsNotNone(file_handler)
        self.assertIsNotNone(file_handler.formatter)
        self.assertIn("app.log", file_handler.baseFilename)
        self.assertEqual(file_handler.level, self.default_log_level)
        self.assertEqual(file_handler.maxBytes, 1 * 1024 * 1024)
        self.assertEqual(file_handler.backupCount, 5)

    def test_setup_logger_file_handler_with_custom_config(self):
        self.test_logger = setup_logger(
            name=self.test_logger_name,
            disable_log_file=False,
            log_file_config=LogFileConfig(
                log_filename="test.log", max_bytes=3_000, backup_count=1, log_file_level=self.test_log_level
            ),
        )

        file_handler: logging.handlers.RotatingFileHandler = self._find_handler_by_type(logging.handlers.RotatingFileHandler)  # type: ignore
        self.assertIsNotNone(file_handler)
        self.assertIsNotNone(file_handler.formatter)
        self.assertIn("test.log", file_handler.baseFilename)
        self.assertEqual(file_handler.level, self.test_log_level)
        self.assertEqual(file_handler.maxBytes, 3_000)
        self.assertEqual(file_handler.backupCount, 1)

    def test_setup_logger_log_formatter_keeps_default_converter_when_no_timezone_set(self):
        self.test_logger = setup_logger(name=self.test_logger_name)

        for handler in self.test_logger.handlers:
            self.assertEqual(handler.formatter.converter, time.localtime)  # type: ignore

    def test_setup_logger_log_formatter_sets_timezone_converter_when_timezone_set(self):
        with patch.dict(os.environ, {"TZ": "Asia/Jerusalem"}):
            self.test_logger = setup_logger(name=self.test_logger_name)

        for handler in self.test_logger.handlers:
            self.assertNotEqual(handler.formatter.converter, time.localtime)  # type: ignore

    def _find_handler_by_type(self, handler_type: type) -> logging.Handler | None:
        for handler in self.test_logger.handlers:
            if isinstance(handler, handler_type):
                return handler
        return None


if __name__ == "__main__":
    unittest.main()
