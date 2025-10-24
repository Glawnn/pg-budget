"""Formatters for logging"""

import logging
import traceback


class SimpleFormatter(logging.Formatter):
    """Simple formatter with time, level, logger name"""

    def format(self, record):
        time = self.formatTime(record, "%H:%M:%S")
        level = record.levelname.ljust(8)
        name = record.name
        msg = record.getMessage()
        if record.exc_info:
            exc_text = "".join(traceback.format_exception(*record.exc_info))
            msg = f"{msg}\n{exc_text}"
        return f"[{time}] {level} {name}: {msg}"
