"""Expense Plan model"""

import uuid
from dataclasses import dataclass, field
from typing import Literal

from pg_budget.core.models.base_model import BaseModel


@dataclass
class ExpensesPlan(BaseModel):  # pylint: disable=too-many-instance-attributes
    """Expense Plan model"""

    amount: float
    name: str

    start_date: str
    end_date: str
    due_date: str | None = None
    frequency: Literal["monthly", "quarterly", "yearly"] = "monthly"

    description: str | None = None
    category_id: str | None = None

    expensesplan_id: str | None = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if not self.due_date:
            self.due_date = self.start_date
