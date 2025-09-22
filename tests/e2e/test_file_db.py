import json

import pytest

from pg_budget.gui.windows.main_window import MainWindow
from tests.e2e.utils import present_in_table


@pytest.mark.usefixtures("qtbot")
class TestDatabaseFile:
    @pytest.fixture(autouse=True)
    def setup(self, qtbot, qbot_delay):
        """Instancie la fenêtre principale avant chaque test"""
        self.main_window = MainWindow()
        qtbot.addWidget(self.main_window)
        self.main_window.show()
        qbot_delay()

        yield

        self.main_window.close()

    def test_create_new_db(self, qtbot, mocker, tmp_path, qbot_delay):
        test_db_path = tmp_path / "subfolder" / "test_budget_new.json"

        mocker.patch(
            "pg_budget.gui.windows.main_window.QFileDialog.getSaveFileName",
            return_value=(str(test_db_path), "JSON Files (*.json)"),
        )

        mock_info = mocker.patch("pg_budget.gui.windows.main_window.QMessageBox.information")

        # --- Récupérer directement l'action "New User" ---
        file_action = next(a for a in self.main_window.menuBar().actions() if a.text() == "File")
        new_user_action = next(a for a in file_action.menu().actions() if a.text() == "New User")

        # --- Déclencher l'action ---
        new_user_action.trigger()
        qbot_delay()

        # --- Vérifier que la DB a bien été créée ---
        assert test_db_path.exists(), "Le fichier DB n'a pas été créé"

        with open(test_db_path, "r") as f:
            data = json.load(f)
            assert "expenses" in data
            assert "expensesplans" in data
            assert "categories" in data

        # --- Vérifier que la popup a été affichée ---
        mock_info.assert_called_once()

    def test_load_existing_db(self, make_db, mocker, qbot_delay):
        db_data = {
            "expenses": [
                {
                    "expense_id": "e1",
                    "name": "Test Expense",
                    "amount": 123.45,
                    "date": "2025-09-01",
                    "payed": False,
                }
            ],
            "expensesplans": [
                {
                    "expensesplan_id": "p1",
                    "name": "Test Plan",
                    "amount": 500.0,
                    "start_date": "2025-09-01",
                    "end_date": "2025-09-30",
                    "due_date": "2025-09-15",
                    "description": "Desc",
                    "frequency": "monthly",
                }
            ],
            "categories": [],
        }

        test_db_path = make_db(db_data)

        # --- Patcher QFileDialog pour ouvrir ce fichier ---
        mocker.patch(
            "pg_budget.gui.windows.main_window.QFileDialog.getOpenFileName",
            return_value=(str(test_db_path), "JSON Files (*.json)"),
        )

        # --- Patcher QMessageBox pour éviter la popup ---
        mocker.patch("pg_budget.gui.windows.main_window.QMessageBox.information")

        # --- Récupérer l’action "Open User" ---
        file_action = next(a for a in self.main_window.menuBar().actions() if a.text() == "File")
        open_user_action = next(a for a in file_action.menu().actions() if a.text() == "Open User")

        # --- Déclencher l’action ---
        open_user_action.trigger()
        qbot_delay()

        # --- Vérifier que les données sont chargées dans ExpensesView ---
        expense_table = self.main_window.expenses_view.expense_table
        assert len(expense_table.rows) == 1

        assert present_in_table(expense_table, {"Name": "Test Expense", "Amount": "123.45 €", "Date": "2025-09-01"})

        # --- Vérifier que les données sont chargées dans ExpensesPlanView ---
        plan_table = self.main_window.expenses_plan_view.expenses_plan_table
        assert len(plan_table.rows) == 1

        assert present_in_table(plan_table, {"Name": "Test Plan", "Amount": "500.00 €"})
