"""Expense Plan model"""

from dataclasses import dataclass, field
from typing import Literal, Optional
import uuid
from pg_budget.core.models.base_model import BaseModel


@dataclass
class ExpensesPlan(BaseModel):  # pylint: disable=too-many-instance-attributes
    """Expense Plan model"""

    amount: float
    name: str

    start_date: str
    end_date: str
    due_date: Optional[str] = None
    frequency: Literal["monthly", "quarterly", "yearly"] = "monthly"

    description: Optional[str] = None
    category_id: Optional[str] = None

    expensesplan_id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if not self.due_date:
            self.due_date = self.start_date
