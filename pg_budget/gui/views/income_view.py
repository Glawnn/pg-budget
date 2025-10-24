"""View for Expenses"""

from pg_budget.core.services import income_service
from pg_budget.gui import logger
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.views.base_view import BaseView
from pg_budget.gui.widgets.incomes_stats import IncomesStats
from pg_budget.gui.widgets.incomes_table import IncomesTable
from pg_budget.gui.widgets.month_year_picker import MonthYearPicker


class IncomeView(BaseView):
    """View for Expenses"""

    def _init(self):
        logger.debug("Initializing IncomeView")
        self.month_year_picker = MonthYearPicker()
        self._layout.addWidget(self.month_year_picker)

        self.income_table = IncomesTable()
        self._layout.addWidget(self.income_table)
        self.income_table.updated_table.connect(safe_callback(self.load))
        self.month_year_picker.month_changed.connect(safe_callback(self.load))

        self.incomes_stats = IncomesStats()
        self.incomes_stats.setObjectName("IncomesStats")
        self._layout.addWidget(self.incomes_stats)

        logger.debug("IncomeView initialized with MonthYearPicker and IncomesTable")

    def load(self, *_args, **_kwargs):
        """Load / reload all elements on view"""
        year, month = self.month_year_picker.get_year_month()
        logger.info("Loading ExpenseIncomeViewsView for %d/%d", month, year)
        incomes = income_service.get_by_month(year, month)

        self.income_table.load(incomes)
        self.incomes_stats.update_stats(incomes)
        logger.debug("IncomeView loaded %d expenses", len(incomes))
