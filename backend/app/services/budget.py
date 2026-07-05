import uuid
from decimal import Decimal

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ExpenseFlowException
from app.models.budget import Budget
from app.models.category import Category
from app.repositories.budget import BudgetRepository
from app.repositories.category import CategoryRepository
from app.repositories.transaction import TransactionRepository
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate


class BudgetService:
    def __init__(self, db: Session):
        self.db = db
        self.budgets = BudgetRepository(db)
        self.categories = CategoryRepository(db)
        self.transactions = TransactionRepository(db)

    def create(self, payload: BudgetCreate, user_id: uuid.UUID) -> BudgetRead:
        category = self._resolve_category(payload.category_name, user_id)
        budget = Budget(
            user_id=user_id,
            name=payload.name,
            amount=payload.amount,
            period=payload.period,
            category=category,
            is_active=payload.is_active,
        )
        created = self.budgets.create(budget)
        return self._to_read_model(created, user_id)

    def list(self, user_id: uuid.UUID) -> list[BudgetRead]:
        return [self._to_read_model(item, user_id) for item in self.budgets.list(user_id)]

    def update(self, budget_id: uuid.UUID, payload: BudgetUpdate, user_id: uuid.UUID) -> BudgetRead:
        budget = self.budgets.get(budget_id, user_id)
        if not budget:
            raise ExpenseFlowException("Budget not found", status.HTTP_404_NOT_FOUND)

        updates = payload.model_dump(exclude_unset=True)
        category_name = updates.pop("category_name", None)
        for field, value in updates.items():
            setattr(budget, field, value)

        if category_name is not None:
            budget.category = self._resolve_category(category_name, user_id)

        updated = self.budgets.save(budget)
        return self._to_read_model(updated, user_id)

    def delete(self, budget_id: uuid.UUID, user_id: uuid.UUID) -> None:
        budget = self.budgets.get(budget_id, user_id)
        if not budget:
            raise ExpenseFlowException("Budget not found", status.HTTP_404_NOT_FOUND)
        self.budgets.delete(budget)

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

    def _to_read_model(self, budget: Budget, user_id: uuid.UUID) -> BudgetRead:
        spent_amount = Decimal("0.00")
        for transaction in self.transactions.list(user_id):
            if budget.category_id and transaction.category_id != budget.category_id:
                continue
            spent_amount += transaction.my_share

        remaining_amount = budget.amount - spent_amount
        return BudgetRead.model_validate(
            {
                **budget.__dict__,
                "category_name": budget.category.name if budget.category else None,
                "spent_amount": spent_amount,
                "remaining_amount": remaining_amount,
            }
        )
