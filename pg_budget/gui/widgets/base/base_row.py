from dataclasses import dataclass, field
from typing import Any, Type
from PySide6.QtWidgets import QFrame, QHBoxLayout, QCheckBox, QLabel, QComboBox
from PySide6.QtCore import Signal, Qt

@dataclass
class RowField:
    label: str
    type: Type = QLabel      
    value: Any = None
    options: list = field(default_factory=list)

class BaseRow(QFrame):
    row_clicked = Signal()

    def __init__(self, fields: list[RowField], row_id: str, parent=None):
        super().__init__(parent)
        self.row_id = row_id
        self.fields = fields
        self.widgets= []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)
        self._layout = layout

        self._init_fields()
        self._init_connections()
        self._init_styles()

        self._ignore_widgets = None
    
    def get_widget_by_name(self, name: str):
        for w_name, widget in self.widgets:
            if w_name == name:
                return widget
        return None 

    def _init_fields(self):
        for field in self.fields:
            if field.type == QLabel:
                widget = QLabel(str(field.value))
            elif field.type == QCheckBox:
                widget = QCheckBox()
                widget.setChecked(bool(field.value))
            elif field.type == QComboBox:
                widget = QComboBox()
                widget.addItems(field.options)
                if field.value in field.options:
                    widget.setCurrentText(field.value)
            else:
                widget = QLabel(str(field.value))

            self.widgets.append((field.label, widget))
            self._layout.addWidget(widget)
            self._layout.addStretch(1)

    def _init_connections(self):
        """Override pour connecter les signals (ex : checkbox, clic)"""
        pass

    def _init_styles(self):
        """Appliquer le style des widgets ou du row"""
        pass

    def mousePressEvent(self, event):
        clicked_widget = self.childAt(event.pos())

        interactive_widgets = [w for w in self.widgets if isinstance(w, (QCheckBox, QComboBox))]
        if clicked_widget in interactive_widgets:
            return super().mousePressEvent(event)

        self.row_clicked.emit(self.row_id)
        return super().mousePressEvent(event)
    
    def resize_columns(self, width: dict):
        """Redimensionne chaque colonne selon un dict {'name': w1, 'amount': w2, ...}"""
        for w_name, widget in self.widgets:
            if w_name in width:
                widget.setFixedWidth(width[w_name])
