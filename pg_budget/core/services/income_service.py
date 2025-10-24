from datetime import datetime

from pg_budget.core import logger
from pg_budget.core.models.category import Category
from pg_budget.core.models.income import Income
from pg_budget.core.services.crud_services import CRUDService


class IncomeService(CRUDService):
    """Income service"""

    def __init__(self):
        super().__init__(Income)
        self.categoryService = CRUDService(Category, "categories")

    def get_by_category(self, category_id):
        """get Income by category"""
        all_entries = self.get_all()
        filtered = [Income(**entry) for entry in all_entries if entry["category_id"] == category_id]
        logger.debug("Filtered %d income for category_id=%s", len(filtered), category_id)
        return filtered

    def get_by_month(self, year: int, month: int):
        """get all Income for a month"""
        all_entries = self.get_all()
        filtered_entries = []
        for entry in all_entries:
            date = datetime.strptime(entry["date"], "%Y-%m-%d")
            if date.year == year and date.month == month:
                filtered_entries.append(Income(**entry))
        logger.debug("Filtered %d expenses for %04d-%02d", len(filtered_entries), year, month)
        return filtered_entries

    def get_categories(self):
        """get all categories"""
        categories = self.categoryService.get_all()
        logger.debug("Retrieved %d categories", len(categories))
        return [Category(**category) for category in categories if category["category_type"] == "income"]


income_service = IncomeService()
