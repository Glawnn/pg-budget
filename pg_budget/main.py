"""Entry point"""
import sys

from pg_budget.logger_setup import logger
from pg_budget.utils import __version__


def main():
    """main entry point"""
    logger.info("=" * 60)
    logger.info("Starting PG-Budget application %s", __version__)
    logger.info("=" * 60)

    from PySide6.QtWidgets import QApplication

    from pg_budget.gui.windows import MainWindow

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
        exit_code = 0
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("Exception occurred in main entry point")
        exit_code = 1
    finally:
        logger.info("=" * 60)
        logger.info("Application exited with code %d", exit_code)
        logger.info("=" * 60)

        sys.exit(exit_code)


if __name__ == "__main__":
    main()
