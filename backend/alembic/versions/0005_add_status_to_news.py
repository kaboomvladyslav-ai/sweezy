"""add status to news

Revision ID: 0005_add_status_to_news
Revises: 0004_add_content_to_news
Create Date: 2025-11-10 12:22:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "0005_add_status_to_news"
down_revision = "0004_add_content_to_news"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("news", sa.Column("status", sa.String(length=16), nullable=False, server_default="published"))
    op.alter_column("news", "status", server_default=None)


def downgrade() -> None:
    op.drop_column("news", "status")


