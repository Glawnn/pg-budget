"""Income Table"""

from typing import List
from PySide6.QtWidgets import QLineEdit, QDoubleSpinBox, QDateEdit, QLabel, QComboBox
from PySide6.QtCore import QDate


from pg_budget.core.models.category import Category
from pg_budget.core.models.income import Income
from pg_budget.core.services import incomeService
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.widgets.base.base_dialog import BaseDialog
from pg_budget.gui.widgets.base.base_table import BaseTable
from pg_budget.gui.widgets.income_row import IncomeRow
from pg_budget.gui.widgets.text_edit import TextEdit
from pg_budget.gui import logger


class IncomesTable(BaseTable):
    """Income table class"""

    def __init__(self):
        super().__init__(IncomeRow, default_filterable="Date")
        logger.debug("IncomesTable initialized")

    def _init_row_connections(self, row: IncomeRow):
        row.row_clicked.connect(safe_callback(lambda iid=row.row_id: self._show_income_detail(iid)))

    def _show_income_detail(self, iid):
        logger.info("Opening IncomeDialog for ID %s", iid)
        dialog = IncomeDialog(parent=self.window(), income_id=iid)
        dialog.updated.connect(safe_callback(lambda iid: self.updated_table.emit()))
        dialog.exec()
        logger.debug("IncomeDialog closed for ID %s", iid)


class IncomeDialog(BaseDialog):
    """Income dialog"""

    def __init__(self, income_id=None, parent=None):
        super().__init__(income_id, parent, fixed_size=(300, 300))
        if income_id:
            self.setWindowTitle("Update Income")
        else:
            self.setWindowTitle("Create Income")
        logger.debug("IncomeDialog %s, initialized with ID %s", self.windowTitle(), income_id)

    def _init_form(self, form_layout):
        income: Income = incomeService.get_by_id(self.entity_id) if self.entity_id else None
        categories: List[Category] = incomeService.get_categories()
        logger.info(
            "Loaded Income ID %s: %s",
            self.entity_id,
            income.__dict__ if income else "None",
        )

        self.name_input = QLineEdit(income.name if income else "")
        form_layout.addRow(QLabel("Name:"), self.name_input)

        self.description_input = TextEdit(income.description if income else "", lines_number=3, max_chars=120)
        form_layout.addRow(QLabel("Description"), self.description_input)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(1_000_000)
        self.amount_input.setValue(income.amount if income else 0.0)
        form_layout.addRow(QLabel("Amount:"), self.amount_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        if income:
            y, m, d = map(int, income.date.split("-"))
            self.date_input.setDate(QDate(y, m, d))
        else:
            self.date_input.setDate(QDate.currentDate())
        self.form_layout.addRow(QLabel("Date:"), self.date_input)

        self.category_combo = QComboBox()
        for cat in categories:
            self.category_combo.addItem(cat.name, cat.category_id)

        if income and getattr(income, "category_id", None):
            idx = self.category_combo.findData(income.category_id)
            if idx != -1:
                self.category_combo.setCurrentIndex(idx)

        form_layout.addRow(QLabel("Category:"), self.category_combo)

    def _on_save_btn_clicked(self):
        new_data = {
            "name": self.name_input.text(),
            "description": self.description_input.get_text(),
            "amount": self.amount_input.value(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "category_id": self.category_combo.currentData(),
        }

        if self.entity_id:
            incomeService.update(self.entity_id, **new_data)
            logger.info("Updated Income ID %s: %s", self.entity_id, new_data)
        else:
            self.entity_id = incomeService.create(**new_data).income_id
            logger.info("Created new Income ID %s: %s", self.entity_id, new_data)

        self.updated.emit(self.entity_id)
        logger.debug("IncomeDialog emit updated signal for ID %s", self.entity_id)
        self.close()
        logger.debug("IncomeDialog closed after save for ID %s", self.entity_id)

    def _delete_entity(self):
        incomeService.delete(self.entity_id)
        logger.info("Deleted Income ID %s", self.entity_id)
