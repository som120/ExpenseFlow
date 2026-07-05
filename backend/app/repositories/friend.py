import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.friend import Friend


class FriendRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, friend: Friend) -> Friend:
        self.db.add(friend)
        self.db.commit()
        self.db.refresh(friend)
        return friend

    def list(self, user_id: uuid.UUID) -> list[Friend]:
        stmt = select(Friend).where(Friend.user_id == user_id).order_by(Friend.name.asc())
        return list(self.db.scalars(stmt).all())

    def get(self, friend_id: uuid.UUID, user_id: uuid.UUID) -> Friend | None:
        stmt = select(Friend).where(Friend.id == friend_id, Friend.user_id == user_id)
        return self.db.scalar(stmt)

    def save(self, friend: Friend) -> Friend:
        self.db.add(friend)
        self.db.commit()
        self.db.refresh(friend)
        return friend

    def delete(self, friend: Friend) -> None:
        self.db.delete(friend)
        self.db.commit()
