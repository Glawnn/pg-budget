from datetime import date, datetime
import os
import sys

import pytest
from PySide6.QtCore import QDate, QLocale

import pg_budget.utils as utils


class TestUtils:
    def test_version_string(self, mocker):
        mocker.patch("importlib.metadata.version", return_value="1.2.3")
        import importlib
        import pg_budget.utils as utils_reload

        importlib.reload(utils_reload)

        assert utils_reload.__version__ == "v1.2.3"

    def test_resource_path_with_meipass(self, mocker):
        mocker.patch("sys._MEIPASS", "/tmp/fake_meipass", create=True)
        path = utils.resource_path("file.txt")
        assert path == os.path.join("/tmp/fake_meipass", "file.txt")

    def test_resource_path_without_meipass(self):
        if hasattr(sys, "_MEIPASS"):
            del sys._MEIPASS
        path = utils.resource_path("file.txt")
        expected = os.path.join(os.path.abspath("."), "file.txt")
        assert path == expected


class TestDateFormatter:
    @pytest.mark.parametrize(
        "input_value, expected_year, expected_month, expected_day",
        [
            pytest.param("2025-10-25", 2025, 10, 25, id="string_dash"),
            pytest.param("2025/10/25", 2025, 10, 25, id="string_slash"),
            pytest.param(datetime(2025, 10, 25), 2025, 10, 25, id="datetime"),
            pytest.param(date(2025, 10, 25), 2025, 10, 25, id="date"),
            pytest.param(QDate(2025, 10, 25), 2025, 10, 25, id="qdate"),
        ],
    )
    def test_to_qdate_valid(self, input_value, expected_year, expected_month, expected_day):
        qd = utils.DateFormatter.to_qdate(input_value)
        assert isinstance(qd, QDate)
        assert qd.year() == expected_year
        assert qd.month() == expected_month
        assert qd.day() == expected_day

    @pytest.mark.parametrize(
        "invalid_input",
        [
            pytest.param("25-10-2025", id="invalid_string"),
            pytest.param(12345, id="invalid_int"),
            pytest.param(None, id="invalid_none"),
            pytest.param([], id="invalid_list"),
            pytest.param({}, id="invalid_dict"),
        ],
    )
    def test_to_qdate_invalid(self, invalid_input):
        with pytest.raises((ValueError, TypeError)):
            utils.DateFormatter.to_qdate(invalid_input)

    @pytest.mark.parametrize(
        "locale, expected",
        [
            pytest.param(QLocale(QLocale.French, QLocale.France), "25/10/2025", id="fr"),
            pytest.param(QLocale(QLocale.English, QLocale.UnitedStates), "10/25/25", id="en"),
        ],
    )
    def test_format_locales(self, locale, expected):
        dt = datetime(2025, 10, 25)
        formatted = utils.DateFormatter.format(dt, locale=locale)
        assert isinstance(formatted, str)
        assert formatted == expected
