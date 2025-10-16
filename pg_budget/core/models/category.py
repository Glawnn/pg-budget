"""Module defining expense categories using an enumeration."""

from dataclasses import dataclass
from typing import List, Optional
from pg_budget.core.models.base_model import BaseModel


@dataclass
class Category(BaseModel):
    """Expense categories model"""

    category_id: str
    category_type: str  # 'expense'
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


def init_category_db():
    categories: List[Category] = []
    categories.extend(base_expense_categories())
    categories.extend(base_income_categories())

    json_categories = [category.to_dict() for category in categories]
    return json_categories


def base_expense_categories():
    """Initialize the category database table."""
    return [
        Category(
            category_id="housing",
            category_type="expense",
            name="Housing",
            description="Rent, mortgage, utilities, and home-related costs",
            color="#4F46E5",
            icon="home",
        ),
        Category(
            category_id="transport",
            category_type="expense",
            name="Transport",
            description="Fuel, public transport, car maintenance, parking",
            color="#F59E0B",
            icon="car",
        ),
        Category(
            category_id="food",
            category_type="expense",
            name="Food",
            description="Groceries, restaurants, takeout, and coffee",
            color="#EF4444",
            icon="utensils",
        ),
        Category(
            category_id="subscriptions",
            category_type="expense",
            name="Subscriptions",
            description="Streaming services, phone plans, software subscriptions",
            color="#10B981",
            icon="credit-card",
        ),
        Category(
            category_id="health",
            category_type="expense",
            name="Health",
            description="Medicine, doctor visits, gym memberships",
            color="#3B82F6",
            icon="heart-pulse",
        ),
        Category(
            category_id="leisure",
            category_type="expense",
            name="Leisure",
            description="Movies, hobbies, vacations, and entertainment",
            color="#EC4899",
            icon="gamepad",
        ),
        Category(
            category_id="clothing",
            category_type="expense",
            name="Clothing",
            description="Apparel, shoes, accessories, laundry",
            color="#F97316",
            icon="shopping-bag",
        ),
        Category(
            category_id="taxes",
            category_type="expense",
            name="Taxes",
            description="Taxes, fees, and government-related payments",
            color="#DC2626",
            icon="file-text",
        ),
        Category(
            category_id="pets",
            category_type="expense",
            name="Pets",
            description="Pet food, vet visits, and pet accessories",
            color="#EAB308",
            icon="paw-print",
        ),
        Category(
            category_id="other",
            category_type="expense",
            name="Other",
            description="Miscellaneous or uncategorized expenses",
            color="#6B7280",
            icon="ellipsis-horizontal",
        ),
    ]


def base_income_categories():
    """Initialize the income category database table."""
    return [
        Category(
            category_id="salary",
            category_type="income",
            name="Salary",
            description="Income from your main or secondary job",
            color="#10B981",
            icon="wallet",
        ),
        Category(
            category_id="investments",
            category_type="income",
            name="Investments",
            description="Dividends, interest, stock profits, crypto gains, etc.",
            color="#F59E0B",
            icon="trending-up",
        ),
        Category(
            category_id="rental",
            category_type="income",
            name="Rental Income",
            description="Income from renting out properties or assets",
            color="#8B5CF6",
            icon="home",
        ),
        Category(
            category_id="business",
            category_type="income",
            name="Business",
            description="Earnings from your business, shop, or company",
            color="#EF4444",
            icon="building-2",
        ),
        Category(
            category_id="gifts",
            category_type="income",
            name="Gifts",
            description="Money received as gifts, inheritances, or donations",
            color="#EC4899",
            icon="gift",
        ),
        Category(
            category_id="other_income",
            category_type="income",
            name="Other Income",
            description="Miscellaneous or uncategorized income",
            color="#6B7280",
            icon="ellipsis-horizontal",
        ),
    ]
