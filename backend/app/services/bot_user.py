from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import ExpenseFlowException
from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.category import CategoryRepository
from app.repositories.user import UserRepository
from app.services.telegram_link import TelegramLinkService


class BotUserService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.categories = CategoryRepository(db)
        self.link_service = TelegramLinkService(db)

    def get_or_create_telegram_user(
        self,
        telegram_id: int,
        full_name: str,
        telegram_username: str | None = None,
    ) -> User:
        user = self.users.get_by_telegram_id(telegram_id)
        if user:
            updated = False
            if full_name and user.full_name != full_name:
                user.full_name = full_name
                updated = True
            if updated:
                return self.users.save(user)
            return user

        email = self._build_telegram_email(telegram_id, telegram_username)
        user = User(
            email=email,
            full_name=full_name or f"Telegram User {telegram_id}",
            hashed_password=get_password_hash(uuid.uuid4().hex),
            telegram_id=str(telegram_id),
        )
        created = self.users.create(user)
        self.categories.seed_defaults()
        return created

    def consume_manual_link_code(
        self,
        code: str,
        telegram_id: int,
        full_name: str,
        telegram_username: str | None = None,
    ) -> User:
        code = code.strip()
        if not code.isdigit():
            raise ExpenseFlowException("Invalid link code format")

        telegram_user = self.get_or_create_telegram_user(telegram_id, full_name, telegram_username)
        return self.link_service.consume_link_code(code, telegram_user)

    def _build_telegram_email(self, telegram_id: int, telegram_username: str | None) -> str:
        username_part = (telegram_username or f"user{telegram_id}").strip().replace(" ", "_").lower()
        return f"telegram_{username_part}_{telegram_id}@bot.expenseflow.local"
