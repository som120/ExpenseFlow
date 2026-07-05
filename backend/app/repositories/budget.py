import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.budget import Budget


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, budget: Budget) -> Budget:
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        return budget

    def list(self, user_id: uuid.UUID) -> list[Budget]:
        stmt = (
            select(Budget)
            .options(selectinload(Budget.category))
            .where(Budget.user_id == user_id)
            .order_by(Budget.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def get(self, budget_id: uuid.UUID, user_id: uuid.UUID) -> Budget | None:
        stmt = (
            select(Budget)
            .options(selectinload(Budget.category))
            .where(Budget.id == budget_id, Budget.user_id == user_id)
        )
        return self.db.scalar(stmt)

    def save(self, budget: Budget) -> Budget:
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        return budget

    def delete(self, budget: Budget) -> None:
        self.db.delete(budget)
        self.db.commit()
