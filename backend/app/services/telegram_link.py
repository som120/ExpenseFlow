from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ExpenseFlowException
from app.models.user import User
from app.repositories.user import UserRepository


class TelegramLinkService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def generate_link_code(self, user: User) -> dict[str, str]:
        code = f"{secrets.randbelow(900000) + 100000}"
        user.telegram_link_code = code
        user.telegram_link_code_expires_at = datetime.now(UTC) + timedelta(minutes=15)
        self.users.save(user)
        return {
            "code": code,
            "expires_at": user.telegram_link_code_expires_at.isoformat(),
            "instructions": f"Send /link {code} to the Telegram bot within 15 minutes.",
        }

    def consume_link_code(self, code: str, telegram_user: User) -> User:
        target_user = self.users.get_by_telegram_link_code(code)
        if not target_user:
            raise ExpenseFlowException("Invalid or expired link code", status.HTTP_404_NOT_FOUND)

        existing = self.users.get_by_telegram_id(telegram_user.telegram_id)
        if existing and existing.id != target_user.id and existing.email.endswith("@bot.expenseflow.local"):
            existing.telegram_id = None
            self.users.save(existing)

        target_user.telegram_id = telegram_user.telegram_id
        target_user.telegram_link_code = None
        target_user.telegram_link_code_expires_at = None
        return self.users.save(target_user)
