"""expense service"""

from datetime import datetime

from pg_budget.core import logger
from pg_budget.core.models.category import Category
from pg_budget.core.models.expense import Expense
from pg_budget.core.services.crud_services import CRUDService


class ExpenseService(CRUDService):
    """expense service"""

    def __init__(self):
        super().__init__(Expense)
        self.categoryService = CRUDService(Category, "categories")

    def get_by_category(self, category_id):
        """get expense by category"""
        all_expenses = self.get_all()
        filtered = [Expense(**expense) for expense in all_expenses if expense["category_id"] == category_id]
        logger.debug("Filtered %d expenses for category_id=%s", len(filtered), category_id)
        return filtered

    def get_by_plan(self, plan_id):
        """get expense by plan"""
        all_expenses = self.get_all()

        filtered = [Expense(**expense) for expense in all_expenses if expense["plan_id"] == plan_id]
        logger.debug("Filtered %d expenses for plan_id=%s", len(filtered), plan_id)
        return filtered

    def get_by_month(self, year: int, month: int):
        """get all expenses for a month"""
        all_expenses = self.get_all()
        filtered_expenses = []
        for expense in all_expenses:
            date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if date.year == year and date.month == month:
                filtered_expenses.append(Expense(**expense))
        logger.debug("Filtered %d expenses for %04d-%02d", len(filtered_expenses), year, month)
        return filtered_expenses

    def get_categories(self):
        """get all categories"""
        categories = self.categoryService.get_all()
        logger.debug("Retrieved %d categories", len(categories))
        return [Category(**category) for category in categories if category["category_type"] == "expense"]


expense_service = ExpenseService()
