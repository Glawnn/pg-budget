"""Custom Row for ExpensePlan"""

from pg_budget.core.models.expenses_plan import ExpensesPlan
from pg_budget.gui.widgets.base.base_row import BaseRow, RowField
from pg_budget.utils import DateFormatter


class ExpensesPlanRow(BaseRow):
    """Class row for expense"""

    def __init__(self, expenses_plan: ExpensesPlan, parent=None):
        formatted_start_date = DateFormatter.format(expenses_plan.start_date)
        formatted_end_date = DateFormatter.format(expenses_plan.end_date)

        fields = [
            RowField("Name", value=expenses_plan.name),
            RowField("Amount", value=f"{expenses_plan.amount:.2f} €"),
            RowField("Start Date", value=formatted_start_date),
            RowField("End Date", value=formatted_end_date),
        ]

        super().__init__(fields, expenses_plan.expensesplan_id, parent)

    def _init_connections(self):
        pass

    @staticmethod
    def get_fields_names():
        return ["Name", "Amount", "Start Date", "End Date"]
