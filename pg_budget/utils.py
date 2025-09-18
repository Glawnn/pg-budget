"""utils"""

import os
import sys
from importlib.metadata import version

__version__ = "v" + version("pg-budget")


def resource_path(relative_path):
    """open file path dev / build"""
    try:
        base_path = sys._MEIPASS  # pylint: disable=protected-access
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
