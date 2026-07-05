from app.schemas.bot import BotResponse
from app.services.summary import SummaryService


class BotMessageService:
    def __init__(self, summary_service: SummaryService, user_id):
        self.summary_service = summary_service
        self.user_id = user_id

    def build_balance_response(self) -> BotResponse:
        summary = self.summary_service.get_summary(self.user_id)
        return BotResponse(
            message=(
                f"Current balance: {summary.current_balance} | "
                f"Income: {summary.total_income} | Expenses: {summary.total_expenses} | "
                f"You owe: {summary.money_you_owe} | Owed to you: {summary.money_owed_to_you}"
            ),
            command="balance",
        )

    def build_summary_response(self) -> BotResponse:
        summary = self.summary_service.get_summary(self.user_id)
        return BotResponse(
            message=(
                f"Summary | Income: {summary.total_income} | Expenses: {summary.total_expenses} | "
                f"Net savings: {summary.net_savings} | Current balance: {summary.current_balance}"
            ),
            command="summary",
        )
