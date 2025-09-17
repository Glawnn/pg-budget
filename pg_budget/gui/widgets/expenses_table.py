from PySide6.QtWidgets import QWidget, QMessageBox, QCheckBox, QVBoxLayout, QFormLayout, QScrollArea, QLineEdit, QDoubleSpinBox, QDateEdit, QCheckBox, QPushButton, QHBoxLayout, QPushButton, QFrame, QHBoxLayout, QLabel, QSizePolicy, QDialog
from PySide6.QtCore import Qt, Signal, QDate

from pg_budget.core.models import Expense
from pg_budget.core.services import expenseService
from pg_budget.gui.widgets.base import BaseRow, RowField
from pg_budget.gui.widgets.base.base_table import BaseTable


class ExpenseRow(BaseRow):
    paid_changed = Signal(bool)

    def __init__(self, expense: Expense, parent=None):
        
        fields = [
            RowField("Name", value=expense.name),
            RowField("Amount", value=f"{expense.amount:.2f} €"),
            RowField("Date", value=expense.date),
            RowField("Paid", type=QCheckBox, value=expense.payed)
        ]

        super().__init__(fields, expense.expense_id , parent)

    def _init_connections(self):
        paid_checkbox: QCheckBox = self.get_widget_by_name("Paid")
        if paid_checkbox:
            paid_checkbox.stateChanged.connect(lambda state: self.paid_changed.emit(state == 2))

class ExpensesTable2(BaseTable):
    updated_table = Signal()
    def __init__(self):
        super().__init__(ExpenseRow)

    def _init_row_connections(self, row):
        row.paid_changed.connect(lambda value, eid=row.row_id: self._on_paid_changed(eid, value))

    def _on_paid_changed(self, expense_id: str, paid: bool):
        expenseService.update(expense_id, payed=paid)
        self.updated_table.emit()

class ExpensesTable(QFrame):
    updated_table = Signal()

    def __init__(self):
        super().__init__()

        self.selected_year = None
        self.selected_month = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(5)
        scroll.setWidget(self.container)

        self.rows: list[ExpenseRow] = []
        self.expenses: list[Expense] = []
   

    def clear(self):
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)  # détache du layout
        self.rows = []
        self.expenses = []

    def load_month(self, year: int, month: int):
        self.clear()
        self.selected_year = year
        self.selected_month = month
        
        self.expenses = expenseService.get_by_month(year, month)

        for expense in self.expenses:
            row = ExpenseRow(expense)

            row.paid_changed.connect(lambda value, eid=expense.expense_id: self._on_paid_changed(eid, value))
            row.row_clicked.connect(lambda eid=expense.expense_id: self.show_expense_detail(eid))

            self.container_layout.addWidget(row)
            self.rows.append(row)

        self.container_layout.setAlignment(Qt.AlignTop)
        self.updated_table.emit()

        # resizing
        if self.rows:
            column_keys = [name for name, widget in self.rows[0].widgets]
            max_widths = {key: 0 for key in column_keys}

            # Calculer la largeur max de chaque colonne
            for row in self.rows:
                for w_name, widget in row.widgets:
                    widget_width = widget.sizeHint().width()
                    if widget_width > max_widths[w_name]:
                        max_widths[w_name] = widget_width

            for row in self.rows:
                row.resize_columns(max_widths)

    def _on_paid_changed(self, expense_id: str, paid: bool):
        expenseService.update(expense_id, payed=paid)

        for exp in self.expenses:
            if exp.expense_id == expense_id:
                exp.payed = paid
                break

        self.updated_table.emit()

    def show_expense_detail(self, expense_id):
        dialog = ExpenseDialog(parent=self.window(), expense_id=expense_id)
        dialog.expense_updated.connect(lambda eid: self.load_month(self.selected_year, self.selected_month))
        dialog.expense_deleted.connect(lambda eid: self.load_month(self.selected_year, self.selected_month))
        dialog.exec()

    def get_data(self):
        return {
            "total": sum(exp.amount for exp in self.expenses),
            "remaining": sum(exp.amount for exp in self.expenses if not exp.payed)
        }


    
class ExpenseDialog(QDialog):
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
            y, m, d = map(int, self.expense.date.split('-'))
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

        new_data = {
            "name": self.name_input.text(),
            "amount": self.amount_input.value(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "payed": self.paid_checkbox.isChecked()
        }

        if self.expense_id:
            expenseService.update(self.expense_id, **new_data)
        else:
            self.expense_id = expenseService.create(**new_data).expense_id
        self.expense_updated.emit(self.expense_id)
        self.close()

    def deleted_expense(self):
        reply = QMessageBox.question(
        self,
            "Confirmation",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            expenseService.delete(self.expense_id)
            self.expense_deleted.emit(self.expense_id)
            self.accept() 