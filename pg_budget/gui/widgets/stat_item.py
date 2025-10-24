from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class StatItem(QWidget):
    """Single stat item (title + value + unit in one label)"""

    def __init__(self, title: str, value: str = "0", unit: str = "", id: str = None, parent=None):
        super().__init__(parent)
        self._id = id or title.lower().replace(" ", "_")
        self.title = title
        self.unit = unit
        self.value = value

        self.label = QLabel(self._format_text())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName(f"StatItem_{self._id}")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

    def _format_text(self):
        """Builds the full text for the label"""
        if self.unit:
            return f"<b>{self.title}:</b> {self.value} {self.unit}"
        return f"<b>{self.title}:</b> {self.value}"

    def set_value(self, value):
        """Update displayed value"""
        self.value = str(value)
        self.label.setText(self._format_text())

    def set_unit(self, unit):
        """Update unit dynamically"""
        self.unit = unit
        self.label.setText(self._format_text())

    def set_color(self, color: str):
        """Change text color dynamically"""
        self.label.setStyleSheet(f"color: {color};")
