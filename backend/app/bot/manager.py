from __future__ import annotations

import logging
from io import BytesIO

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from app.bot.commands import BOT_COMMANDS
from app.core.config import settings


logger = logging.getLogger(__name__)


class TelegramBotManager:
    def __init__(self) -> None:
        self._dispatcher = Dispatcher()
        self._bot: Bot | None = None

    @property
    def dispatcher(self) -> Dispatcher:
        return self._dispatcher

    @property
    def is_enabled(self) -> bool:
        return bool(settings.telegram_bot_token)

    def get_bot(self) -> Bot | None:
        if not self.is_enabled:
            return None

        if self._bot is None:
            self._bot = Bot(
                token=settings.telegram_bot_token,
                default=DefaultBotProperties(parse_mode="HTML"),
            )
        return self._bot

    async def configure_commands(self) -> None:
        bot = self.get_bot()
        if not bot:
            logger.info("Telegram bot token not configured; skipping command sync")
            return

        try:
            await bot.set_my_commands(
                [BotCommand(command=command, description=description) for command, description in BOT_COMMANDS]
            )
        except Exception:
            logger.exception("Failed to configure Telegram commands")

    async def send_text(self, chat_id: int, text: str) -> None:
        bot = self.get_bot()
        if not bot:
            return

        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except Exception:
            logger.exception("Failed to send Telegram message", extra={"chat_id": chat_id})

    async def get_file_bytes(self, file_id: str) -> bytes | None:
        bot = self.get_bot()
        if not bot:
            return None

        try:
            telegram_file = await bot.get_file(file_id)
            buffer = BytesIO()
            await bot.download_file(telegram_file.file_path, destination=buffer)
            return buffer.getvalue()
        except Exception:
            logger.exception("Failed to download Telegram file", extra={"file_id": file_id})
            return None

    async def shutdown(self) -> None:
        if self._bot is not None:
            await self._bot.session.close()


telegram_bot_manager = TelegramBotManager()
