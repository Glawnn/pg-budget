"""Custom table for ExpensePlan"""

from PySide6.QtWidgets import (
    QMessageBox,
    QComboBox,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDoubleSpinBox,
    QDateEdit,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QDialog,
)
from PySide6.QtCore import Qt, Signal, QDate

from pg_budget.core.models.expenses_plan import ExpensesPlan
from pg_budget.core.services import expensesPlanService
from pg_budget.gui.widgets.base.base_table import BaseTable
from pg_budget.gui.widgets.expense_plan_row import ExpensesPlanRow


class ExpensesPlanTable(BaseTable):
    """class for table expenses plans table"""

    def __init__(self):
        super().__init__(ExpensesPlanRow)

    def _init_row_connections(self, row):
        row.row_clicked.connect(lambda eid=row.row_id: self._show_expenses_plan_detail(eid))

    def _show_expenses_plan_detail(self, expenses_plan_id):
        dialog = ExpensesPlanDialog(parent=self.window(), expenses_plan_id=expenses_plan_id)
        dialog.expenses_plan_updated.connect(lambda epid: self.updated_table.emit())
        dialog.expenses_plan_deleted.connect(lambda epid: self.updated_table.emit())
        dialog.exec()


class ExpensesPlanDialog(QDialog):  # pylint: disable=too-many-instance-attributes
    """dialog"""

    expenses_plan_deleted = Signal(str)
    expenses_plan_updated = Signal(str)

    def __init__(self, parent=None, expenses_plan_id: str = None):
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.expenses_plan_id = expenses_plan_id

        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 300)

        layout = QVBoxLayout(self)

        if self.expenses_plan_id:
            self.expenses_plan: ExpensesPlan = expensesPlanService.get_by_id(self.expenses_plan_id)
        else:
            self.expenses_plan = None

        self.init_info(layout)

        self.init_buttons(layout)

    def init_info(self, layout):
        """tmp"""
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        # Name
        self.name_input = QLineEdit(self.expenses_plan.name if self.expenses_plan else "")
        form_layout.addRow(QLabel("Name:"), self.name_input)

        # Description
        self.description_input = QLineEdit(self.expenses_plan.description if self.expenses_plan else "")
        form_layout.addRow(QLabel("Description:"), self.description_input)

        # Amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(1_000_000)
        self.amount_input.setValue(self.expenses_plan.amount if self.expenses_plan else 0.0)
        form_layout.addRow(QLabel("Amount:"), self.amount_input)

        # Start Date
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        if self.expenses_plan:
            y, m, d = map(int, self.expenses_plan.start_date.split("-"))
            self.start_date_input.setDate(QDate(y, m, d))
        else:
            self.start_date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Date:"), self.start_date_input)

        # End Date
        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        if self.expenses_plan:
            y, m, d = map(int, self.expenses_plan.end_date.split("-"))
            self.end_date_input.setDate(QDate(y, m, d))
        else:
            self.end_date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Date:"), self.end_date_input)

        # Due date
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        if self.expenses_plan:
            y, m, d = map(int, self.expenses_plan.due_date.split("-"))
            self.due_date_input.setDate(QDate(y, m, d))
        else:
            self.due_date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Date:"), self.due_date_input)

        # Frequency
        self.frequency_input = QComboBox()
        self.frequency_input.addItems(["monthly", "quarterly", "yearly"])

        if self.expenses_plan:
            index = self.frequency_input.findText(self.expenses_plan.frequency)
            if index >= 0:
                self.frequency_input.setCurrentIndex(index)

        form_layout.addRow(QLabel("Frequency:"), self.frequency_input)

    def init_buttons(self, layout):
        """tmp"""
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_expenses_plan)
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        if self.expenses_plan_id:
            deleted_btn = QPushButton("Deleted")
            deleted_btn.clicked.connect(self.deleted_expenses_plan)
            deleted_btn.setStyleSheet("background-color: red")
            layout.addWidget(deleted_btn)

    def save_expenses_plan(self):
        """tmp"""
        new_data = {
            "name": self.name_input.text(),
            "amount": self.amount_input.value(),
            "start_date": self.start_date_input.date().toString("yyyy-MM-dd"),
            "end_date": self.end_date_input.date().toString("yyyy-MM-dd"),
            "due_date": self.due_date_input.date().toString("yyyy-MM-dd"),
            "description": self.description_input.text(),
            "frequency": self.frequency_input.currentText(),
        }

        if self.expenses_plan_id:
            expensesPlanService.update(self.expenses_plan_id, **new_data)
        else:
            self.expenses_plan_id = expensesPlanService.create(**new_data).expensesplan_id
        self.expenses_plan_updated.emit(self.expenses_plan_id)
        self.close()

    def deleted_expenses_plan(self):
        """tmp"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this Plan?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            expensesPlanService.delete(self.expenses_plan_id)
            self.expenses_plan_deleted.emit(self.expenses_plan_id)
            self.accept()
