"""Expense model"""

from dataclasses import dataclass, field
from typing import Optional
import uuid
from datetime import datetime

from pg_budget.core.models.base_model import BaseModel


@dataclass
class Expense(BaseModel):  # pylint: disable=too-many-instance-attributes
    """Expense model"""

    amount: float
    name: str
    description: Optional[str] = None
    category_id: Optional[str] = None
    plan_id: Optional[str] = None
    expense_id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))
    date: Optional[str] = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    payed: bool = False
