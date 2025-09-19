"""Custom table for ExpensePlan"""

from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QDoubleSpinBox,
    QDateEdit,
    QLabel,
)
from PySide6.QtCore import QDate

from pg_budget.core.models.expenses_plan import ExpensesPlan
from pg_budget.core.services import expensesPlanService
from pg_budget.gui.utils import safe_callback
from pg_budget.gui.widgets.base.base_dialog import BaseDialog
from pg_budget.gui.widgets.base.base_table import BaseTable
from pg_budget.gui.widgets.expense_plan_row import ExpensesPlanRow
from pg_budget.gui.widgets.text_edit import TextEdit


class ExpensesPlanTable(BaseTable):
    """class for table expenses plans table"""

    def __init__(self):
        super().__init__(ExpensesPlanRow)

    def _init_row_connections(self, row):
        row.row_clicked.connect(safe_callback(lambda eid=row.row_id: self._show_expenses_plan_detail(eid)))

    def _show_expenses_plan_detail(self, expenses_plan_id):
        dialog = ExpensesPlanDialog(parent=self.window(), expenses_plan_id=expenses_plan_id)
        dialog.updated.connect(safe_callback(lambda eid: self.updated_table.emit()))
        dialog.exec()


class ExpensesPlanDialog(BaseDialog):
    """Expenses plan dialog"""

    def __init__(self, expenses_plan_id=None, parent=None):
        super().__init__(expenses_plan_id, parent, fixed_size=(300, 300))

    def _init_form(self, form_layout):
        expenses_plan: ExpensesPlan = expensesPlanService.get_by_id(self.entity_id)

        self.name_input = QLineEdit(expenses_plan.name if expenses_plan else "")
        form_layout.addRow(QLabel("Name:"), self.name_input)

        self.description_input = TextEdit(
            expenses_plan.description if expenses_plan else "", lines_number=3, max_chars=120
        )
        form_layout.addRow(QLabel("Description"), self.description_input)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(1_000_000)
        self.amount_input.setValue(expenses_plan.amount if expenses_plan else 0.0)
        form_layout.addRow(QLabel("Amount:"), self.amount_input)

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        if expenses_plan:
            y, m, d = map(int, expenses_plan.start_date.split("-"))
            self.start_date_input.setDate(QDate(y, m, d))
        else:
            self.start_date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Start date:"), self.start_date_input)

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        if expenses_plan:
            y, m, d = map(int, expenses_plan.end_date.split("-"))
            self.end_date_input.setDate(QDate(y, m, d))
        else:
            self.end_date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("End date:"), self.end_date_input)

        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        if expenses_plan:
            y, m, d = map(int, expenses_plan.due_date.split("-"))
            self.due_date_input.setDate(QDate(y, m, d))
        else:
            self.due_date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Due date:"), self.due_date_input)

        self.frequency_input = QComboBox()
        self.frequency_input.addItems(["monthly", "quarterly", "yearly"])
        if expenses_plan:
            index = self.frequency_input.findText(expenses_plan.frequency)
            if index >= 0:
                self.frequency_input.setCurrentIndex(index)
        form_layout.addRow(QLabel("Frequency:"), self.frequency_input)

    def _on_save_btn_clicked(self):
        new_data = {
            "name": self.name_input.text(),
            "description": self.description_input.get_text(),
            "amount": self.amount_input.value(),
            "start_date": self.start_date_input.date().toString("yyyy-MM-dd"),
            "end_date": self.end_date_input.date().toString("yyyy-MM-dd"),
            "due_date": self.due_date_input.date().toString("yyyy-MM-dd"),
            "frequency": self.frequency_input.currentText(),
        }

        if self.entity_id:
            expensesPlanService.update(self.entity_id, **new_data)
        else:
            self.entity_id = expensesPlanService.create(**new_data).expensesplan_id
        self.updated.emit(self.entity_id)
        self.close()

    def _delete_entity(self):
        expensesPlanService.delete(self.entity_id)
