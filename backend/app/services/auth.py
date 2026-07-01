from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import ExpenseFlowException
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories.category import CategoryRepository
from app.repositories.user import UserRepository
from app.schemas.auth import Token, UserLogin, UserRegister


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.categories = CategoryRepository(db)

    def register(self, payload: UserRegister) -> User:
        if self.users.get_by_email(payload.email):
            raise ExpenseFlowException("Email is already registered", status.HTTP_409_CONFLICT)

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
        )
        created_user = self.users.create(user)
        self.categories.seed_defaults()
        return created_user

    def login(self, payload: UserLogin) -> Token:
        user = self.users.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise ExpenseFlowException("Invalid email or password", status.HTTP_401_UNAUTHORIZED)

        return Token(access_token=create_access_token(str(user.id)))
