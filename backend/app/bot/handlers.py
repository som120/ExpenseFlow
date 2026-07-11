from app.bot.keyboards import help_text
from app.schemas.bot import BotResponse
from app.services.bot_user import BotUserService
from app.services.bot_message import BotMessageService


def _command_name(command: str) -> str:
    token = command.strip().split()[0].lower()
    return token.split("@", 1)[0]


def handle_command(command: str, service: BotMessageService) -> BotResponse:
    normalized = _command_name(command)

    if normalized == "/start":
        return BotResponse(
            message=(
                "Welcome to ExpenseFlow. Send expenses like '450 coffee', 'Dinner 200 with Om', "
                "or income like '+500 freelance'."
            ),
            command="start",
        )

    if normalized == "/help":
        return BotResponse(message=help_text(), command="help")

    if normalized == "/balance":
        return service.build_balance_response()

    if normalized == "/summary":
        return service.build_summary_response()

    if normalized == "/month":
        return BotResponse(message="Monthly drill-down will be expanded in Phase 4 analytics.", command="month")

    if normalized == "/report":
        return BotResponse(message="Reports module is planned for later phases.", command="report")

    if normalized == "/export":
        return BotResponse(message="Export flows are planned for a later phase.", command="export")

    if normalized == "/friends":
        return BotResponse(message="Friends management UI/API will expand in upcoming phases.", command="friends")

    if normalized == "/budgets":
        return BotResponse(message="Budget management arrives in Phase 3.", command="budgets")

    if normalized == "/settings":
        return BotResponse(message="Telegram bot settings will expand in later phases.", command="settings")

    return BotResponse(message="Unknown command. Use /help for supported commands.", command="unknown")


def handle_link_command(
    command: str,
    bot_user_service: BotUserService,
    telegram_id: int,
    full_name: str,
    telegram_username: str | None,
) -> BotResponse:
    parts = command.strip().split()
    if len(parts) != 2:
        return BotResponse(message="Usage: /link 123456", command="link")

    linked_user = bot_user_service.consume_manual_link_code(parts[1], telegram_id, full_name, telegram_username)
    return BotResponse(
        message=f"Telegram linked successfully to ExpenseFlow account: {linked_user.full_name}",
        command="link",
    )
