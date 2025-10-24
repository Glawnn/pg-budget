"""Custom Row for Expense"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from pg_budget.gui import logger
from pg_budget.gui.widgets.base.base_row import BaseRow


class HeaderRow(BaseRow):
    """class for expense row"""

    sort_requested = Signal(str, bool)  # (column_name, ascending)

    def __init__(self, fields, parent=None, clickable: bool = False):
        self._sort_states = {}
        super().__init__(fields, row_id="header", parent=parent, clickable=clickable)

    def _init_connections(self):
        for name, widget in self.widgets:
            if isinstance(widget, QPushButton):
                self._sort_states[name] = True
                widget.clicked.connect(lambda checked, n=name: self._on_sort_clicked(n))

    def _on_sort_clicked(self, column_name):
        ascending = self._sort_states[column_name]
        self._sort_states[column_name] = not ascending
        self.sort_requested.emit(column_name, ascending)
        logger.debug("Sort requested on column '%s', ascending=%s", column_name, ascending)

    @staticmethod
    def get_fields_names():
        return None
