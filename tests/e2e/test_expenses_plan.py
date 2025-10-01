import pytest
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QDialog, QPushButton, QApplication, QMessageBox

from pg_budget.gui.windows.main_window import MainWindow
from tests.e2e.utils import absent_in_table, get_row_in_table, present_in_table


@pytest.mark.usefixtures("qtbot")
class TestCreateExpensesPlan:
    @pytest.fixture(autouse=True)
    def setup(self, qtbot, qbot_delay):
        self.main_window = MainWindow()
        qtbot.addWidget(self.main_window)
        self.main_window.show()
        qbot_delay()

        yield

        self.main_window.close()

    def test_create_new_expenses_plan(self, make_db, qbot_delay, qtbot):
        make_db(activate=True)

        def handle_dialog():
            dialogs = self.main_window.findChildren(QDialog)
            assert dialogs, "Aucun QDialog ouvert"
            dialog = dialogs[-1]
            assert dialog.windowTitle() == "Create Expenses Plan"

            dialog.name_input.clear()
            qtbot.keyClicks(dialog.name_input, "fake_name")
            QApplication.processEvents()
            qbot_delay()

            dialog.amount_input.lineEdit().clear()
            qtbot.keyClicks(dialog.amount_input.lineEdit(), "123,45")
            QApplication.processEvents()
            qbot_delay()

            assert dialog.name_input.text() == "fake_name"

            save_btn = next(btn for btn in dialog.findChildren(QPushButton) if btn.text() == "Save")

            qtbot.mouseClick(save_btn, Qt.LeftButton)
            qbot_delay()

        file_action = next(a for a in self.main_window.menuBar().actions() if a.text() == "Actions")
        add_expenses_plan_action = next(a for a in file_action.menu().actions() if a.text() == "Add Expenses Plan")

        QTimer.singleShot(100, handle_dialog)
        add_expenses_plan_action.trigger()
        qbot_delay()
        expenses_plan_table = self.main_window.expenses_plan_view.expenses_plan_table
        assert len(expenses_plan_table.rows) == 1
        assert present_in_table(expenses_plan_table, {"Name": "fake_name", "Amount": "123.45 €"})

    def test_create_tow_new_expenses_plan(self, make_db, qbot_delay, qtbot):
        make_db(activate=True)

        def make_handle_dialog(name):
            def handle_dialog():
                dialogs = self.main_window.findChildren(QDialog)
                assert dialogs, "Aucun QDialog ouvert"
                dialog = dialogs[-1]
                assert dialog.windowTitle() == "Create Expenses Plan"

                dialog.name_input.clear()
                qtbot.keyClicks(dialog.name_input, name)
                QApplication.processEvents()
                qbot_delay()
                assert dialog.name_input.text() == name

                save_btn = next(btn for btn in dialog.findChildren(QPushButton) if btn.text() == "Save")

                qtbot.mouseClick(save_btn, Qt.LeftButton)
                qbot_delay()

            return handle_dialog

        for i in range(2):
            file_action = next(a for a in self.main_window.menuBar().actions() if a.text() == "Actions")
            add_expenses_plan_action = next(a for a in file_action.menu().actions() if a.text() == "Add Expenses Plan")

            QTimer.singleShot(100, make_handle_dialog(name=f"fake_name_{i}"))
            add_expenses_plan_action.trigger()
            qbot_delay()

        expenses_plan_table = self.main_window.expenses_plan_view.expenses_plan_table
        assert len(expenses_plan_table.rows) == 2
        assert present_in_table(expenses_plan_table, {"Name": "fake_name_0", "Amount": "0.00 €"})
        assert present_in_table(expenses_plan_table, {"Name": "fake_name_1", "Amount": "0.00 €"})


