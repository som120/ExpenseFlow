import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TransactionType(str, enum.Enum):
    PERSONAL = "personal"
    SHARED = "shared"
    BORROWED = "borrowed"
    INCOME = "income"


transaction_type_sql_enum = Enum(
    TransactionType,
    name="transactiontype",
    values_callable=lambda enum_cls: [item.value for item in enum_cls],
    validate_strings=True,
)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    category_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("categories.id"), nullable=True)
    transaction_type: Mapped[TransactionType] = mapped_column(transaction_type_sql_enum, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    my_share: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    payment_owner: Mapped[str] = mapped_column(String(120), nullable=False, default="self")
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    participants = relationship(
        "TransactionParticipant",
        back_populates="transaction",
        cascade="all, delete-orphan",
    )


class TransactionParticipant(Base):
    __tablename__ = "transaction_participants"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("transactions.id"), nullable=False)
    friend_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("friends.id"), nullable=True)
    participant_name: Mapped[str] = mapped_column(String(120), nullable=False)
    share_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    pending_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    transaction = relationship("Transaction", back_populates="participants")
    friend = relationship("Friend", back_populates="participants")
