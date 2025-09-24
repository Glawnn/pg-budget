import pytest

from pg_budget.core.services.expenses_plan_service import ExpensesPlanService


class FakeExpense:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__


class FakeExpensesPlan:
    def __init__(
        self,
        expensesplan_id=1,
        name="Plan",
        description="desc",
        amount=100,
        category_id=10,
        start_date="2023-01-01",
        end_date="2023-03-31",
        due_date="2023-01-15",
        frequency="monthly",
    ):
        self.expensesplan_id = expensesplan_id
        self.name = name
        self.description = description
        self.amount = amount
        self.category_id = category_id
        self.start_date = start_date
        self.end_date = end_date
        self.due_date = due_date
        self.frequency = frequency

    def to_dict(self):
        return self.__dict__


class TestExpensesPlanService:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        mocker.patch("pg_budget.core.services.expenses_plan_service.ExpensesPlan", FakeExpensesPlan)
        mocker.patch("pg_budget.core.services.expenses_plan_service.Expense", FakeExpense)
        self.service = ExpensesPlanService()
        self.service.model_key = "expensesplans"
        self.service.model_key_id = "expensesplan_id"

        self.mock_create_expense = mocker.patch.object(self.service.expense_service, "create")

    def test_generate_expenses_monthly(self):
        plan = FakeExpensesPlan(
            start_date="2023-01-01", end_date="2023-03-31", due_date="2023-01-15", frequency="monthly"
        )
        expenses = self.service._generate_expenses(plan)
        assert len(expenses) == 3  # Jan, Feb, Mar
        assert all(isinstance(e, FakeExpense) for e in expenses)

    def test_generate_expenses_quarterly(self):
        plan = FakeExpensesPlan(
            start_date="2023-01-01", end_date="2023-12-31", due_date="2023-01-15", frequency="quarterly"
        )
        expenses = self.service._generate_expenses(plan)
        assert len(expenses) == 4  # Jan, Apr, Jul, Oct

    def test_generate_expenses_yearly(self):
        plan = FakeExpensesPlan(
            start_date="2023-01-01", end_date="2025-12-31", due_date="2023-01-15", frequency="yearly"
        )
        expenses = self.service._generate_expenses(plan)
        assert len(expenses) == 3  # 2023, 2024, 2025

    def test_generate_expenses_invalid_frequency(self):
        plan = FakeExpensesPlan(frequency="weekly")
        with pytest.raises(ValueError):
            self.service._generate_expenses(plan)

    def test_create_calls_expense_service(self, mocker):
        mocker.patch(
            "pg_budget.core.services.expenses_plan_service.CRUDService.create", return_value=FakeExpensesPlan()
        )

        plan = self.service.create(name="TestPlan")
        assert isinstance(plan, FakeExpensesPlan)
        assert self.mock_create_expense.call_count > 0
