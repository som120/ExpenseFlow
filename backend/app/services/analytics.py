from __future__ import annotations

from collections import defaultdict
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.transaction import TransactionType
from app.repositories.transaction import TransactionRepository
from app.schemas.analytics import AnalyticsRead, CategoryBreakdownItem, FriendBalanceItem, TrendPoint


class AnalyticsService:
    def __init__(self, db: Session):
        self.transactions = TransactionRepository(db)

    def get_analytics(self, user_id) -> AnalyticsRead:
        transactions = self.transactions.list(user_id)

        monthly = defaultdict(lambda: {"income": Decimal("0.00"), "expenses": Decimal("0.00")})
        categories = defaultdict(lambda: Decimal("0.00"))
        friend_balances = defaultdict(lambda: Decimal("0.00"))
        highest_expense = Decimal("0.00")
        highest_income = Decimal("0.00")

        for transaction in transactions:
            month_key = transaction.transaction_date.strftime("%Y-%m")

            if transaction.transaction_type == TransactionType.INCOME:
                monthly[month_key]["income"] += transaction.amount
                highest_income = max(highest_income, transaction.amount)
                continue

            monthly[month_key]["expenses"] += transaction.my_share
            categories[transaction.category.name if transaction.category else "Others"] += transaction.my_share
            highest_expense = max(highest_expense, transaction.my_share)

            direction = None
            if transaction.transaction_type == TransactionType.SHARED:
                direction = "owed_to_you"
            elif transaction.transaction_type == TransactionType.BORROWED:
                direction = "you_owe"

            if direction:
                for participant in transaction.participants:
                    key = f"{direction}:{participant.participant_name}"
                    friend_balances[key] += participant.pending_amount

        trend_points = []
        monthly_expenses = []
        for label in sorted(monthly):
            income = monthly[label]["income"]
            expenses = monthly[label]["expenses"]
            monthly_expenses.append(expenses)
            trend_points.append(
                TrendPoint(label=label, income=income, expenses=expenses, savings=income - expenses)
            )

        category_breakdown = [
            CategoryBreakdownItem(category=category, amount=amount)
            for category, amount in sorted(categories.items(), key=lambda item: item[1], reverse=True)
        ]
        friend_balance_items = []
        for key, amount in sorted(friend_balances.items(), key=lambda item: item[1], reverse=True):
            direction, friend = key.split(":", 1)
            friend_balance_items.append(FriendBalanceItem(friend=friend, amount=amount, direction=direction))

        top_spending_category = category_breakdown[0].category if category_breakdown else None
        average_monthly_spend = (
            sum(monthly_expenses, Decimal("0.00")) / len(monthly_expenses)
            if monthly_expenses
            else Decimal("0.00")
        )

        return AnalyticsRead(
            monthly_trends=trend_points,
            category_breakdown=category_breakdown,
            friend_balances=friend_balance_items,
            top_spending_category=top_spending_category,
            average_monthly_spend=average_monthly_spend.quantize(Decimal("0.01")),
            highest_expense=highest_expense,
            highest_income=highest_income,
        )
