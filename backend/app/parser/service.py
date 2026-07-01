from __future__ import annotations

from decimal import Decimal

from app.parser.category_map import CATEGORY_KEYWORDS
from app.parser.regex_patterns import AMOUNT_PATTERN, PAID_BY_PATTERN, RECEIVED_PATTERN, WITH_PATTERN
from app.parser.schemas import ParsedParticipant, ParsedTransaction


class TransactionMessageParser:
    """Regex-first parser designed to be swappable with AI later."""

    def parse(self, text: str) -> ParsedTransaction | None:
        normalized = " ".join(text.strip().split())
        if not normalized:
            return None

        amount_match = AMOUNT_PATTERN.search(normalized)
        if not amount_match:
            return None

        amount = Decimal(amount_match.group("amount").replace("+", "").replace("-", ""))
        payer_match = PAID_BY_PATTERN.search(normalized)
        with_match = WITH_PATTERN.search(normalized)

        if RECEIVED_PATTERN.search(normalized):
            description = normalized.replace(amount_match.group("amount"), "", 1).strip(" -") or "Income"
            category = self._infer_category(description, income=True)
            return ParsedTransaction(
                transaction_type="income",
                amount=amount,
                my_share=amount,
                description=description,
                category_name=category,
                confidence=0.96,
            )

        if payer_match:
            payer = payer_match.group("payer").strip()
            description = normalized[: payer_match.start()].strip()
            description = description.replace(amount_match.group("amount"), "", 1).strip(" -") or description
            category = self._infer_category(description)
            return ParsedTransaction(
                transaction_type="borrowed",
                amount=amount,
                my_share=(amount / 2).quantize(Decimal("0.01")),
                description=description,
                category_name=category,
                payment_owner=payer,
                participants=[ParsedParticipant(name=payer, share_amount=(amount / 2).quantize(Decimal("0.01")))],
                confidence=0.9,
            )

        if with_match:
            names = [name.strip() for name in with_match.group("participants").split() if name.strip()]
            description = normalized[: with_match.start()].strip()
            description = description.replace(amount_match.group("amount"), "", 1).strip(" -") or description
            total_people = len(names) + 1
            share = (amount / total_people).quantize(Decimal("0.01"))
            category = self._infer_category(description)
            return ParsedTransaction(
                transaction_type="shared",
                amount=amount,
                my_share=share,
                description=description,
                category_name=category,
                participants=[ParsedParticipant(name=name, share_amount=share) for name in names],
                confidence=0.92,
            )

        description = normalized.replace(amount_match.group("amount"), "", 1).strip(" -") or "Expense"
        category = self._infer_category(description)
        return ParsedTransaction(
            transaction_type="personal",
            amount=amount,
            my_share=amount,
            description=description,
            category_name=category,
            confidence=0.85,
        )

    def _infer_category(self, description: str, *, income: bool = False) -> str:
        lowered = description.lower()
        for category, keywords in CATEGORY_KEYWORDS.items():
            if income and category not in {"Salary", "Freelance", "Investment", "Gift", "Refund"}:
                continue
            if any(keyword in lowered for keyword in keywords):
                return category
        return "Others"
