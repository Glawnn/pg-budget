"""utils"""

import os
import sys
from datetime import date, datetime
from importlib.metadata import version

from PySide6.QtCore import QDate, QLocale

__version__ = "v" + version("pg-budget")


def resource_path(relative_path):
    """open file path dev / build"""
    try:
        base_path = sys._MEIPASS  # pylint: disable=protected-access
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DateFormatter:
    """date formatter utility"""

    @staticmethod
    def to_qdate(date_input) -> QDate:
        """
        Convert various date formats to QDate.
        """
        if isinstance(date_input, QDate):
            return date_input

        if isinstance(date_input, (datetime, date)):
            return QDate(date_input.year, date_input.month, date_input.day)

        if isinstance(date_input, str):
            fmt = "%Y-%m-%d" if "-" in date_input else "%Y/%m/%d"
            try:
                dt = datetime.strptime(date_input, fmt)
                return QDate(dt.year, dt.month, dt.day)
            except ValueError as err:
                raise ValueError(f"String date format should be YYYY-MM-DD or YYYY/MM/DD, got: {date_input}") from err

        raise TypeError(f"Unsupported date type: {type(date_input)}")

    @staticmethod
    def format(date_input, format_type=QLocale.ShortFormat, locale: QLocale | None = None) -> str:
        loc = locale or QLocale.system()
        qdate = DateFormatter.to_qdate(date_input)
        return loc.toString(qdate, format_type)
