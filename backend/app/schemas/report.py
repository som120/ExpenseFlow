from decimal import Decimal

from pydantic import BaseModel


class ReportSection(BaseModel):
    title: str
    value: str


class ReportRead(BaseModel):
    report_type: str
    sections: list[ReportSection]
    generated_at: str


class ExportRead(BaseModel):
    filename: str
    content: str
    media_type: str
    encoding: str = "utf-8"
