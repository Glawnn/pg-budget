"""Income model"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from pg_budget.core.models.base_model import BaseModel


@dataclass
class Income(BaseModel):
    """Income model"""

    amount: float
    name: str
    description: str | None = None
    category_id: str | None = None
    income_id: str | None = field(default_factory=lambda: str(uuid.uuid4()))
    date: str | None = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
