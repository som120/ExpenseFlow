import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.transaction import TransactionType


class TransactionParticipantBase(BaseModel):
    friend_id: uuid.UUID | None = None
    participant_name: str = Field(min_length=1, max_length=120)
    share_amount: Decimal = Field(gt=0, decimal_places=2)
    status: str = Field(default="pending", max_length=20)
    pending_amount: Decimal = Field(ge=0, decimal_places=2)


class TransactionParticipantCreate(TransactionParticipantBase):
    pass


class TransactionParticipantRead(TransactionParticipantBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    paid_at: datetime | None = None
    created_at: datetime


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    category_name: str | None = Field(default=None, max_length=100)
    amount: Decimal = Field(gt=0, decimal_places=2)
    my_share: Decimal = Field(ge=0, decimal_places=2)
    description: str = Field(min_length=1)
    payment_owner: str = Field(default="self", max_length=120)
    transaction_date: date
    participants: list[TransactionParticipantCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_share(self):
        if self.my_share > self.amount:
            raise ValueError("my_share cannot exceed amount")

        if self.transaction_type == TransactionType.PERSONAL and self.my_share != self.amount:
            raise ValueError("Personal expenses must use full amount as my_share")
        return self


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    transaction_type: TransactionType | None = None
    category_name: str | None = Field(default=None, max_length=100)
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    my_share: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    description: str | None = Field(default=None, min_length=1)
    payment_owner: str | None = Field(default=None, max_length=120)
    transaction_date: date | None = None
    participants: list[TransactionParticipantCreate] | None = None


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    transaction_type: TransactionType
    amount: Decimal
    my_share: Decimal
    description: str
    payment_owner: str
    transaction_date: date
    created_at: datetime
    updated_at: datetime
    category_name: str | None = None
    participants: list[TransactionParticipantRead]
