# ExpenseFlow

ExpenseFlow is an AI-ready personal finance and expense sharing platform.

## Phase 1 status

This repository currently includes a production-minded backend foundation for:

- FastAPI application setup
- SQLAlchemy 2.0 models
- Alembic migration scaffolding
- JWT authentication
- Transaction CRUD APIs
- Summary endpoint
- Test scaffolding for auth and transactions

## Phase 2 status

The backend now also includes:

- Telegram bot scaffolding with aiogram
- Webhook endpoint for Telegram updates
- Regex-based natural language parser for expense/income messages
- Bot command handlers for `/start`, `/help`, `/balance`, `/summary`, `/month`, `/report`, `/export`, `/friends`, `/budgets`, `/settings`

## Structure

- `backend/` – FastAPI app, migrations, and tests
- `docs/` – implementation notes by phase

## Environment

Use `backend/env.sample` as the starting point for your local `.env` file.

Optional Telegram settings:

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_WEBHOOK_SECRET=your-webhook-secret
TELEGRAM_WEBHOOK_PATH=/api/v1/telegram/webhook
```

## Quick start

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp env.sample .env
alembic upgrade head
uvicorn app.main:app --reload
```

## API docs

After starting the backend:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Current endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/transactions`
- `GET /api/v1/transactions`
- `GET /api/v1/transactions/{transaction_id}`
- `PUT /api/v1/transactions/{transaction_id}`
- `DELETE /api/v1/transactions/{transaction_id}`
- `GET /api/v1/summary`
- `POST /api/v1/telegram/webhook`
