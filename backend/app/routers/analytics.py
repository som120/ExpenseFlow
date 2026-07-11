from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.analytics import AnalyticsRead
from app.services.analytics import AnalyticsService


router = APIRouter()


@router.get("", response_model=AnalyticsRead)
def get_analytics(db: DbSession, current_user: CurrentUser):
    return AnalyticsService(db).get_analytics(current_user.id)
