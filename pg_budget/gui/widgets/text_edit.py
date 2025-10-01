"""Text Edit Widget"""

from PySide6.QtWidgets import QWidget, QTextEdit, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

from pg_budget.gui.utils import safe_callback
from pg_budget.gui import logger


class TextEdit(QWidget):
    """Widget text edit"""

    def __init__(self, text: str = "", lines_number: int = 5, max_chars: int = None, parent=None):
        super().__init__(parent)
        self.lines_number = lines_number
        self.max_chars = max_chars

        logger.debug(
            "Initializing TextEdit widget: lines=%d, max_chars=%s",
            lines_number,
            max_chars,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- text Zone ---
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(text)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.text_edit)

        # --- Counter Label ---
        self.counter_label = QLabel("", self)
        self.counter_label.setAlignment(Qt.AlignRight)
        self.counter_label.setStyleSheet("color: gray; font-size: 10px;")
        self.counter_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.counter_label)

        self._update_height()

        self.text_edit.textChanged.connect(safe_callback(self._enforce_limits))
        self._enforce_limits()

    def _update_height(self):
        """Set the fixed height based on number of visible lines."""
        font_metrics = self.text_edit.fontMetrics()
        line_height = font_metrics.lineSpacing()
        height = self.lines_number * line_height + 10 * self.text_edit.frameWidth()
        self.text_edit.setFixedHeight(height)
        logger.debug("TextEdit height set to %d", height)

    def _enforce_limits(self):
        """Enforce max characters and update counter."""
        text = self.text_edit.toPlainText()
        if self.max_chars is not None and len(text) > self.max_chars:
            cursor = self.text_edit.textCursor()
            pos = cursor.position()
            self.text_edit.setPlainText(text[: self.max_chars])
            # Restore cursor position safely
            cursor.setPosition(min(pos, self.max_chars))
            self.text_edit.setTextCursor(cursor)
            logger.info("TextEdit content truncated to max_chars=%d", self.max_chars)

        # Update counter
        if self.max_chars:
            self.counter_label.setText(f"{len(self.text_edit.toPlainText())}/{self.max_chars}")
        else:
            self.counter_label.setText(f"{len(self.text_edit.toPlainText())}")

    def get_text(self):
        """return the current text"""
        return self.text_edit.toPlainText()
