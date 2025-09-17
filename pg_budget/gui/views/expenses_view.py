from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


from pg_budget.core.models.expense import Expense
from pg_budget.core.services import expenseService
from pg_budget.gui.widgets import MonthYearPicker, ExpensesTable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from pg_budget.gui.widgets.expenses_table import ExpenseRow, ExpensesTable2


class ExpensesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        self.month_year_picker = MonthYearPicker()
        layout.addWidget(self.month_year_picker)
        year, month = self.month_year_picker.get_year_month()
        # v1
        self.expense_table = ExpensesTable()
        self.expense_table.load_month(year, month)
        #layout.addWidget(self.expense_table)

        self.month_year_picker.month_changed.connect(lambda y, m: self.expense_table.load_month(y, m))

        # v2
        def load():
            expenses = expenseService.get_by_month(year, month)
            self.expense_table2.load(expenses)

        self.expense_table2 = ExpensesTable2()
        load()
        layout.addWidget(self.expense_table2)
        self.expense_table2.updated_table.connect(lambda: load())

        

        

        # --- Stats section ---
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.stats_label)

        self.expense_table.updated_table.connect(self.load_stats)

        self.load_stats()

    def reload(self):
        self.month_year_picker.go_to_today()
        
        self.load_table()
        self.load_stats()

    def load_table(self):
        year, month = self.month_year_picker.get_year_month()
        self.expense_table.load_month(year, month)

    def load_stats(self):
        data: dict = self.expense_table.get_data()

        self.stats_label.setText(
            f"💰 Total du mois : {data.get("total"):.2f} €    |    🔴 Restant à payer : {data.get("remaining"):.2f} €"
        )

        


