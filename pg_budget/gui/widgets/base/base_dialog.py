"""class for base dialog"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal

from pg_budget.gui.utils import safe_callback


class BaseDialog(QDialog):
    """Base class for dialog"""

    updated = Signal(str)

    def __init__(self, entity_id: str = None, parent=None, fixed_size: tuple[int, int] = (300, 300)):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.entity_id = entity_id
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(*fixed_size)

        self._layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        self._init_form(self.form_layout)
        self._layout.addLayout(self.form_layout)
        self._init_buttons()

    def _init_form(self, form_layout: QFormLayout):
        """"""
        raise NotImplementedError

    def _init_buttons(self):
        """tmp"""
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(safe_callback(self._on_save_btn_clicked))
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(safe_callback(self._on_cancel_btn_clicked))
        btn_layout.addWidget(cancel_btn)

        self._layout.addLayout(btn_layout)

        if self.entity_id:
            deleted_btn = QPushButton("Deleted")
            deleted_btn.clicked.connect(safe_callback(self.confirm_delete))
            deleted_btn.setStyleSheet("background-color: red")
            self._layout.addWidget(deleted_btn)

    def _on_save_btn_clicked(self):
        """"""
        raise NotImplementedError

    def _delete_entity(self):
        """"""
        raise NotImplementedError

    def _on_cancel_btn_clicked(self):
        """"""
        self.close()

    def confirm_delete(self):
        """Ask for confirmation before deletion."""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this item?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._delete_entity()
            self.updated.emit(self.entity_id)
            self.accept()
