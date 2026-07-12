import uuid
from datetime import date, datetime
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


class FriendTransactionHistoryItem(BaseModel):
    transaction_id: uuid.UUID
    transaction_date: date
    description: str
    transaction_type: str
    share_amount: Decimal
    pending_amount: Decimal
    status: str


class FriendDetailRead(FriendRead):
    history: list[FriendTransactionHistoryItem]


class FriendSettlementRequest(BaseModel):
    transaction_id: uuid.UUID | None = None
