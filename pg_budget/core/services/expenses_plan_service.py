"""expanse plan service"""

from datetime import datetime

from dateutil.relativedelta import relativedelta

from pg_budget.core import logger
from pg_budget.core.models.expense import Expense
from pg_budget.core.models.expenses_plan import ExpensesPlan
from pg_budget.core.services.crud_services import CRUDService
from pg_budget.core.services.expense_service import ExpenseService


class ExpensesPlanService(CRUDService):
    """expanse plan service"""

    def __init__(self):
        super().__init__(ExpensesPlan)
        self.expense_service = ExpenseService()

    def create(self, **kwargs):
        """custom create plan"""
        plan = super().create(**kwargs)
        logger.info("Created new expense plan: %s", plan.name)

        expenses = self._generate_expenses(plan)

        logger.debug("Generated %d expenses for plan '%s'", len(expenses), plan.name)

        for expense in expenses:
            self.expense_service.create(**expense.to_dict())
            logger.debug("Created expense '%s' on %s", expense.name, expense.date)

        return plan

    def _generate_expenses(self, plan: ExpensesPlan):
        expenses = []
        start = datetime.strptime(plan.start_date, "%Y-%m-%d")
        end = datetime.strptime(plan.end_date, "%Y-%m-%d")
        due = datetime.strptime(plan.due_date, "%Y-%m-%d")

        current = due

        while current <= end:
            if current >= start:
                expenses.append(
                    Expense(
                        amount=plan.amount,
                        name=plan.name,
                        description=plan.description,
                        category_id=plan.category_id,
                        plan_id=plan.expensesplan_id,
                        date=current.strftime("%Y-%m-%d"),
                    )
                )

            if plan.frequency == "monthly":
                current += relativedelta(months=1)
            elif plan.frequency == "quarterly":
                current += relativedelta(months=3)
            elif plan.frequency == "yearly":
                current += relativedelta(years=1)
            else:
                logger.error("Unknown frequency '%s' for plan '%s'", plan.frequency, plan.name)
                raise ValueError(f"Unknown frequency: {plan.frequency}")

        return expenses


expenses_plan_service = ExpensesPlanService()
