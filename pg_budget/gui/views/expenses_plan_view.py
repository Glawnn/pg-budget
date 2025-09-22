"""View for Expenses Plans"""

from pg_budget.core.models.expenses_plan import ExpensesPlan
from pg_budget.core.services import expensesPlanService
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.views.base_view import BaseView
from pg_budget.gui.widgets.expenses_plan_table import ExpensesPlanTable
from pg_budget.gui import logger


class ExpensesPlanView(BaseView):
    """class view for Expenses Plan"""

    def _init(self):
        logger.debug("Initializing ExpensesPlanView")

        self.expenses_plan_table = ExpensesPlanTable()
        self._layout.addWidget(self.expenses_plan_table)
        self.expenses_plan_table.updated_table.connect(safe_callback(self.load))

        logger.debug("ExpensesPlanView initialized with ExpensesPlanTable")

    def load(self):
        """Load / reload all elements on view"""
        logger.info("Loading ExpensesPlanView")
        expenses_plans = [ExpensesPlan(**exp_plan) for exp_plan in expensesPlanService.get_all()]
        self.expenses_plan_table.load(expenses_plans)
        logger.debug("ExpensesPlanView loaded %d expense plans", len(expenses_plans))
