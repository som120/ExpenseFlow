from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.category import CategoryRead
from app.services.category import CategoryService


router = APIRouter()


@router.get("", response_model=list[CategoryRead])
def list_categories(db: DbSession, current_user: CurrentUser):
    return CategoryService(db).list(current_user.id)
