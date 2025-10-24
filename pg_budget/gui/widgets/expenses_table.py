"""Expense Table"""

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QCheckBox, QComboBox, QDateEdit, QDoubleSpinBox, QLabel, QLineEdit, QSizePolicy

from pg_budget.core.models.category import Category
from pg_budget.core.models.expense import Expense
from pg_budget.core.services import expense_service
from pg_budget.gui import logger
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.widgets.base.base_dialog import BaseDialog
from pg_budget.gui.widgets.base.base_table import BaseTable
from pg_budget.gui.widgets.expense_row import ExpenseRow
from pg_budget.gui.widgets.text_edit import TextEdit


class ExpensesTable(BaseTable):
    """Expense table class"""

    def __init__(self):
        super().__init__(ExpenseRow, default_filterable="Date")
        logger.debug("ExpensesTable initialized")

    def _init_row_connections(self, row: ExpenseRow):
        row.paid_changed.connect(safe_callback(lambda value, eid=row.row_id: self._on_paid_changed(eid, value)))
        row.row_clicked.connect(safe_callback(lambda eid=row.row_id: self._show_expense_detail(eid)))

    def _on_paid_changed(self, expense_id: str, paid: bool):
        logger.info("Updating expense ID %s: payed=%s", expense_id, paid)
        expense_service.update(expense_id, payed=paid)
        self.updated_table.emit()
        logger.debug("Updated signal emitted for expense ID %s", expense_id)

    def _show_expense_detail(self, eid):
        logger.info("Opening ExpenseDialog for ID %s", eid)
        dialog = ExpenseDialog(parent=self.window(), expense_id=eid)
        dialog.updated.connect(safe_callback(lambda eid: self.updated_table.emit()))
        dialog.exec()
        logger.debug("ExpenseDialog closed for ID %s", eid)


class ExpenseDialog(BaseDialog):
    """Expense dialog"""

    def __init__(self, expense_id=None, parent=None):
        super().__init__(expense_id, parent, fixed_size=(300, 300))
        if expense_id:
            self.setWindowTitle("Update Expense")
        else:
            self.setWindowTitle("Create Expense")
        logger.debug("ExpenseDialog %s, initialized with ID %s", self.windowTitle(), expense_id)

    def _init_form(self, form_layout):
        expense: Expense = expense_service.get_by_id(self.entity_id) if self.entity_id else None
        categories: list[Category] = expense_service.get_categories()
        logger.info(
            "Loaded Expense ID %s: %s",
            self.entity_id,
            expense.__dict__ if expense else "None",
        )

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

        self.category_combo = QComboBox()
        for cat in categories:
            self.category_combo.addItem(cat.name, cat.category_id)

        if expense and getattr(expense, "category_id", None):
            idx = self.category_combo.findData(expense.category_id)
            if idx != -1:
                self.category_combo.setCurrentIndex(idx)

        form_layout.addRow(QLabel("Category:"), self.category_combo)

    def _on_save_btn_clicked(self):
        new_data = {
            "name": self.name_input.text(),
            "description": self.description_input.get_text(),
            "amount": self.amount_input.value(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "payed": self.paid_checkbox.isChecked(),
            "category_id": self.category_combo.currentData(),
        }

        if self.entity_id:
            expense_service.update(self.entity_id, **new_data)
            logger.info("Updated Expense ID %s: %s", self.entity_id, new_data)
        else:
            self.entity_id = expense_service.create(**new_data).expense_id
            logger.info("Created new Expense ID %s: %s", self.entity_id, new_data)

        self.updated.emit(self.entity_id)
        logger.debug("ExpenseDialog emit updated signal for ID %s", self.entity_id)
        self.close()
        logger.debug("ExpenseDialog closed after save for ID %s", self.entity_id)

    def _delete_entity(self):
        expense_service.delete(self.entity_id)
        logger.info("Deleted Expense ID %s", self.entity_id)
