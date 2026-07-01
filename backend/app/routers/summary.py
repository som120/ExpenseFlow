from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.summary import SummaryRead
from app.services.summary import SummaryService


router = APIRouter()


@router.get("", response_model=SummaryRead)
def get_summary(db: DbSession, current_user: CurrentUser):
    return SummaryService(db).get_summary(current_user.id)
