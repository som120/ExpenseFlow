import uuid

from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get(self, transaction_id: uuid.UUID, user_id: uuid.UUID) -> Transaction | None:
        stmt = self._base_query().where(Transaction.id == transaction_id, Transaction.user_id == user_id)
        return self.db.scalar(stmt)

    def list(self, user_id: uuid.UUID) -> list[Transaction]:
        stmt = (
            self._base_query()
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def delete(self, transaction: Transaction) -> None:
        self.db.delete(transaction)
        self.db.commit()

    def save(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def _base_query(self) -> Select[tuple[Transaction]]:
        return select(Transaction).options(
            selectinload(Transaction.category),
            selectinload(Transaction.participants),
        )
