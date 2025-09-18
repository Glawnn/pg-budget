import json

import pytest

from pg_budget.gui.windows.main_window import MainWindow


@pytest.mark.usefixtures("qtbot")
class TestDatabaseFile:
    @pytest.fixture(autouse=True)
    def setup(self, qtbot):
        """Instancie la fenêtre principale avant chaque test"""
        self.main_window = MainWindow()
        qtbot.addWidget(self.main_window)
        self.main_window.show()
        qtbot.wait(1000)

        yield

        self.main_window.close()

    def test_create_new_db(self, qtbot, mocker, tmp_path):
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
        qtbot.wait(500)

        # --- Vérifier que la DB a bien été créée ---
        assert test_db_path.exists(), "Le fichier DB n'a pas été créé"

        with open(test_db_path, "r") as f:
            data = json.load(f)
            assert "expenses" in data
            assert "expensesplans" in data
            assert "categories" in data

        # --- Vérifier que la popup a été affichée ---
        mock_info.assert_called_once()

    def test_load_existing_db(self, qtbot, mocker, tmp_path):
        # --- Préparer un fichier DB temporaire avec une expense et un expense plan ---
        test_db_path = tmp_path / "test_budget_load.json"
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
        test_db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(test_db_path, "w") as f:
            json.dump(db_data, f, indent=4)

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
        qtbot.wait(500)

        # --- Vérifier que les données sont chargées dans ExpensesView ---
        expense_rows = self.main_window.expenses_view.expense_table.rows
        assert len(expense_rows) == 1
        assert self.main_window.expenses_view.expense_table.rows[0].get_widget_by_name("Name").text() == "Test Expense"
        assert self.main_window.expenses_view.expense_table.rows[0].get_widget_by_name("Amount").text() == "123.45 €"
        assert self.main_window.expenses_view.expense_table.rows[0].get_widget_by_name("Date").text() == "2025-09-01"

        # --- Vérifier que les données sont chargées dans ExpensesPlanView ---
        # plan_rows = self.main_window.expenses_plan_view.expenses_plan_table.rows
        # assert len(plan_rows) == 1
        # assert plan_rows[0].name_label.text() == "Test Plan"
        # assert plan_rows[0].amount_label.text() == "500.00 €"
