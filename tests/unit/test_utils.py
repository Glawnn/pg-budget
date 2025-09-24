import os
import sys

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
