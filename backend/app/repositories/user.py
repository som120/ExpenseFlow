import uuid

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get(self, user_id: uuid.UUID | str) -> User | None:
        return self.db.get(User, user_id)

    def get_by_telegram_id(self, telegram_id: int | str) -> User | None:
        return self.db.scalar(select(User).where(User.telegram_id == str(telegram_id)))

    def get_by_telegram_link_code(self, code: str) -> User | None:
        stmt = select(User).where(User.telegram_link_code == code).where(User.telegram_link_code_expires_at > datetime.now(UTC))
        return self.db.scalar(stmt)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
