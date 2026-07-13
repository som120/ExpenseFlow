import logging

from aiogram.types import Update
from fastapi import APIRouter, Header, status

from app.api.deps import DbSession
from app.bot.handlers import handle_command, handle_link_command
from app.bot.manager import telegram_bot_manager
from app.core.config import settings
from app.core.exceptions import ExpenseFlowException
from app.schemas.bot import BotResponse
from app.services.budget import BudgetService
from app.services.bot_message import BotMessageService
from app.services.bot_transaction import BotTransactionService
from app.services.bot_user import BotUserService
from app.services.friend import FriendService
from app.services.ocr import OCRService
from app.services.report import ReportService
from app.services.summary import SummaryService


logger = logging.getLogger(__name__)


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
    if not message:
        return BotResponse(message="Ignored unsupported Telegram update type.")

    if not message.from_user:
        return BotResponse(message="Could not identify Telegram sender.")

    telegram_user = BotUserService(db).get_or_create_telegram_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        telegram_username=message.from_user.username,
    )

    bot_user_service = BotUserService(db)

    message_service = BotMessageService(
        SummaryService(db),
        telegram_user.id,
        report_service=ReportService(db),
        budget_service=BudgetService(db),
        friend_service=FriendService(db),
    )
    try:
        if message.photo:
            largest_photo = message.photo[-1]
            file_bytes = await telegram_bot_manager.get_file_bytes(largest_photo.file_id)
            if not file_bytes:
                response = BotResponse(message="Could not download receipt image from Telegram.")
            else:
                ocr_service = OCRService()
                extracted_text = ocr_service.extract_text(file_bytes)
                parsed = ocr_service.parse_receipt(extracted_text)
                if not parsed:
                    response = BotResponse(message="Receipt text extracted, but no transaction could be inferred.")
                else:
                    BotTransactionService(db).create_transaction_from_parsed(parsed, telegram_user.id)
                    response = BotResponse(
                        message=f"Receipt processed and transaction saved. {BotTransactionService(db)._build_preview(parsed)}",
                        parsed=parsed.model_dump(mode="json"),
                    )
        elif message.text and message.text.startswith("/link "):
            response = handle_link_command(
                message.text,
                bot_user_service,
                message.from_user.id,
                message.from_user.full_name,
                message.from_user.username,
            )
        elif message.text and message.text.startswith("/"):
            response = handle_command(message.text, message_service)
        else:
            response = BotTransactionService(db).create_transaction_from_message(message.text or "", telegram_user)
    except ExpenseFlowException as exc:
        response = BotResponse(message=exc.detail)
    except Exception as exc:
        logger.exception("Unhandled Telegram bot error", exc_info=exc)
        response = BotResponse(message="Something went wrong while processing your message.")

    await telegram_bot_manager.send_text(message.chat.id, response.message)
    return response
