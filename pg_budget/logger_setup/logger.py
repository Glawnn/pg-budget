"""logger for app"""

import logging
import sys
from logging.handlers import RotatingFileHandler

from pg_budget.logger_setup.config import (
    LOG_DIR,
    LOG_DIR_DEV,
    LOG_FILE,
    LOG_FILE_DEV,
    LOG_LEVEL_CONSOLE,
    LOG_LEVEL_FILE,
    LOGGER_NAME,
)

from .formatter import SimpleFormatter

# Detect log path
if getattr(sys, "frozen", False):
    log_dir = LOG_DIR
    log_file = LOG_FILE
else:
    log_dir = LOG_DIR_DEV
    log_file = LOG_FILE_DEV

log_dir.mkdir(parents=True, exist_ok=True)


logger: logging.Logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

# File handler
file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=20, encoding="utf-8")
file_handler.setLevel(getattr(logging, LOG_LEVEL_FILE))
file_handler.setFormatter(SimpleFormatter())
logger.addHandler(file_handler)

# Console handler (dev only)
if getattr(sys, "frozen", False) is False:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL_CONSOLE))
    console_handler.setFormatter(SimpleFormatter())
    logger.addHandler(console_handler)
