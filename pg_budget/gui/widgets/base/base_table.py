"""base of table"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QFrame,
    QPushButton,
    QCheckBox,
    QLabel,
    QComboBox,
)
from PySide6.QtCore import Qt, Signal

from pg_budget.gui.widgets.base import BaseRow
from pg_budget.gui import logger
from pg_budget.gui.widgets.base.base_row import RowField
from pg_budget.gui.widgets.header_row import HeaderRow


class BaseTable(QFrame):
    """Base cladd for Table"""

    updated_table = Signal()

    def __init__(self, row_class: type, default_filterable: str = None):
        super().__init__()
        self.row_class = row_class
        self.rows: list[BaseRow] = []
        self.default_filterable = default_filterable

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

        header_fields = [RowField(name, type=QPushButton, value=name) for name in self.row_class.get_fields_names()]
        self.header_row = HeaderRow(header_fields, parent=self.container)
        self.container_layout.addWidget(self.header_row)
        self.header_row.sort_requested.connect(self._sort_table)

        for item in items:
            row = self.row_class(item, parent=self.container)
            self._init_row_connections(row)
            self.container_layout.addWidget(row)
            self.rows.append(row)

        if self.default_filterable:
            self._sort_table(self.default_filterable, True)

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

            all_rows: list[BaseRow] = []
            all_rows.append(self.header_row)
            all_rows.extend(self.rows)

            for row in all_rows:
                for w_name, widget in row.widgets:
                    widget_width = widget.sizeHint().width()
                    if widget_width > max_widths[w_name]:
                        max_widths[w_name] = widget_width

            for row in all_rows:
                row.resize_columns(max_widths)

    def _sort_table(self, column_name: str, ascending: bool):
        """Sort table by column name

        Args:
            column_name (str): name of column
            ascending (bool): ascending or descending
        """
        logger.debug("Sorting BaseTable by column '%s', ascending=%s", column_name, ascending)
        try:
            index = next(i for i, (name, widget) in enumerate(self.header_row.widgets) if name == column_name)
        except StopIteration:
            logger.error("Column name '%s' not found in header row", column_name)
            return

        def sort_key(row: BaseRow):
            widget = row.widgets[index][1]
            if isinstance(widget, QPushButton) or isinstance(widget, QLabel):
                text = widget.text()
                try:
                    return float(text.replace(" €", "").replace(",", "."))
                except ValueError:
                    return text.lower()
            elif isinstance(widget, QCheckBox):
                return widget.isChecked()
            elif isinstance(widget, QComboBox):
                return widget.currentText().lower()
            return str(widget)

        self.rows.sort(key=sort_key, reverse=not ascending)

        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget and widget != self.header_row:
                widget.setParent(None)

        for row in self.rows:
            self.container_layout.addWidget(row)

        self.resizing()
