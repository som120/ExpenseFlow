from pydantic import BaseModel


class BotResponse(BaseModel):
    message: str
    command: str | None = None
    parsed: dict | None = None
