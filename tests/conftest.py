import pytest
import locale
from PySide6.QtCore import QLocale


def pytest_addoption(parser):
    parser.addoption("--delay", action="store", default=0, type=int, help="Delay (in milliseconds) for E2E tests")


@pytest.fixture
def delay(request):
    """Fixture returning the delay from CLI"""
    return request.config.getoption("--delay")


@pytest.fixture
def qbot_delay(qtbot, delay):
    """Fixture: wait with qtbot.wait using CLI delay"""

    def _wait(ms=None):
        qtbot.wait(ms or delay)

    return _wait


@pytest.fixture(autouse=True)
def force_french_locale():
    locale.setlocale(locale.LC_NUMERIC, "fr_FR.UTF-8")
    QLocale.setDefault(QLocale(QLocale.French, QLocale.France))
