"""View for Expenses Plans"""

from PySide6.QtWidgets import QWidget, QVBoxLayout

from pg_budget.core.models.expenses_plan import ExpensesPlan
from pg_budget.core.services import expensesPlanService
from pg_budget.gui.widgets.expense_plan_table import ExpensesPlanTable


class ExpensesPlanView(QWidget):
    """class view for Expenses Plan"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        self.expense_plan_table = ExpensesPlanTable()
        self.load()
        layout.addWidget(self.expense_plan_table)
        self.expense_plan_table.updated_table.connect(self.load)

    def load(self):
        """Load / reload all elements on view"""
        expenses_plans = [ExpensesPlan(**exp_plan) for exp_plan in expensesPlanService.get_all()]
        self.expense_plan_table.load(expenses_plans)