class TestUpdatedExpensesPlan:
    @pytest.fixture(autouse=True)
    def setup(self, qtbot, qbot_delay):
        self.main_window = MainWindow()
        qtbot.addWidget(self.main_window)
        self.main_window.show()
        qbot_delay()

        yield

        self.main_window.close()

    def test_update_expenses_plan(self, make_db, qbot_delay, qtbot):
        make_db(
            activate=True,
            data={
                "expenses": [],
                "categories": [],
                "expensesplans": [
                    {
                        "amount": 5.0,
                        "name": "toto",
                        "description": "",
                        "category_id": None,
                        "expensesplan_id": "38158ec8-bcb3-473e-9b2b-a092f555b46b",
                        "start_date": "2020-09-01",
                        "end_date": "3025-09-18",
                        "due_date": "2025-10-31",
                        "frequency": "monthly",
                    },
                ],
            },
        )
        self.main_window.expenses_view.load()
        self.main_window.expenses_plan_view.load()

        def handle_dialog():
            dialogs = self.main_window.findChildren(QDialog)

            dialog = dialogs[-1]
            assert dialog.windowTitle() == "Update Expenses Plan"
            QApplication.processEvents()

            dialog.name_input.clear()
            qtbot.keyClicks(dialog.name_input, "renamed")
            QApplication.processEvents()
            qbot_delay()

            dialog.amount_input.lineEdit().clear()
            qtbot.keyClicks(dialog.amount_input.lineEdit(), "123,45")
            QApplication.processEvents()
            qbot_delay()

            assert dialog.name_input.text() == "renamed"

            save_btn = next(btn for btn in dialog.findChildren(QPushButton) if btn.text() == "Save")

            qtbot.mouseClick(save_btn, Qt.LeftButton)
            qbot_delay()

        expenses_plan_table = self.main_window.expenses_plan_view.expenses_plan_table
        row = get_row_in_table(expenses_plan_table, {"Name": "toto"})

        QTimer.singleShot(100, handle_dialog)
        qtbot.mouseClick(row, Qt.LeftButton)
        qbot_delay()

        assert present_in_table(expenses_plan_table, {"Name": "renamed", "Amount": "123.45 €"})


class TestDeletedExpensesPlan:
    @pytest.fixture(autouse=True)
    def setup(self, qtbot, qbot_delay):
        self.main_window = MainWindow()
        qtbot.addWidget(self.main_window)
        self.main_window.show()
        qbot_delay()

        yield

        self.main_window.close()

    def test_delete_expenses_plan(self, make_db, qbot_delay, qtbot, mocker):
        make_db(
            activate=True,
            data={
                "expenses": [],
                "categories": [],
                "expensesplans": [
                    {
                        "amount": 5.0,
                        "name": "toto",
                        "description": "",
                        "category_id": None,
                        "expensesplan_id": "38158ec8-bcb3-473e-9b2b-a092f555b46b",
                        "start_date": "2020-09-01",
                        "end_date": "3025-09-18",
                        "due_date": "2025-10-31",
                        "frequency": "monthly",
                    },
                ],
            },
        )
        self.main_window.expenses_view.load()
        self.main_window.expenses_plan_view.load()
        expenses_plan_table = self.main_window.expenses_plan_view.expenses_plan_table
        assert present_in_table(expenses_plan_table, {"Name": "toto", "Amount": "5.00 €"})

        mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.Yes)

        def handle_dialog():
            dialogs = self.main_window.findChildren(QDialog)

            dialog = dialogs[-1]
            assert dialog.windowTitle() == "Update Expenses Plan"
            QApplication.processEvents()
            qbot_delay()

            save_btn = next(btn for btn in dialog.findChildren(QPushButton) if btn.text() == "Deleted")

            qtbot.mouseClick(save_btn, Qt.LeftButton)
            qbot_delay()

        expenses_plan_table = self.main_window.expenses_plan_view.expenses_plan_table
        row = get_row_in_table(expenses_plan_table, {"Name": "toto"})
        QTimer.singleShot(100, handle_dialog)
        qtbot.mouseClick(row, Qt.LeftButton)
        qbot_delay()

        assert absent_in_table(expenses_plan_table, {"Name": "toto", "Amount": "5.00 €"})
