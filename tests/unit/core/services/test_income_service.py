import pytest
from datetime import datetime

from pg_budget.core.services.income_service import IncomeService


class FakeIncome:
    def __init__(self, name=None, income_id=None, category_id=None, date=None, amount=None):
        self.name = name
        self.income_id = income_id
        self.category_id = category_id
        self.date = date
        self.amount = amount

    def to_dict(self):
        return {
            "name": self.name,
            "income_id": self.income_id,
            "category_id": self.category_id,
            "date": self.date,
            "amount": self.amount,
        }


class TestIncomeService:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        mocker.patch("pg_budget.core.services.expense_service.Expense", FakeIncome)
        self.service = IncomeService()
        self.service.model_key = "incomes"

    def test_get_by_category(self, mocker):
        incomes = [
            {
                "name": "Income 1",
                "income_id": 1,
                "category_id": 10,
                "date": "2023-05-10",
                "amount": 50,
            },
            {
                "name": "Income 2",
                "income_id": 2,
                "category_id": 20,
                "date": "2023-05-11",
                "amount": 30,
            },
        ]
        mocker.patch.object(self.service, "get_all", return_value=incomes)

        result = self.service.get_by_category(10)
        assert len(result) == 1
        assert result[0].category_id == 10

    def test_get_by_month(self, mocker):
        incomes = [
            {
                "name": "Income 1",
                "income_id": 1,
                "category_id": 10,
                "date": "2023-05-10",
                "amount": 50,
            },
            {
                "name": "Income 2",
                "income_id": 2,
                "category_id": 20,
                "date": "2023-06-11",
                "amount": 30,
            },
        ]
        mocker.patch.object(self.service, "get_all", return_value=incomes)

        result = self.service.get_by_month(2023, 5)
        assert len(result) == 1
        assert datetime.strptime(result[0].date, "%Y-%m-%d").month == 5
