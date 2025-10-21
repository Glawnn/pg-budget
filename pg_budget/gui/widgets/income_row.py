"""Custom Row for Income"""

from pg_budget.core.models.income import Income
from pg_budget.gui.widgets.base.base_row import BaseRow, RowField
from pg_budget.utils import DateFormatter
from pg_budget.core.services import incomeService


class IncomeRow(BaseRow):
    """class for income row"""

    def __init__(self, income: Income, parent=None):
        formatted_date = DateFormatter.format(income.date)
        categories = incomeService.get_categories()
        category = next(
            (cat for cat in categories if cat.category_id == income.category_id),
            None,
        )
        category_name = category.name if category else "Unknown"
        category_color = category.color if category and category.color else "#999999"

        fields = [
            RowField("Name", value=income.name),
            RowField("Amount", value=f"{income.amount:.2f} €"),
            RowField("Date", value=formatted_date),
            RowField("Category", value=category_name, color=category_color),
        ]

        super().__init__(fields, income.income_id, parent)

    @staticmethod
    def get_fields_names():
        return ["Name", "Amount", "Date", "Category"]
