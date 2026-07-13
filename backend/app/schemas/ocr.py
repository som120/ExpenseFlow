from pydantic import BaseModel


class OCRRead(BaseModel):
    extracted_text: str
    message: str
    parsed: dict | None = None
