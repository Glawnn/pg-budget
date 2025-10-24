"""Widget for expenses Stats"""

from datetime import datetime

from pg_budget.core.models.income import Income
from pg_budget.gui.widgets.base.base_stats import BaseStats
from pg_budget.gui.widgets.stat_item import StatItem


class IncomesStats(BaseStats):
    def __init__(self, parent=None):
        items = [
            StatItem("Total", "0", "€", id="total_income"),
            StatItem("Already Received", "0", "€", id="already_received"),
            StatItem("Remaining Income", "0", id="income_remaining_count"),
            StatItem("Remaining Count", "0", "€", id="remaining_income"),
        ]
        super().__init__(items, columns=2, parent=parent)

    def update_stats(self, incomes: list[Income]):
        """Update stats from a list of Income objects."""
        if not incomes:
            self.reset_values()
            return

        today = datetime.now().date()

        total = sum(i.amount for i in incomes)

        already_received = sum(
            i.amount for i in incomes if i.date and datetime.strptime(i.date, "%Y-%m-%d").date() <= today
        )

        remaining_amount = total - already_received

        remaining_count = sum(1 for i in incomes if i.date and datetime.strptime(i.date, "%Y-%m-%d").date() > today)

        self.set_value("total_income", f"{total:.2f}")
        self.set_value("already_received", f"{already_received:.2f}")
        self.set_value("remaining_income", f"{remaining_amount:.2f}")
        self.set_value("income_remaining_count", remaining_count)
