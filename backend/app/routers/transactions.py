import uuid

from fastapi import APIRouter, Response, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from app.services.transaction import TransactionService


router = APIRouter()


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: DbSession, current_user: CurrentUser):
    return TransactionService(db).create(payload, current_user.id)


@router.get("", response_model=list[TransactionRead])
def list_transactions(db: DbSession, current_user: CurrentUser):
    return TransactionService(db).list(current_user.id)


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: uuid.UUID, db: DbSession, current_user: CurrentUser):
    return TransactionService(db).get(transaction_id, current_user.id)


@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(
    transaction_id: uuid.UUID,
    payload: TransactionUpdate,
    db: DbSession,
    current_user: CurrentUser,
):
    return TransactionService(db).update(transaction_id, payload, current_user.id)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: uuid.UUID, db: DbSession, current_user: CurrentUser):
    TransactionService(db).delete(transaction_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
