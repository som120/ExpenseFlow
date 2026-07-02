from aiogram.types import Update
from fastapi import APIRouter, Header, status

from app.api.deps import DbSession
from app.bot.handlers import handle_command
from app.bot.manager import telegram_bot_manager
from app.core.config import settings
from app.core.exceptions import ExpenseFlowException
from app.schemas.bot import BotResponse
from app.services.bot_message import BotMessageService
from app.services.bot_transaction import BotTransactionService
from app.services.summary import SummaryService


router = APIRouter()


@router.post("/webhook", response_model=BotResponse)
async def telegram_webhook(
    payload: Update,
    db: DbSession,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> BotResponse:
    expected_secret = settings.telegram_webhook_secret
    if expected_secret and x_telegram_bot_api_secret_token != expected_secret:
        raise ExpenseFlowException("Invalid webhook secret", status.HTTP_401_UNAUTHORIZED)

    message = payload.message or payload.edited_message
    if not message or not message.text:
        return BotResponse(message="Ignored unsupported Telegram update type.")

    message_service = BotMessageService(SummaryService(db))
    if message.text.startswith("/"):
        response = handle_command(message.text, message_service)
    else:
        response = BotTransactionService(db).preview_message(message.text)

    await telegram_bot_manager.send_text(message.chat.id, response.message)
    return response
