from pg_budget.core.models import Income


class TestIncomeModel:
    def test_expense_initialization(self):
        income = Income(amount=100.0, name="Sales Airbus", description="Monthly sales income")
        assert income.amount == 100.0
        assert income.name == "Sales Airbus"
        assert income.description == "Monthly sales income"
        assert income.income_id is not None
        assert income.date is not None
