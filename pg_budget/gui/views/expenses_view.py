"""View for Expenses"""

from PySide6.QtWidgets import QWidget, QVBoxLayout

from pg_budget.core.services import expenseService
from pg_budget.gui.widgets.expenses_table import ExpensesTable
from pg_budget.gui.widgets.month_year_picker import MonthYearPicker


class ExpensesView(QWidget):
    """View for Expenses"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        self.month_year_picker = MonthYearPicker()
        layout.addWidget(self.month_year_picker)

        self.expense_table = ExpensesTable()
        self.load()
        layout.addWidget(self.expense_table)
        self.expense_table.updated_table.connect(self.load)

    def load(self):
        """Load / reload all elements on view"""
        year, month = self.month_year_picker.get_year_month()
        expenses = expenseService.get_by_month(year, month)
        self.expense_table.load(expenses)
