from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout

from pg_budget.core.services import expense_service, income_service
from pg_budget.gui import logger
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.views.base_view import BaseView
from pg_budget.gui.widgets.expenses_table import ExpensesTable
from pg_budget.gui.widgets.incomes_table import IncomesTable
from pg_budget.gui.widgets.month_year_picker import MonthYearPicker
from pg_budget.gui.widgets.resume_stats import ResumeStats


class ResumeView(BaseView):
    """View for resume of budgets"""

    def _init(self):
        logger.debug("Initializing ResumeView")

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        self.month_year_picker = MonthYearPicker()
        top_layout.addWidget(self.month_year_picker, alignment=Qt.AlignLeft)
        self._layout.addLayout(top_layout)

        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(20)

        self.income_table = IncomesTable()
        tables_layout.addWidget(self.income_table)
        self.month_year_picker.month_changed.connect(safe_callback(self.load))

        self.expense_table = ExpensesTable()
        tables_layout.addWidget(self.expense_table)
        self.month_year_picker.month_changed.connect(safe_callback(self.load))

        self._layout.addLayout(tables_layout)

        self.expenses_stats = ResumeStats()
        self.expenses_stats.setObjectName("ResumeStats")
        self._layout.addWidget(self.expenses_stats)

    def load(self, *_args, **_kwargs):
        """Load / reload all elements on view"""
        year, month = self.month_year_picker.get_year_month()
        logger.info("Loading ResumeView for %d/%d", month, year)
        incomes = income_service.get_by_month(year, month)
        expenses = expense_service.get_by_month(year, month)

        self.income_table.load(incomes)
        self.expense_table.load(expenses)
        self.expenses_stats.update_stats(expenses=expenses, incomes=incomes)

        logger.debug("ResumeView loaded %d incomes, %d expenses", len(incomes), len(expenses))
