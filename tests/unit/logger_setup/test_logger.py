# test_logger.py
import logging

from pg_budget.logger_setup import logger


class TestLoggerSetup:
    def test_logger_name_and_level(self):
        assert isinstance(logger, logging.Logger)
        assert logger.name == "pg_budget"
        assert logger.level == logging.DEBUG
