"""Expense Table"""

from PySide6.QtWidgets import (
    QLineEdit,
    QDoubleSpinBox,
    QDateEdit,
    QCheckBox,
    QLabel,
    QSizePolicy,
)
from PySide6.QtCore import QDate


from pg_budget.core.models.expense import Expense
from pg_budget.core.services import expenseService
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.widgets.base.base_dialog import BaseDialog
from pg_budget.gui.widgets.base.base_table import BaseTable
from pg_budget.gui.widgets.expense_row import ExpenseRow
from pg_budget.gui.widgets.text_edit import TextEdit


class ExpensesTable(BaseTable):
    """Expense table class"""

    def __init__(self):
        super().__init__(ExpenseRow)

    def _init_row_connections(self, row: ExpenseRow):
        row.paid_changed.connect(safe_callback(lambda value, eid=row.row_id: self._on_paid_changed(eid, value)))
        row.row_clicked.connect(safe_callback(lambda eid=row.row_id: self._show_expense_detail(eid)))

    def _on_paid_changed(self, expense_id: str, paid: bool):
        expenseService.update(expense_id, payed=paid)
        self.updated_table.emit()

    def _show_expense_detail(self, eid):
        dialog = ExpenseDialog(parent=self.window(), expense_id=eid)
        dialog.updated.connect(safe_callback(lambda eid: self.updated_table.emit()))
        dialog.exec()


class ExpenseDialog(BaseDialog):
    """Expense dialog"""

    def __init__(self, expense_id=None, parent=None):
        super().__init__(expense_id, parent, fixed_size=(300, 300))

    def _init_form(self, form_layout):
        expense: Expense = expenseService.get_by_id(self.entity_id) if self.entity_id else None

        self.name_input = QLineEdit(expense.name if expense else "")
        form_layout.addRow(QLabel("Name:"), self.name_input)

        self.description_input = TextEdit(expense.description if expense else "", lines_number=3, max_chars=120)
        form_layout.addRow(QLabel("Description"), self.description_input)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(1_000_000)
        self.amount_input.setValue(expense.amount if expense else 0.0)
        form_layout.addRow(QLabel("Amount:"), self.amount_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        if expense:
            y, m, d = map(int, expense.date.split("-"))
            self.date_input.setDate(QDate(y, m, d))
        else:
            self.date_input.setDate(QDate.currentDate())
        self.form_layout.addRow(QLabel("Date:"), self.date_input)

        self.paid_checkbox = QCheckBox()
        self.paid_checkbox.setChecked(expense.payed if expense else False)
        self.paid_checkbox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        form_layout.addRow(QLabel("Paid:"), self.paid_checkbox)

    def _on_save_btn_clicked(self):
        new_data = {
            "name": self.name_input.text(),
            "description": self.description_input.get_text(),
            "amount": self.amount_input.value(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "payed": self.paid_checkbox.isChecked(),
        }

        if self.entity_id:
            expenseService.update(self.entity_id, **new_data)
        else:
            self.entity_id = expenseService.create(**new_data).expense_id
        self.updated.emit(self.entity_id)
        self.close()

    def _delete_entity(self):
        expenseService.delete(self.entity_id)
