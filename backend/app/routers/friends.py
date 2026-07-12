import uuid
from datetime import date

from fastapi import APIRouter, Response, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.friend import FriendCreate, FriendDetailRead, FriendRead, FriendSettlementRequest, FriendUpdate
from app.services.friend import FriendService


router = APIRouter()


@router.post("", response_model=FriendRead, status_code=status.HTTP_201_CREATED)
def create_friend(payload: FriendCreate, db: DbSession, current_user: CurrentUser):
    return FriendService(db).create(payload, current_user.id)


@router.get("", response_model=list[FriendRead])
def list_friends(db: DbSession, current_user: CurrentUser, from_date: date | None = None, to_date: date | None = None):
    return FriendService(db).list(current_user.id, from_date=from_date, to_date=to_date)


@router.put("/{friend_id}", response_model=FriendRead)
def update_friend(friend_id: uuid.UUID, payload: FriendUpdate, db: DbSession, current_user: CurrentUser):
    return FriendService(db).update(friend_id, payload, current_user.id)


@router.get("/{friend_id}/history", response_model=FriendDetailRead)
def get_friend_history(
    friend_id: uuid.UUID,
    db: DbSession,
    current_user: CurrentUser,
    from_date: date | None = None,
    to_date: date | None = None,
):
    return FriendService(db).get_detail(friend_id, current_user.id, from_date=from_date, to_date=to_date)


@router.post("/{friend_id}/settlements", response_model=FriendDetailRead)
def settle_friend(friend_id: uuid.UUID, payload: FriendSettlementRequest, db: DbSession, current_user: CurrentUser):
    return FriendService(db).settle(friend_id, current_user.id, payload)


@router.delete("/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_friend(friend_id: uuid.UUID, db: DbSession, current_user: CurrentUser):
    FriendService(db).delete(friend_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
