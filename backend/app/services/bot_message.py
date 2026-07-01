from app.schemas.bot import BotResponse
from app.services.summary import SummaryService


class BotMessageService:
    def __init__(self, summary_service: SummaryService):
        self.summary_service = summary_service

    def build_balance_response(self) -> BotResponse:
        return BotResponse(
            message="Balance snapshot is available after transaction sync for your authenticated account.",
            command="balance",
        )

    def build_summary_response(self) -> BotResponse:
        return BotResponse(
            message="Use the app dashboard or authenticated summary API for full totals. Bot-linked user summaries will be expanded next.",
            command="summary",
        )
