from pydantic import BaseModel


class TelegramWebhookMessage(BaseModel):
    chat_id: int
    text: str
    telegram_user_id: int | None = None
    telegram_username: str | None = None
    full_name: str | None = None


class BotResponse(BaseModel):
    message: str
    command: str | None = None
    parsed: dict | None = None
