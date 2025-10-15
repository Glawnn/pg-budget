"""Module defining expense categories using an enumeration."""

from dataclasses import dataclass
from typing import Optional
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
    """Initialize the category database table."""
    expense_categories = [
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

    json_categories = [category.to_dict() for category in expense_categories]
    return json_categories
