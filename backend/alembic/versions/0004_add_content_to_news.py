"""add content column to news

Revision ID: 0004_add_content_to_news
Revises: 0003_create_news
Create Date: 2025-11-10 12:15:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0004_add_content_to_news"
down_revision = "0003_create_news"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("news", sa.Column("content", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("news", "content")


