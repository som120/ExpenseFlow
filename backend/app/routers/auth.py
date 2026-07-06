from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.auth import AuthResponse, TelegramLinkPayload, Token, UserLogin, UserRead, UserRegister
from app.services.auth import AuthService
from app.services.telegram_auth import TelegramAuthService


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: DbSession):
    return AuthService(db).register(payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: DbSession):
    return AuthService(db).login(payload)


@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUser):
    return current_user


@router.post("/telegram", response_model=AuthResponse)
def telegram_auth(payload: TelegramLinkPayload, db: DbSession):
    return TelegramAuthService(db).authenticate(payload)


@router.post("/telegram/link", response_model=UserRead)
def telegram_link(payload: TelegramLinkPayload, db: DbSession, current_user: CurrentUser):
    return TelegramAuthService(db).link_current_user(current_user, payload)
