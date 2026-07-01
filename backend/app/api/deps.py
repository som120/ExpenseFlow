from typing import Annotated

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import ExpenseFlowException
from app.models.user import User
from app.repositories.user import UserRepository


bearer_scheme = HTTPBearer(auto_error=False)


DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if not credentials:
        raise ExpenseFlowException("Authentication required", status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        subject = payload.get("sub")
    except JWTError as exc:
        raise ExpenseFlowException("Invalid authentication token", status.HTTP_401_UNAUTHORIZED) from exc

    if not subject:
        raise ExpenseFlowException("Invalid authentication token", status.HTTP_401_UNAUTHORIZED)

    user = UserRepository(db).get(subject)
    if not user:
        raise ExpenseFlowException("User not found", status.HTTP_401_UNAUTHORIZED)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
