from __future__ import annotations

import logging

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

    async def shutdown(self) -> None:
        if self._bot is not None:
            await self._bot.session.close()


telegram_bot_manager = TelegramBotManager()
