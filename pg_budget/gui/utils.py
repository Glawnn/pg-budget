"""utils for gui"""

from pg_budget.gui import logger


def safe_callback(func):
    """
    Wrap a Qt callback function so that any exception is logged
    without crashing the application.
    """

    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # pylint: disable=broad-exception-caught
            logger.exception("Exception occurred in callback '%s'", func.__name__)
            return None

    return wrapped
