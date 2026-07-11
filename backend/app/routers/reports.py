from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.report import ExportRead, ReportRead
from app.services.report import ReportService


router = APIRouter()


@router.get("", response_model=ReportRead)
def get_report(db: DbSession, current_user: CurrentUser, report_type: str = "monthly"):
    return ReportService(db).get_report(current_user.id, report_type)


@router.get("/export/csv", response_model=ExportRead)
def export_csv(db: DbSession, current_user: CurrentUser):
    return ReportService(db).export_csv(current_user.id)


@router.get("/export/excel", response_model=ExportRead)
def export_excel(db: DbSession, current_user: CurrentUser):
    return ReportService(db).export_excel(current_user.id)


@router.get("/export/pdf", response_model=ExportRead)
def export_pdf(db: DbSession, current_user: CurrentUser):
    return ReportService(db).export_pdf(current_user.id)
