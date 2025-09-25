"""Widget for expenses Stats"""

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel
from PySide6.QtCore import Qt


class ExpensesStats(QFrame):
    """Class Widget for expenses stats"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QGridLayout()
        self.setLayout(self._layout)

        self.total_label = QLabel("Total: 0 €")
        self.total_label.setObjectName("TotalLabel")
        self.remaining_count_label = QLabel("Remaining Expenses: 0")
        self.remaining_count_label.setObjectName("RemainingCountLabel")
        self.remaining_label = QLabel("Remaining: 0 €")
        self.remaining_label.setObjectName("RemainingLabel")
        self.already_paid_label = QLabel("Already Paid: 0 €")
        self.already_paid_label.setObjectName("AlreadyPaidLabel")

        self._layout.addWidget(self.total_label, 0, 0, alignment=Qt.AlignCenter)
        self._layout.addWidget(self.already_paid_label, 0, 1, alignment=Qt.AlignCenter)
        self._layout.addWidget(self.remaining_count_label, 1, 0, alignment=Qt.AlignCenter)
        self._layout.addWidget(self.remaining_label, 1, 1, alignment=Qt.AlignCenter)

    def update_stats(self, expenses: list):
        """update stats with list of expenses"""
        if not expenses:
            self.total_label.setText("Total: 0 €")
            self.already_paid_label.setText("Already Paid: 0 €")
            self.remaining_count_label.setText("Remaining Expenses: 0")
            self.remaining_label.setText("Remaining: 0 €")
            return

        total_amount = sum(expense.amount for expense in expenses)
        already_paid_amount = sum(expense.amount for expense in expenses if expense.payed)
        remaining_amount = total_amount - already_paid_amount
        remaining_count = sum(1 for expense in expenses if not expense.payed)

        self.total_label.setText(f"Total: {total_amount:.2f} €")
        self.already_paid_label.setText(f"Already Paid: {already_paid_amount:.2f} €")
        self.remaining_count_label.setText(f"Remaining Expenses: {remaining_count}")
        self.remaining_label.setText(f"Remaining: {remaining_amount:.2f} €")
