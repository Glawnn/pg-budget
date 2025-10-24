"""config for logger"""

from pathlib import Path

from pg_budget.utils import __version__

LOG_DIR = Path.home() / ".pg_budget" / "logs"
LOG_DIR_DEV = Path(__file__).parent.parent.parent / "logs"


LOG_FILE = LOG_DIR / f"pg_budget_{__version__}.log"
LOG_FILE_DEV = LOG_DIR_DEV / f"pg_budget_{__version__}.log"

LOG_LEVEL_FILE = "INFO"
LOG_LEVEL_CONSOLE = "DEBUG"
LOGGER_NAME = "pg_budget"
