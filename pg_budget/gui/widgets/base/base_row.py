"""Base row class for Table"""

from dataclasses import dataclass, field
from typing import Any, Type
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QCheckBox,
    QLabel,
    QComboBox,
    QWidget,
    QPushButton,
)
from PySide6.QtCore import Signal
from pg_budget.gui import logger


@dataclass
class RowField:
    """Row field"""

    label: str
    type: Type = QLabel
    value: Any = None
    options: list = field(default_factory=list)


class BaseRow(QFrame):
    """Base of Row"""

    row_clicked = Signal()

    def __init__(self, fields: list[RowField], row_id: str, parent=None, clickable: bool = True):
        super().__init__(parent)
        self.row_id = row_id
        self.fields = fields
        self.widgets = []
        self.clickable = clickable

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self._layout = layout

        self._init_fields()
        self._init_connections()
        self._init_styles()

        self._ignore_widgets = None

    @staticmethod
    def get_fields_names():
        raise NotImplementedError

    def get_widget_by_name(self, name: str) -> QWidget:
        """return widget used for column name

        Args:
            name (str): name of column

        Returns:
            QWidget: QWidget of column
        """
        for w_name, widget in self.widgets:
            if w_name == name:
                return widget
        return None

    def _init_fields(self):
        """create and add all widgets on layout"""
        for _field in self.fields:
            if _field.type == QLabel:
                widget = QLabel(str(_field.value))
            elif _field.type == QCheckBox:
                widget = QCheckBox()
                widget.setChecked(bool(_field.value))
            elif _field.type == QComboBox:
                widget = QComboBox()
                widget.addItems(_field.options)
                if _field.value in _field.options:
                    widget.setCurrentText(_field.value)
            elif _field.type == QPushButton:
                widget = QPushButton(str(_field.value))
                widget.setFlat(True)
            else:
                widget = QLabel(str(_field.value))

            self.widgets.append((_field.label, widget))
            self._layout.addWidget(widget)
            self._layout.addStretch(1)

    def _init_connections(self):
        """Overridefor connect signals (ex : checkbox, click)"""

    def _init_styles(self):
        """Add style row"""

    def mousePressEvent(self, event):
        """Detect when row is clicked"""
        clicked_widget = self.childAt(event.position().toPoint())
        if self.clickable:
            interactive_widgets = [w for w in self.widgets if isinstance(w, (QCheckBox, QComboBox))]
            if clicked_widget in interactive_widgets:
                return super().mousePressEvent(event)

            logger.debug("Row clicked: %s", self.row_id)
            self.row_clicked.emit()

        return super().mousePressEvent(event)

    def resize_columns(self, width: dict):
        """Redimensionne chaque colonne selon un dict {'name': w1, 'amount': w2, ...}"""
        for w_name, widget in self.widgets:
            if w_name in width:
                widget.setFixedWidth(width[w_name])
