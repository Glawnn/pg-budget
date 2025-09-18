"""Formatters for logging"""

import logging


class SimpleFormatter(logging.Formatter):
    """Simple formatter with time, level, logger name"""

    def format(self, record):
        time = self.formatTime(record, "%H:%M:%S")
        level = record.levelname.ljust(8)
        name = record.name
        return f"[{time}] {level} {name}: {record.getMessage()}"
