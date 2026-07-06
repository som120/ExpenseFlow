from __future__ import annotations

import hashlib
import hmac
from datetime import UTC, datetime

from fastapi import status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ExpenseFlowException
from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from app.repositories.category import CategoryRepository
from app.repositories.user import UserRepository
from app.schemas.auth import AuthResponse, TelegramAuthPayload, UserRead


class TelegramAuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)
        self.categories = CategoryRepository(db)

    def authenticate(self, payload: TelegramAuthPayload) -> AuthResponse:
        self._verify_payload(payload)

        user = self.users.get_by_telegram_id(payload.id)
        if not user:
            user = self._create_user_from_telegram(payload)
        else:
            user = self._sync_user_profile(user, payload)

        return AuthResponse(
            access_token=create_access_token(str(user.id)),
            user=UserRead.model_validate(user),
        )

    def link_current_user(self, current_user: User, payload: TelegramAuthPayload) -> UserRead:
        self._verify_payload(payload)

        existing = self.users.get_by_telegram_id(payload.id)
        if existing and existing.id != current_user.id:
            raise ExpenseFlowException(
                "This Telegram account is already linked to another user",
                status.HTTP_409_CONFLICT,
            )

        current_user.telegram_id = str(payload.id)
        if payload.first_name:
            current_user.full_name = self._build_full_name(payload)

        saved = self.users.save(current_user)
        return UserRead.model_validate(saved)

    def _verify_payload(self, payload: TelegramAuthPayload) -> None:
        if not settings.telegram_bot_token:
            raise ExpenseFlowException("Telegram login is not configured", status.HTTP_503_SERVICE_UNAVAILABLE)

        data = payload.model_dump(exclude={"hash"}, exclude_none=True)
        check_string = "\n".join(f"{key}={data[key]}" for key in sorted(data))
        secret = hashlib.sha256(settings.telegram_bot_token.encode()).digest()
        computed_hash = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
        if computed_hash != payload.hash:
            raise ExpenseFlowException("Invalid Telegram login payload", status.HTTP_401_UNAUTHORIZED)

        auth_time = datetime.fromtimestamp(payload.auth_date, tz=UTC)
        age = datetime.now(UTC) - auth_time
        if age.total_seconds() > 86400:
            raise ExpenseFlowException("Telegram login payload has expired", status.HTTP_401_UNAUTHORIZED)

    def _create_user_from_telegram(self, payload: TelegramAuthPayload) -> User:
        email = self._build_email(payload)
        existing_email_user = self.users.get_by_email(email)
        if existing_email_user:
            existing_email_user.telegram_id = str(payload.id)
            return self.users.save(existing_email_user)

        user = User(
            email=email,
            full_name=self._build_full_name(payload),
            hashed_password=get_password_hash(f"telegram-{payload.id}"),
            telegram_id=str(payload.id),
        )
        created = self.users.create(user)
        self.categories.seed_defaults()
        return created

    def _sync_user_profile(self, user: User, payload: TelegramAuthPayload) -> User:
        full_name = self._build_full_name(payload)
        if full_name and user.full_name != full_name:
            user.full_name = full_name
            return self.users.save(user)
        return user

    def _build_full_name(self, payload: TelegramAuthPayload) -> str:
        return " ".join(part for part in [payload.first_name, payload.last_name] if part).strip()

    def _build_email(self, payload: TelegramAuthPayload) -> str:
        username_part = (payload.username or f"user{payload.id}").strip().replace(" ", "_").lower()
        return f"telegram_{username_part}_{payload.id}@bot.expenseflow.local"
