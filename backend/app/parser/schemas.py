from decimal import Decimal

from pydantic import BaseModel, Field


class ParsedParticipant(BaseModel):
    name: str
    share_amount: Decimal | None = None


class ParsedTransaction(BaseModel):
    transaction_type: str
    amount: Decimal
    my_share: Decimal
    description: str
    category_name: str
    payment_owner: str = "self"
    participants: list[ParsedParticipant] = Field(default_factory=list)
    confidence: float = 0.0
    parser_version: str = "regex-v1"
