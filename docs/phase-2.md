# Phase 2 Implementation Notes

## Scope delivered

- Telegram bot scaffolding with aiogram
- Webhook route at `/api/v1/telegram/webhook`
- Webhook route now accepts native Telegram `Update` payloads
- Supported command handling for:
  - `/start`
  - `/help`
  - `/balance`
  - `/summary`
  - `/month`
  - `/report`
  - `/export`
  - `/friends`
  - `/budgets`
  - `/settings`
- Regex + keyword parser for:
  - personal expenses
  - income entries
  - shared expenses
  - borrowed expenses
- Parser tests and webhook tests

## Parser behavior

- `450 coffee` → personal expense
- `Received 45000 salary` → income
- `Dinner 900 with Om Rahul` → shared expense split equally
- `Cab 450 paid by Om` → borrowed expense

## Design choices

- Parsing logic lives in `app/parser/` so it can later be replaced by an AI-powered parser without touching routers.
- Webhook currently returns previews and command responses; authenticated user-to-Telegram identity linking is left for a later auth expansion.
- Webhook also sends text replies back to Telegram chats when a bot token is configured.
- Command handlers are lightweight and intentionally keep advanced reporting/budget flows as placeholders until later phases.

## Verification notes

- Source compilation verified with `python3 -m compileall app tests`.
- Full `pytest` execution could not be run in this sandbox because `pytest` was unavailable and local virtualenv creation/install failed under sandbox restrictions.
