# Phase 3 Implementation Notes

## Scope delivered

- Backend additions for friends and budgets CRUD
- Alembic migration for budgets
- Phase 3 frontend scaffold with Next.js 15 app router
- Tailwind-based SaaS dashboard layout
- Auth pages for login and registration
- Dashboard, transactions, friends, and budgets pages
- React Query client utilities and Zustand auth store
- Quick add transaction form wired to backend API
- Telegram login/linking hooks so website and bot can share the same user identity

## Backend APIs added

- `GET /friends`
- `POST /friends`
- `PUT /friends/{id}`
- `DELETE /friends/{id}`
- `GET /budgets`
- `POST /budgets`
- `PUT /budgets/{id}`
- `DELETE /budgets/{id}`

## Frontend notes

- Set `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local` using `frontend/env.sample` as a base.
- Set `NEXT_PUBLIC_TELEGRAM_BOT_USERNAME` in `frontend/.env.local` to enable Telegram login/link UI.
- Current frontend is production-oriented scaffold with core pages and data hooks.
- Frontend auth now persists in local storage, so after login the dashboard can fetch real user data instead of showing guest defaults.
- Advanced polish like command palette, dark/light switching, skeletons, and dialogs can be layered next.

## Verification notes

- Python source compilation verified with `python3 -m compileall app tests`.
- Frontend dependencies/build were not executed in this sandbox.
