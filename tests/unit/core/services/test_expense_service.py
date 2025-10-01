import pytest
from datetime import datetime

from pg_budget.core.services.expense_service import ExpenseService


class FakeExpense:
    def __init__(self, expense_id=None, category_id=None, plan_id=None, date=None, amount=None):
        self.expense_id = expense_id
        self.category_id = category_id
        self.plan_id = plan_id
        self.date = date
        self.amount = amount

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "category_id": self.category_id,
            "plan_id": self.plan_id,
            "date": self.date,
            "amount": self.amount,
        }


class TestExpenseService:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        mocker.patch("pg_budget.core.services.expense_service.Expense", FakeExpense)
        self.service = ExpenseService()
        self.service.model_key = "expenses"
        self.service.model_key_id = "expense_id"

    def test_get_by_category(self, mocker):
        expenses = [
            {
                "expense_id": 1,
                "category_id": 10,
                "plan_id": 100,
                "date": "2023-05-10",
                "amount": 50,
            },
            {
                "expense_id": 2,
                "category_id": 20,
                "plan_id": 100,
                "date": "2023-05-11",
                "amount": 30,
            },
        ]
        mocker.patch.object(self.service, "get_all", return_value=expenses)

        result = self.service.get_by_category(10)
        assert len(result) == 1
        assert result[0].category_id == 10

    def test_get_by_plan(self, mocker):
        expenses = [
            {
                "expense_id": 1,
                "category_id": 10,
                "plan_id": 200,
                "date": "2023-05-10",
                "amount": 50,
            },
            {
                "expense_id": 2,
                "category_id": 20,
                "plan_id": 300,
                "date": "2023-05-11",
                "amount": 30,
            },
        ]
        mocker.patch.object(self.service, "get_all", return_value=expenses)

        result = self.service.get_by_plan(200)
        assert len(result) == 1
        assert result[0].plan_id == 200

    def test_get_by_month(self, mocker):
        expenses = [
            {
                "expense_id": 1,
                "category_id": 10,
                "plan_id": 200,
                "date": "2023-05-10",
                "amount": 50,
            },
            {
                "expense_id": 2,
                "category_id": 20,
                "plan_id": 300,
                "date": "2023-06-11",
                "amount": 30,
            },
        ]
        mocker.patch.object(self.service, "get_all", return_value=expenses)

        result = self.service.get_by_month(2023, 5)
        assert len(result) == 1
        assert datetime.strptime(result[0].date, "%Y-%m-%d").month == 5
