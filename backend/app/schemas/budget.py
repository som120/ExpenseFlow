import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    amount: Decimal = Field(gt=0, decimal_places=2)
    period: str = Field(default="monthly", max_length=20)
    category_name: str | None = Field(default=None, max_length=100)
    is_active: bool = True


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    period: str | None = Field(default=None, max_length=20)
    category_name: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class BudgetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    amount: Decimal
    period: str
    category_name: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    spent_amount: Decimal = Decimal("0.00")
    remaining_amount: Decimal = Decimal("0.00")
