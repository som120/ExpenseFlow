from __future__ import annotations

import base64
from datetime import UTC, datetime
from io import BytesIO, StringIO

from fpdf import FPDF
from openpyxl import Workbook

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
        return ExportRead(filename="expenseflow-report.csv", content=buffer.getvalue(), media_type="text/csv", encoding="utf-8")

    def export_excel(self, user_id) -> ExportRead:
        report = self.get_report(user_id, report_type="excel")
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "ExpenseFlow Report"
        sheet.append(["Title", "Value"])
        for section in report.sections:
            sheet.append([section.title, section.value])

        buffer = BytesIO()
        workbook.save(buffer)
        return ExportRead(
            filename="expenseflow-report.xlsx",
            content=base64.b64encode(buffer.getvalue()).decode("ascii"),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            encoding="base64",
        )

    def export_pdf(self, user_id) -> ExportRead:
        report = self.get_report(user_id, report_type="pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=16)
        pdf.cell(0, 10, "ExpenseFlow Report", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=11)
        pdf.cell(0, 8, f"Generated at: {report.generated_at}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        for section in report.sections:
            pdf.cell(0, 8, f"{section.title}: {section.value}", new_x="LMARGIN", new_y="NEXT")

        content = bytes(pdf.output())
        return ExportRead(
            filename="expenseflow-report.pdf",
            content=base64.b64encode(content).decode("ascii"),
            media_type="application/pdf",
            encoding="base64",
        )
