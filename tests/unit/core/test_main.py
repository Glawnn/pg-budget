import pg_budget.main as entry


class FakeApp:
    def __init__(self, *args, **kwargs):
        self._exec_called = False

    def exec(self):
        self._exec_called = True
        return 123  # fake exit code


class FakeWindow:
    def __init__(self):
        self._shown = False

    def show(self):
        self._shown = True


class TestEntryPoint:
    def test_main_normal_run(self, mocker):
        mocker.patch("PySide6.QtWidgets.QApplication", return_value=FakeApp())
        mocker.patch("pg_budget.gui.windows.MainWindow", return_value=FakeWindow())
        mock_sys_exit = mocker.patch("pg_budget.main.sys.exit")

        entry.main()

        mock_sys_exit.assert_called_once_with(123)

    def test_main_keyboard_interrupt(self, mocker):
        fake_app = FakeApp()
        mocker.patch("PySide6.QtWidgets.QApplication", return_value=fake_app)
        mocker.patch("pg_budget.gui.windows.MainWindow", side_effect=KeyboardInterrupt)
        mock_sys_exit = mocker.patch("pg_budget.main.sys.exit")

        entry.main()

        mock_sys_exit.assert_called_once_with(0)

    def test_main_generic_exception(self, mocker):
        fake_app = FakeApp()
        mocker.patch("PySide6.QtWidgets.QApplication", return_value=fake_app)
        mocker.patch("pg_budget.gui.windows.MainWindow", side_effect=RuntimeError("boom"))
        mock_sys_exit = mocker.patch("pg_budget.main.sys.exit")

        entry.main()

        mock_sys_exit.assert_called_once_with(1)
