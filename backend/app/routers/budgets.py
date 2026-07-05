import uuid

from fastapi import APIRouter, Response, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate
from app.services.budget import BudgetService


router = APIRouter()


@router.post("", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget(payload: BudgetCreate, db: DbSession, current_user: CurrentUser):
    return BudgetService(db).create(payload, current_user.id)


@router.get("", response_model=list[BudgetRead])
def list_budgets(db: DbSession, current_user: CurrentUser):
    return BudgetService(db).list(current_user.id)


@router.put("/{budget_id}", response_model=BudgetRead)
def update_budget(budget_id: uuid.UUID, payload: BudgetUpdate, db: DbSession, current_user: CurrentUser):
    return BudgetService(db).update(budget_id, payload, current_user.id)


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: uuid.UUID, db: DbSession, current_user: CurrentUser):
    BudgetService(db).delete(budget_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
