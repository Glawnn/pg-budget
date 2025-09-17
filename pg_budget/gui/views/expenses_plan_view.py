from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel


from pg_budget.core.models.expense import Expense
from pg_budget.core.services import expenseService
from pg_budget.gui.widgets import MonthYearPicker, ExpensesTable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from pg_budget.gui.widgets.expense_plan_table import ExpensesPlanTable


class ExpensesPlanView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        self.expense_plan_table = ExpensesPlanTable()
        layout.addWidget(self.expense_plan_table)

        self.load_table()

    def load_table(self):
        self.expense_plan_table.load()

    def reload(self):
        self.load_table()

        


