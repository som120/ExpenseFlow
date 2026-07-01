import uuid
from decimal import Decimal

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ExpenseFlowException
from app.models.category import Category
from app.models.transaction import Transaction, TransactionParticipant, TransactionType
from app.repositories.category import CategoryRepository
from app.repositories.transaction import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate


class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.categories = CategoryRepository(db)
        self.transactions = TransactionRepository(db)

    def create(self, payload: TransactionCreate, user_id: uuid.UUID) -> TransactionRead:
        category = self._resolve_category(payload.category_name, user_id)
        transaction = Transaction(
            user_id=user_id,
            transaction_type=payload.transaction_type,
            category=category,
            amount=payload.amount,
            my_share=payload.my_share,
            description=payload.description,
            payment_owner=payload.payment_owner,
            transaction_date=payload.transaction_date,
            participants=[
                TransactionParticipant(
                    friend_id=participant.friend_id,
                    participant_name=participant.participant_name,
                    share_amount=participant.share_amount,
                    status=participant.status,
                    pending_amount=participant.pending_amount,
                )
                for participant in payload.participants
            ],
        )
        self._validate_transaction_rules(transaction)
        created = self.transactions.create(transaction)
        return self._to_read_model(created)

    def list(self, user_id: uuid.UUID) -> list[TransactionRead]:
        return [self._to_read_model(item) for item in self.transactions.list(user_id)]

    def get(self, transaction_id: uuid.UUID, user_id: uuid.UUID) -> TransactionRead:
        transaction = self.transactions.get(transaction_id, user_id)
        if not transaction:
            raise ExpenseFlowException("Transaction not found", status.HTTP_404_NOT_FOUND)
        return self._to_read_model(transaction)

    def update(self, transaction_id: uuid.UUID, payload: TransactionUpdate, user_id: uuid.UUID) -> TransactionRead:
        transaction = self.transactions.get(transaction_id, user_id)
        if not transaction:
            raise ExpenseFlowException("Transaction not found", status.HTTP_404_NOT_FOUND)

        updates = payload.model_dump(exclude_unset=True)
        category_name = updates.pop("category_name", None)
        participants = updates.pop("participants", None)

        for field, value in updates.items():
            setattr(transaction, field, value)

        if category_name is not None:
            transaction.category = self._resolve_category(category_name, user_id)

        if participants is not None:
            transaction.participants.clear()
            transaction.participants.extend(
                TransactionParticipant(
                    friend_id=item.friend_id,
                    participant_name=item.participant_name,
                    share_amount=item.share_amount,
                    status=item.status,
                    pending_amount=item.pending_amount,
                )
                for item in participants
            )

        self._validate_transaction_rules(transaction)
        updated = self.transactions.save(transaction)
        return self._to_read_model(updated)

    def delete(self, transaction_id: uuid.UUID, user_id: uuid.UUID) -> None:
        transaction = self.transactions.get(transaction_id, user_id)
        if not transaction:
            raise ExpenseFlowException("Transaction not found", status.HTTP_404_NOT_FOUND)
        self.transactions.delete(transaction)

    def _resolve_category(self, category_name: str | None, user_id: uuid.UUID) -> Category | None:
        if not category_name:
            return None

        category = self.categories.get_by_name(category_name, user_id)
        if category:
            return category

        category = Category(name=category_name, user_id=user_id, is_system=False)
        self.db.add(category)
        self.db.flush()
        return category

    def _validate_transaction_rules(self, transaction: Transaction) -> None:
        if transaction.my_share > transaction.amount:
            raise ExpenseFlowException("my_share cannot exceed amount")

        if transaction.transaction_type == TransactionType.INCOME and transaction.participants:
            raise ExpenseFlowException("Income transactions cannot have participants")

        if transaction.transaction_type == TransactionType.INCOME and transaction.my_share != transaction.amount:
            raise ExpenseFlowException("Income transactions must use full amount as my_share")

        if transaction.transaction_type in {TransactionType.SHARED, TransactionType.BORROWED} and not transaction.participants:
            raise ExpenseFlowException("Shared and borrowed transactions require participants")

        total_participant_share = sum(
            (participant.share_amount for participant in transaction.participants), Decimal("0.00")
        )
        if transaction.transaction_type in {TransactionType.SHARED, TransactionType.BORROWED} and total_participant_share <= 0:
            raise ExpenseFlowException("Participants must have a positive share amount")

    def _to_read_model(self, transaction: Transaction) -> TransactionRead:
        return TransactionRead.model_validate(
            {
                **transaction.__dict__,
                "category_name": transaction.category.name if transaction.category else None,
                "participants": transaction.participants,
            }
        )
