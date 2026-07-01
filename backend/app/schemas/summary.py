from decimal import Decimal

from pydantic import BaseModel


class SummaryRead(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    money_you_owe: Decimal
    money_owed_to_you: Decimal
    net_savings: Decimal
    current_balance: Decimal
