"""Expense Table"""

from PySide6.QtWidgets import (
    QMessageBox,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDoubleSpinBox,
    QDateEdit,
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
    QDialog,
)
from PySide6.QtCore import Qt, Signal, QDate

from pg_budget.core.services import expenseService
from pg_budget.gui.widgets.base.base_table import BaseTable
from pg_budget.gui.widgets.expense_row import ExpenseRow


class ExpensesTable(BaseTable):
    """Expense table class"""

    def __init__(self):
        super().__init__(ExpenseRow)

    def _init_row_connections(self, row):
        row.paid_changed.connect(lambda value, eid=row.row_id: self._on_paid_changed(eid, value))
        row.row_clicked.connect(lambda eid=row.row_id: self._show_expense_detail(eid))

    def _on_paid_changed(self, expense_id: str, paid: bool):
        expenseService.update(expense_id, payed=paid)
        self.updated_table.emit()

    def _show_expense_detail(self, eid):
        dialog = ExpenseDialog(parent=self.window(), expense_id=eid)
        dialog.expense_updated.connect(lambda eid: self.updated_table.emit())
        dialog.expense_deleted.connect(lambda eid: self.updated_table.emit())
        dialog.exec()

    # def get_data(self):
    #     return {
    #         "total": sum(exp.amount for exp in self.expenses),
    #         "remaining": sum(exp.amount for exp in self.expenses if not exp.payed)
    #     }


class ExpenseDialog(QDialog):
    """Expense dialog class"""

    expense_deleted = Signal(str)
    expense_updated = Signal(str)

    def __init__(self, parent=None, expense_id: str = None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.expense_id = expense_id

        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 300)

        layout = QVBoxLayout(self)

        if self.expense_id:
            self.expense = expenseService.get_by_id(expense_id)
        else:
            self.expense = None

        self.init_info(layout)

        self.init_buttons(layout)

    def init_info(self, layout):
        """init info"""
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        # Name
        self.name_input = QLineEdit(self.expense.name if self.expense else "")
        form_layout.addRow(QLabel("Name:"), self.name_input)

        # Amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(1_000_000)
        self.amount_input.setValue(self.expense.amount if self.expense else 0.0)
        form_layout.addRow(QLabel("Amount:"), self.amount_input)

        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        if self.expense:
            y, m, d = map(int, self.expense.date.split("-"))
            self.date_input.setDate(QDate(y, m, d))
        else:
            self.date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Date:"), self.date_input)

        # Paid
        self.paid_checkbox = QCheckBox()
        self.paid_checkbox.setChecked(self.expense.payed if self.expense else False)
        self.paid_checkbox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

        form_layout.addRow(QLabel("Paid:"), self.paid_checkbox)

    def init_buttons(self, layout):
        """init buttons"""
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_expense)
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        if self.expense_id:
            deleted_btn = QPushButton("Deleted")
            deleted_btn.clicked.connect(self.deleted_expense)
            deleted_btn.setStyleSheet("background-color: red")
            layout.addWidget(deleted_btn)

    def save_expense(self):
        """save expenses"""

        new_data = {
            "name": self.name_input.text(),
            "amount": self.amount_input.value(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "payed": self.paid_checkbox.isChecked(),
        }

        if self.expense_id:
            expenseService.update(self.expense_id, **new_data)
        else:
            self.expense_id = expenseService.create(**new_data).expense_id
        self.expense_updated.emit(self.expense_id)
        self.close()

    def deleted_expense(self):
        """del expense"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            expenseService.delete(self.expense_id)
            self.expense_deleted.emit(self.expense_id)
            self.accept()
