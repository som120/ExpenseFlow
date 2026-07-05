from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.transaction import TransactionType
from app.models.user import User
from app.parser.schemas import ParsedTransaction
from app.parser.service import TransactionMessageParser
from app.schemas.bot import BotResponse
from app.schemas.transaction import TransactionCreate, TransactionParticipantCreate
from app.services.transaction import TransactionService


class BotTransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.parser = TransactionMessageParser()
        self.transaction_service = TransactionService(db)

    def parse_message(self, text: str) -> ParsedTransaction | None:
        return self.parser.parse(text)

    def preview_message(self, text: str) -> BotResponse:
        parsed = self.parse_message(text)
        if not parsed:
            return BotResponse(message="Sorry, I could not understand that message.")

        return BotResponse(
            message=self._build_preview(parsed),
            parsed=parsed.model_dump(mode="json"),
        )

    def create_transaction_from_message(self, text: str, user: User) -> BotResponse:
        parsed = self.parse_message(text)
        if not parsed:
            return BotResponse(message="Sorry, I could not understand that message.")

        self.create_transaction_from_parsed(parsed, user.id)
        return BotResponse(
            message=f"Saved transaction. {self._build_preview(parsed)}",
            parsed=parsed.model_dump(mode="json"),
        )

    def create_transaction_from_parsed(self, parsed: ParsedTransaction, user_id) -> None:
        payload = TransactionCreate(
            transaction_type=TransactionType(parsed.transaction_type),
            category_name=parsed.category_name,
            amount=parsed.amount,
            my_share=parsed.my_share,
            description=parsed.description,
            payment_owner=parsed.payment_owner,
            transaction_date=date.today(),
            participants=[
                TransactionParticipantCreate(
                    participant_name=item.name,
                    share_amount=item.share_amount or Decimal("0.00"),
                    pending_amount=item.share_amount or Decimal("0.00"),
                    status="pending",
                )
                for item in parsed.participants
            ],
        )
        self.transaction_service.create(payload, user_id)

    def _build_preview(self, parsed: ParsedTransaction) -> str:
        base = (
            f"Detected {parsed.transaction_type} | amount: {parsed.amount} | "
            f"my share: {parsed.my_share} | category: {parsed.category_name}"
        )
        if parsed.participants:
            people = ", ".join(item.name for item in parsed.participants)
            base += f" | participants: {people}"
        if parsed.payment_owner != "self":
            base += f" | paid by: {parsed.payment_owner}"
        return base
