import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FriendBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    telegram_username: str | None = Field(default=None, max_length=120)
    phone: str | None = Field(default=None, max_length=30)
    notes: str | None = None


class FriendCreate(FriendBase):
    pass


class FriendUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    telegram_username: str | None = Field(default=None, max_length=120)
    phone: str | None = Field(default=None, max_length=30)
    notes: str | None = None


class FriendRead(FriendBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    total_owed_to_you: Decimal = Decimal("0.00")
    total_you_owe: Decimal = Decimal("0.00")
