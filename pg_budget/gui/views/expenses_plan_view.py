"""View for Expenses Plans"""

from pg_budget.core.models.expenses_plan import ExpensesPlan
from pg_budget.core.services import expensesPlanService
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.views.base_view import BaseView
from pg_budget.gui.widgets.expense_plan_table import ExpensesPlanTable


class ExpensesPlanView(BaseView):
    """class view for Expenses Plan"""

    def _init(self):

        self.expense_plan_table = ExpensesPlanTable()
        self._layout.addWidget(self.expense_plan_table)
        self.expense_plan_table.updated_table.connect(safe_callback(self.load))

    def load(self):
        """Load / reload all elements on view"""
        expenses_plans = [ExpensesPlan(**exp_plan) for exp_plan in expensesPlanService.get_all()]
        self.expense_plan_table.load(expenses_plans)
