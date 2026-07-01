from fastapi import APIRouter, Header, status

from app.api.deps import DbSession
from app.bot.handlers import handle_command
from app.core.config import settings
from app.core.exceptions import ExpenseFlowException
from app.schemas.bot import BotResponse, TelegramWebhookMessage
from app.services.bot_message import BotMessageService
from app.services.bot_transaction import BotTransactionService
from app.services.summary import SummaryService


router = APIRouter()


@router.post("/webhook", response_model=BotResponse)
def telegram_webhook(
    payload: TelegramWebhookMessage,
    db: DbSession,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> BotResponse:
    expected_secret = settings.telegram_webhook_secret
    if expected_secret and x_telegram_bot_api_secret_token != expected_secret:
        raise ExpenseFlowException("Invalid webhook secret", status.HTTP_401_UNAUTHORIZED)

    message_service = BotMessageService(SummaryService(db))
    if payload.text.startswith("/"):
        return handle_command(payload.text, message_service)

    return BotTransactionService(db).preview_message(payload.text)
