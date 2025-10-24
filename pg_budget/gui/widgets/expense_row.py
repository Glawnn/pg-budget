"""Custom Row for Expense"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox

from pg_budget.core.models.expense import Expense
from pg_budget.core.services import expense_service
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.widgets.base.base_row import BaseRow, RowField
from pg_budget.utils import DateFormatter


class ExpenseRow(BaseRow):
    """class for expense row"""

    paid_changed = Signal(bool)

    def __init__(self, expense: Expense, parent=None):
        formatted_date = DateFormatter.format(expense.date)
        categories = expense_service.get_categories()
        category = next(
            (cat for cat in categories if cat.category_id == expense.category_id),
            None,
        )
        category_name = category.name if category else "Unknown"
        category_color = category.color if category and category.color else "#999999"

        fields = [
            RowField("Name", value=expense.name),
            RowField("Amount", value=f"{expense.amount:.2f} €"),
            RowField("Date", value=formatted_date),
            RowField("Paid", type=QCheckBox, value=expense.payed),
            RowField("Category", value=category_name, color=category_color),
        ]

        super().__init__(fields, expense.expense_id, parent)

    def _init_connections(self):
        paid_checkbox: QCheckBox = self.get_widget_by_name("Paid")
        if paid_checkbox:
            paid_checkbox.stateChanged.connect(safe_callback(lambda state: self.paid_changed.emit(state == 2)))

    @staticmethod
    def get_fields_names():
        return ["Name", "Amount", "Date", "Paid", "Category"]
