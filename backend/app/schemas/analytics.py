from decimal import Decimal

from pydantic import BaseModel


class TrendPoint(BaseModel):
    label: str
    income: Decimal = Decimal("0.00")
    expenses: Decimal = Decimal("0.00")
    savings: Decimal = Decimal("0.00")


class CategoryBreakdownItem(BaseModel):
    category: str
    amount: Decimal


class FriendBalanceItem(BaseModel):
    friend: str
    amount: Decimal
    direction: str


class AnalyticsRead(BaseModel):
    monthly_trends: list[TrendPoint]
    category_breakdown: list[CategoryBreakdownItem]
    friend_balances: list[FriendBalanceItem]
    top_spending_category: str | None = None
    average_monthly_spend: Decimal = Decimal("0.00")
    highest_expense: Decimal = Decimal("0.00")
    highest_income: Decimal = Decimal("0.00")
