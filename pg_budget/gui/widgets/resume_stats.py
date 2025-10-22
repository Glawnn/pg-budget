"""Widget for resume Stats"""

from typing import List
from pg_budget.core.models.expense import Expense
from pg_budget.gui.widgets.base.base_stats import BaseStats
from pg_budget.gui.widgets.stat_item import StatItem


class ResumeStats(BaseStats):
    def __init__(self, parent=None):
        items = [
            StatItem("Total expense", "0", "€", id="expense_total"),
            StatItem("Total income", "0", "€", id="total_income"),
            StatItem("Remaining", "0", "€", id="remaining"),
        ]
        super().__init__(items, columns=3, parent=parent)

    def update_stats(self, expenses: List[Expense], incomes: List[Expense]):
        if not expenses or not incomes:
            self.reset_values()
            return

        total_expense = sum(e.amount for e in expenses)
        total_income = sum(i.amount for i in incomes)
        remaining = total_income - total_expense

        self.set_value("expense_total", f"{total_expense:.2f}")
        self.set_value("total_income", f"{total_income:.2f}")
        self.set_value("remaining", f"{remaining:.2f}")

        remaining_item = self._stats["remaining"]
        if remaining_item:
            if remaining >= 0:
                remaining_item.set_color("#7ee37e")
            else:
                remaining_item.set_color("#e37e7e")
