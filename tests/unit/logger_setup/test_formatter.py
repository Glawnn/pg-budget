# test_formatter.py
import logging

import pytest

from pg_budget.logger_setup.formatter import SimpleFormatter


@pytest.fixture
def formatter():
    return SimpleFormatter()


def make_record(name="test_logger", level=logging.INFO, msg="Hello", exc_info=None):
    """Helper pour créer un LogRecord."""
    return logging.LogRecord(
        name=name,
        level=level,
        pathname=__file__,
        lineno=42,
        msg=msg,
        args=None,
        exc_info=exc_info,
    )


def test_format_simple_message(formatter):
    record = make_record(msg="Hello World", level=logging.INFO)
    output = formatter.format(record)

    assert "Hello World" in output
    assert "INFO" in output
    assert "test_logger" in output
    assert output.startswith("[")  # commence bien par un timestamp formaté


def test_format_level_alignment(formatter):
    record = make_record(level=logging.WARNING, msg="Something")
    output = formatter.format(record)

    # WARNING doit être justifié sur 8 caractères
    assert "WARNING " in output  # note l'espace à la fin


def test_format_different_logger_name(formatter):
    record = make_record(name="custom_logger", msg="Test message")
    output = formatter.format(record)

    assert "custom_logger" in output
    assert "Test message" in output
