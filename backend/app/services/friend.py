from __future__ import annotations

import uuid
from datetime import UTC, date, datetime
from decimal import Decimal

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ExpenseFlowException
from app.models.friend import Friend
from app.repositories.friend import FriendRepository
from app.repositories.transaction import TransactionRepository
from app.models.transaction import TransactionType
from app.schemas.friend import (
    FriendCreate,
    FriendDetailRead,
    FriendRead,
    FriendSettlementRequest,
    FriendTransactionHistoryItem,
    FriendUpdate,
)


class FriendService:
    def __init__(self, db: Session):
        self.friends = FriendRepository(db)
        self.transactions = TransactionRepository(db)

    def create(self, payload: FriendCreate, user_id: uuid.UUID) -> Friend:
        friend = Friend(user_id=user_id, **payload.model_dump())
        return self.friends.create(friend)

    def list(self, user_id: uuid.UUID, from_date: date | None = None, to_date: date | None = None) -> list[FriendRead]:
        transactions = self.transactions.list(user_id)
        result = []
        for friend in self.friends.list(user_id):
            total_owed_to_you = Decimal("0.00")
            total_you_owe = Decimal("0.00")

            for transaction in transactions:
                if from_date and transaction.transaction_date < from_date:
                    continue
                if to_date and transaction.transaction_date > to_date:
                    continue

                for participant in transaction.participants:
                    if participant.friend_id != friend.id and participant.participant_name != friend.name:
                        continue
                    if transaction.transaction_type == TransactionType.SHARED:
                        total_owed_to_you += participant.pending_amount
                    elif transaction.transaction_type == TransactionType.BORROWED:
                        total_you_owe += participant.pending_amount

            result.append(
                FriendRead.model_validate(
                    {
                        **friend.__dict__,
                        "total_owed_to_you": total_owed_to_you,
                        "total_you_owe": total_you_owe,
                    }
                )
            )

        return result

    def update(self, friend_id: uuid.UUID, payload: FriendUpdate, user_id: uuid.UUID) -> FriendRead:
        friend = self.friends.get(friend_id, user_id)
        if not friend:
            raise ExpenseFlowException("Friend not found", status.HTTP_404_NOT_FOUND)

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(friend, field, value)

        updated = self.friends.save(friend)
        return FriendRead.model_validate(updated)

    def delete(self, friend_id: uuid.UUID, user_id: uuid.UUID) -> None:
        friend = self.friends.get(friend_id, user_id)
        if not friend:
            raise ExpenseFlowException("Friend not found", status.HTTP_404_NOT_FOUND)
        self.friends.delete(friend)

    def get_detail(
        self,
        friend_id: uuid.UUID,
        user_id: uuid.UUID,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> FriendDetailRead:
        friend = self.friends.get(friend_id, user_id)
        if not friend:
            raise ExpenseFlowException("Friend not found", status.HTTP_404_NOT_FOUND)

        balances = self.list(user_id, from_date=from_date, to_date=to_date)
        balance = next((item for item in balances if item.id == friend_id), None)
        history = self._build_history(friend, user_id, from_date=from_date, to_date=to_date)

        return FriendDetailRead.model_validate(
            {
                **friend.__dict__,
                "total_owed_to_you": balance.total_owed_to_you if balance else Decimal("0.00"),
                "total_you_owe": balance.total_you_owe if balance else Decimal("0.00"),
                "history": history,
            }
        )

    def settle(self, friend_id: uuid.UUID, user_id: uuid.UUID, payload: FriendSettlementRequest) -> FriendDetailRead:
        friend = self.friends.get(friend_id, user_id)
        if not friend:
            raise ExpenseFlowException("Friend not found", status.HTTP_404_NOT_FOUND)

        touched = False
        for transaction in self.transactions.list(user_id):
            if payload.transaction_id and transaction.id != payload.transaction_id:
                continue

            updated = False
            for participant in transaction.participants:
                if participant.friend_id == friend.id or participant.participant_name == friend.name:
                    if participant.pending_amount > 0:
                        participant.pending_amount = Decimal("0.00")
                        participant.status = "settled"
                        participant.paid_at = datetime.now(UTC)
                        touched = True
                        updated = True

            if updated:
                self.transactions.save(transaction)

        if not touched:
            raise ExpenseFlowException("No pending settlements found for this friend", status.HTTP_400_BAD_REQUEST)

        return self.get_detail(friend_id, user_id)

    def _build_history(
        self,
        friend: Friend,
        user_id: uuid.UUID,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[FriendTransactionHistoryItem]:
        history: list[FriendTransactionHistoryItem] = []
        for transaction in self.transactions.list(user_id):
            if from_date and transaction.transaction_date < from_date:
                continue
            if to_date and transaction.transaction_date > to_date:
                continue
            for participant in transaction.participants:
                if participant.friend_id == friend.id or participant.participant_name == friend.name:
                    history.append(
                        FriendTransactionHistoryItem(
                            transaction_id=transaction.id,
                            transaction_date=transaction.transaction_date,
                            description=transaction.description,
                            transaction_type=transaction.transaction_type.value,
                            share_amount=participant.share_amount,
                            pending_amount=participant.pending_amount,
                            status=participant.status,
                        )
                    )
        return history
