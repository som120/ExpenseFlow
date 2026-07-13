from __future__ import annotations

import io
import re
from decimal import Decimal

import pytesseract
from PIL import Image

from app.core.exceptions import ExpenseFlowException
from app.parser.schemas import ParsedTransaction
from app.parser.service import TransactionMessageParser


TOTAL_KEYWORDS = ("total", "grand total", "amount", "net amount", "bill total")
AMOUNT_REGEX = re.compile(r"(?P<amount>\d+(?:\.\d{1,2})?)")


class OCRService:
    def __init__(self) -> None:
        self.parser = TransactionMessageParser()

    def extract_text(self, file_bytes: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(file_bytes)).convert("L")
        except Exception as exc:
            raise ExpenseFlowException("Unsupported receipt image format") from exc

        try:
            return pytesseract.image_to_string(image).strip()
        except pytesseract.TesseractNotFoundError as exc:
            raise ExpenseFlowException("OCR engine is not installed on the server") from exc
        except Exception as exc:
            raise ExpenseFlowException("Failed to read receipt image") from exc

    def parse_receipt(self, extracted_text: str) -> ParsedTransaction | None:
        lines = [line.strip() for line in extracted_text.splitlines() if line.strip()]
        if not lines:
            return None

        description = next((line for line in lines if any(character.isalpha() for character in line)), "Receipt")
        amount = self._detect_amount(lines)
        if amount is None:
            return None

        synthetic_text = f"{amount} {description}"
        parsed = self.parser.parse(synthetic_text)
        if parsed:
            return parsed

        return ParsedTransaction(
            transaction_type="personal",
            amount=amount,
            my_share=amount,
            description=description,
            category_name=self.parser._infer_category(description),
            confidence=0.7,
        )

    def _detect_amount(self, lines: list[str]) -> Decimal | None:
        keyword_match: Decimal | None = None
        max_amount: Decimal | None = None
        for line in lines:
            matches = [Decimal(match.group("amount")) for match in AMOUNT_REGEX.finditer(line)]
            if not matches:
                continue
            line_max = max(matches)
            max_amount = line_max if max_amount is None else max(max_amount, line_max)
            lowered = line.lower()
            if any(keyword in lowered for keyword in TOTAL_KEYWORDS):
                keyword_match = line_max

        return keyword_match or max_amount
