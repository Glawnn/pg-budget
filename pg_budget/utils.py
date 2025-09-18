"""utils"""

import os
import sys


def resource_path(relative_path):
    """open file path dev / build"""
    try:
        base_path = sys._MEIPASS  # pylint: disable=protected-access
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
