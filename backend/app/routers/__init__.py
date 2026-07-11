from fastapi import APIRouter

from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router
from app.routers.budgets import router as budgets_router
from app.routers.friends import router as friends_router
from app.routers.health import router as health_router
from app.routers.reports import router as reports_router
from app.routers.summary import router as summary_router
from app.routers.telegram import router as telegram_router
from app.routers.transactions import router as transactions_router


api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
api_router.include_router(friends_router, prefix="/friends", tags=["friends"])
api_router.include_router(budgets_router, prefix="/budgets", tags=["budgets"])
api_router.include_router(summary_router, prefix="/summary", tags=["summary"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(telegram_router, prefix="/telegram", tags=["telegram"])
