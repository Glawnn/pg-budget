"""Custom Row for Expense"""

from PySide6.QtCore import Signal

from pg_budget.gui.widgets.base.base_row import BaseRow


class HeaderRow(BaseRow):
    """class for expense row"""

    paid_changed = Signal(bool)

    def __init__(self, fields, parent=None):
        super().__init__(fields, row_id="header", parent=parent)

    @staticmethod
    def get_fields_names():
        return None
