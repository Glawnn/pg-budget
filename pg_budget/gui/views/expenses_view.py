"""View for Expenses"""

from pg_budget.core.services import expenseService
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.views.base_view import BaseView
from pg_budget.gui.widgets.expenses_table import ExpensesTable
from pg_budget.gui.widgets.month_year_picker import MonthYearPicker
from pg_budget.gui import logger


class ExpensesView(BaseView):
    """View for Expenses"""

    def _init(self):
        logger.debug("Initializing ExpensesView")
        self.month_year_picker = MonthYearPicker()
        self._layout.addWidget(self.month_year_picker)

        self.expense_table = ExpensesTable()
        self._layout.addWidget(self.expense_table)
        self.expense_table.updated_table.connect(safe_callback(self.load))
        self.month_year_picker.month_changed.connect(safe_callback(self.load))
        logger.debug("ExpensesView initialized with MonthYearPicker and ExpensesTable")

    def load(self, *_args, **_kwargs):
        """Load / reload all elements on view"""
        year, month = self.month_year_picker.get_year_month()
        logger.info("Loading ExpensesView for %d/%d", month, year)
        expenses = expenseService.get_by_month(year, month)
        self.expense_table.load(expenses)
        logger.debug("ExpensesView loaded %d expenses", len(expenses))
