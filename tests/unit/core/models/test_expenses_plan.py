from pg_budget.core.models import ExpensesPlan


class TestExpenseModel:
    def test_expenses_plan_initialization(self):
        expenses_plan = ExpensesPlan(
            name="Netflix Subscription",
            start_date="2025-01-01",
            end_date="2025-12-31",
            amount=100.55,
            description="Weekly grocery shopping",
        )
        assert expenses_plan.amount == 100.55
        assert expenses_plan.name == "Netflix Subscription"
        assert expenses_plan.description == "Weekly grocery shopping"
        assert expenses_plan.end_date == "2025-12-31"
        assert expenses_plan.start_date == "2025-01-01"
        assert expenses_plan.expensesplan_id is not None
