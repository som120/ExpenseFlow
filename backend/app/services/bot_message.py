from app.schemas.bot import BotResponse
from app.services.budget import BudgetService
from app.services.friend import FriendService
from app.services.report import ReportService
from app.services.summary import SummaryService


class BotMessageService:
    def __init__(self, summary_service: SummaryService, user_id, report_service: ReportService | None = None, budget_service: BudgetService | None = None, friend_service: FriendService | None = None):
        self.summary_service = summary_service
        self.user_id = user_id
        self.report_service = report_service
        self.budget_service = budget_service
        self.friend_service = friend_service

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

    def build_month_response(self) -> BotResponse:
        summary = self.summary_service.get_summary(self.user_id)
        return BotResponse(
            message=(
                f"This month | Expenses: {summary.total_expenses} | Income: {summary.total_income} | "
                f"Net: {summary.net_savings}"
            ),
            command="month",
        )

    def build_report_response(self) -> BotResponse:
        if not self.report_service:
            return BotResponse(message="Report service is unavailable right now.", command="report")
        report = self.report_service.get_report(self.user_id)
        text = " | ".join(f"{section.title}: {section.value}" for section in report.sections)
        return BotResponse(message=f"Report | {text}", command="report")

    def build_export_response(self) -> BotResponse:
        return BotResponse(
            message="Exports are available in the website Reports page: CSV, Excel, and PDF.",
            command="export",
        )

    def build_friends_response(self) -> BotResponse:
        if not self.friend_service:
            return BotResponse(message="Friend service is unavailable right now.", command="friends")
        friends = self.friend_service.list(self.user_id)
        if not friends:
            return BotResponse(message="No friends added yet.", command="friends")
        names = ", ".join(friend.name for friend in friends[:10])
        return BotResponse(message=f"Friends: {names}", command="friends")

    def build_budgets_response(self) -> BotResponse:
        if not self.budget_service:
            return BotResponse(message="Budget service is unavailable right now.", command="budgets")
        budgets = self.budget_service.list(self.user_id)
        if not budgets:
            return BotResponse(message="No budgets created yet.", command="budgets")
        items = "; ".join(f"{budget.name}: ₹{budget.remaining_amount} left" for budget in budgets[:5])
        return BotResponse(message=f"Budgets | {items}", command="budgets")

    def build_settings_response(self) -> BotResponse:
        return BotResponse(
            message="Settings | Telegram account is linked. Use the website for advanced preferences.",
            command="settings",
        )
