from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.transaction import TransactionType
from app.repositories.transaction import TransactionRepository
from app.schemas.summary import SummaryRead


class SummaryService:
    def __init__(self, db: Session):
        self.transactions = TransactionRepository(db)

    def get_summary(self, user_id) -> SummaryRead:
        transactions = self.transactions.list(user_id)

        total_income = Decimal("0.00")
        total_expenses = Decimal("0.00")
        money_you_owe = Decimal("0.00")
        money_owed_to_you = Decimal("0.00")

        for transaction in transactions:
            if transaction.transaction_type == TransactionType.INCOME:
                total_income += transaction.amount
                continue

            total_expenses += transaction.my_share

            participant_total = sum(
                (participant.pending_amount for participant in transaction.participants),
                Decimal("0.00"),
            )
            if transaction.transaction_type == TransactionType.BORROWED:
                money_you_owe += participant_total
            elif transaction.transaction_type == TransactionType.SHARED:
                money_owed_to_you += participant_total

        net_savings = total_income - total_expenses
        current_balance = net_savings - money_you_owe + money_owed_to_you

        return SummaryRead(
            total_income=total_income,
            total_expenses=total_expenses,
            money_you_owe=money_you_owe,
            money_owed_to_you=money_owed_to_you,
            net_savings=net_savings,
            current_balance=current_balance,
        )
