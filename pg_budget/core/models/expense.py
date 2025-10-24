"""Expense model"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from pg_budget.core.models.base_model import BaseModel


@dataclass
class Expense(BaseModel):  # pylint: disable=too-many-instance-attributes
    """Expense model"""

    amount: float
    name: str
    description: str | None = None
    category_id: str | None = None
    plan_id: str | None = None
    expense_id: str | None = field(default_factory=lambda: str(uuid.uuid4()))
    date: str | None = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    payed: bool = False
