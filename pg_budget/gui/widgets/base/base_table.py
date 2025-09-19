"""base of table"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PySide6.QtCore import Qt, Signal

from pg_budget.gui.widgets.base import BaseRow
from pg_budget.gui import logger


class BaseTable(QFrame):
    """Base cladd for Table"""

    updated_table = Signal()

    def __init__(self, row_class: type):
        super().__init__()
        self.row_class = row_class
        self.rows: list[BaseRow] = []

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self._layout.addWidget(scroll)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(5)
        scroll.setWidget(self.container)

    def clear(self):
        """Clear all elements of the table content"""
        logger.debug("Clearing BaseTable rows (%d rows)", len(self.rows))
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.rows = []
        self._clear()

    def _clear(self):
        """add other clear"""

    def load(self, items, clear=True):
        """Load a list of items (models)

        Args:
            items (_type_): list of models
            clear (bool, optional): clear table before reload. Defaults to True.
        """
        if clear:
            self.clear()

        for item in items:
            row = self.row_class(item)
            self._init_row_connections(row)
            self.container_layout.addWidget(row)
            self.rows.append(row)

        self.container_layout.setAlignment(Qt.AlignTop)
        logger.debug("Loaded BaseTable with %d rows", len(self.rows))

        self.resizing()

    def _init_row_connections(self, row: BaseRow):
        pass

    def resizing(self):
        """Resize all row"""
        if self.rows:
            column_keys = [name for name, widget in self.rows[0].widgets]
            max_widths = {key: 0 for key in column_keys}

            for row in self.rows:
                for w_name, widget in row.widgets:
                    widget_width = widget.sizeHint().width()
                    if widget_width > max_widths[w_name]:
                        max_widths[w_name] = widget_width

            for row in self.rows:
                row.resize_columns(max_widths)
