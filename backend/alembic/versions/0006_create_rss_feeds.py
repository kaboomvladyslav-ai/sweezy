"""create rss_feeds table

Revision ID: 0006_create_rss_feeds
Revises: 0005_add_status_to_news
Create Date: 2025-11-10 14:15:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "0006_create_rss_feeds"
down_revision = "0005_add_status_to_news"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rss_feeds",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("url", sa.String(length=1000), nullable=False, unique=True),
        sa.Column("language", sa.String(length=8), nullable=False, server_default="uk"),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="draft"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("max_items", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("download_images", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("last_imported_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=False), nullable=False),
    )
    op.create_index("ix_rss_feeds_enabled", "rss_feeds", ["enabled"])


def downgrade() -> None:
    op.drop_index("ix_rss_feeds_enabled", table_name="rss_feeds")
    op.drop_table("rss_feeds")


