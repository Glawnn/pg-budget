"""Entry point"""

import sys
from PySide6.QtWidgets import QApplication

from pg_budget.gui.windows import MainWindow
from pg_budget.logger_setup import logger


def main():
    """main entry point"""

    logger.info("Starting PG-Budget application")
    exit_code = 0
    try:
        app = QApplication(sys.argv)
        logger.debug("QApplication initialized")

        window = MainWindow()
        logger.info("Main window created")

        window.show()
        logger.info("Main window shown")

        exit_code = app.exec()
        logger.info("Application event loop exited")

    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C).")
    except Exception:  # pylint: disable=broad-exception-caught
        logger.error("Exception occurred in main entry point", exc_info=True)
        exit_code = 1
    finally:
        logger.info("Application exited with code %d", exit_code)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
