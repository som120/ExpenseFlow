from __future__ import annotations

from datetime import UTC, datetime
from io import StringIO

from sqlalchemy.orm import Session

from app.schemas.report import ExportRead, ReportRead, ReportSection
from app.services.analytics import AnalyticsService
from app.services.summary import SummaryService


class ReportService:
    def __init__(self, db: Session):
        self.summary = SummaryService(db)
        self.analytics = AnalyticsService(db)

    def get_report(self, user_id, report_type: str = "monthly") -> ReportRead:
        summary = self.summary.get_summary(user_id)
        analytics = self.analytics.get_analytics(user_id)
        sections = [
            ReportSection(title="Total Income", value=str(summary.total_income)),
            ReportSection(title="Total Expenses", value=str(summary.total_expenses)),
            ReportSection(title="Net Savings", value=str(summary.net_savings)),
            ReportSection(title="Top Spending Category", value=analytics.top_spending_category or "N/A"),
            ReportSection(title="Highest Expense", value=str(analytics.highest_expense)),
        ]
        return ReportRead(
            report_type=report_type,
            sections=sections,
            generated_at=datetime.now(UTC).isoformat(),
        )

    def export_csv(self, user_id) -> ExportRead:
        report = self.get_report(user_id, report_type="csv")
        buffer = StringIO()
        buffer.write("title,value\n")
        for section in report.sections:
            buffer.write(f"{section.title},{section.value}\n")
        return ExportRead(filename="expenseflow-report.csv", content=buffer.getvalue(), media_type="text/csv")

    def export_excel(self, user_id) -> ExportRead:
        csv_export = self.export_csv(user_id)
        return ExportRead(
            filename="expenseflow-report.xls",
            content=csv_export.content,
            media_type="application/vnd.ms-excel",
        )

    def export_pdf(self, user_id) -> ExportRead:
        report = self.get_report(user_id, report_type="pdf")
        content = "ExpenseFlow Report\n" + "\n".join(f"{section.title}: {section.value}" for section in report.sections)
        return ExportRead(filename="expenseflow-report.pdf", content=content, media_type="application/pdf")
