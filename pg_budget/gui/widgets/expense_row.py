"""Custom Row for Expense"""

from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Signal

from pg_budget.gui.utils import safe_callback
from pg_budget.gui.widgets.base.base_row import BaseRow, RowField
from pg_budget.core.models.expense import Expense


class ExpenseRow(BaseRow):
    """class for expense row"""

    paid_changed = Signal(bool)

    def __init__(self, expense: Expense, parent=None):
        fields = [
            RowField("Name", value=expense.name),
            RowField("Amount", value=f"{expense.amount:.2f} €"),
            RowField("Date", value=expense.date),
            RowField("Paid", type=QCheckBox, value=expense.payed),
        ]

        super().__init__(fields, expense.expense_id, parent)

    def _init_connections(self):
        paid_checkbox: QCheckBox = self.get_widget_by_name("Paid")
        if paid_checkbox:
            paid_checkbox.stateChanged.connect(safe_callback(lambda state: self.paid_changed.emit(state == 2)))

    @staticmethod
    def get_fields_names():
        return ["Name", "Amount", "Date", "Paid"]
