


from dataclasses import dataclass, field
from typing import Optional
import uuid
from pg_budget.core.models.base_model import BaseModel
from datetime import datetime


@dataclass
class Expense(BaseModel):
        amount: float
        name: str
        description: Optional[str] = None
        category_id: Optional[str] = None
        plan_id: Optional[str] = None
        expense_id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))
        date: Optional[str] = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
        payed: bool = False


        