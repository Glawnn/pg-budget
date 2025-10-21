"""Widget for expenses Stats"""

from pg_budget.gui.widgets.base.base_stats import BaseStats
from pg_budget.gui.widgets.stat_item import StatItem


class ExpensesStats(BaseStats):
    def __init__(self, parent=None):
        items = [
            StatItem("Total", "0", "€", id="expense_total"),
            StatItem("Already Paid", "0", "€", id="already_paid"),
            StatItem("Remaining Expenses", "0", id="expense_remaining_count"),
            StatItem("Remaining", "0", "€", id="expense_remaining"),
        ]
        super().__init__(items, columns=2, parent=parent)

    def update_stats(self, expenses: list):
        if not expenses:
            self.reset_values()
            return

        total = sum(e.amount for e in expenses)
        paid = sum(e.amount for e in expenses if e.payed)
        remaining = total - paid
        remaining_count = sum(1 for e in expenses if not e.payed)

        self.set_value("expense_total", f"{total:.2f}")
        self.set_value("already_paid", f"{paid:.2f}")
        self.set_value("expense_remaining", f"{remaining:.2f}")
        self.set_value("expense_remaining_count", remaining_count)
