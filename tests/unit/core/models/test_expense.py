
from pg_budget.core.models.expense import Expense



class TestExpenseModel:
    def test_expense_initialization(self):
        expense = Expense(amount=100.0, name="Groceries", description="Weekly grocery shopping")
        assert expense.amount == 100.0
        assert expense.name == "Groceries"
        assert expense.description == "Weekly grocery shopping"
        assert expense.expense_id is not None
        assert expense.date is not None