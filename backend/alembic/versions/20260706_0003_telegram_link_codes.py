"""Add telegram link code fields

Revision ID: 20260706_0003
Revises: 20260705_0002
Create Date: 2026-07-06 00:00:00
"""

import sqlalchemy as sa
from alembic import op


revision = "20260706_0003"
down_revision = "20260705_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("telegram_link_code", sa.String(length=12), nullable=True))
    op.add_column("users", sa.Column("telegram_link_code_expires_at", sa.DateTime(timezone=True), nullable=True))
    op.create_unique_constraint("uq_users_telegram_link_code", "users", ["telegram_link_code"])


def downgrade() -> None:
    op.drop_constraint("uq_users_telegram_link_code", "users", type_="unique")
    op.drop_column("users", "telegram_link_code_expires_at")
    op.drop_column("users", "telegram_link_code")
