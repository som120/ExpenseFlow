import uuid

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ExpenseFlowException
from app.models.friend import Friend
from app.repositories.friend import FriendRepository
from app.schemas.friend import FriendCreate, FriendRead, FriendUpdate


class FriendService:
    def __init__(self, db: Session):
        self.friends = FriendRepository(db)

    def create(self, payload: FriendCreate, user_id: uuid.UUID) -> Friend:
        friend = Friend(user_id=user_id, **payload.model_dump())
        return self.friends.create(friend)

    def list(self, user_id: uuid.UUID) -> list[FriendRead]:
        return [FriendRead.model_validate(item) for item in self.friends.list(user_id)]

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
