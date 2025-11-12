"""add roles, status fields, audit and translations

Revision ID: 0007_roles_status_translations
Revises: 0006_create_rss_feeds
Create Date: 2025-11-11
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0007_roles_status_translations"
down_revision = "0006_create_rss_feeds"
branch_labels = None
depends_on = None


def upgrade():
    # users.role
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("role", sa.String(length=20), nullable=False, server_default="viewer"))
    # guides.status
    with op.batch_alter_table("guides") as batch_op:
        batch_op.add_column(sa.Column("status", sa.String(length=20), nullable=False, server_default="published"))
    # checklists.status
    with op.batch_alter_table("checklists") as batch_op:
        batch_op.add_column(sa.Column("status", sa.String(length=20), nullable=False, server_default="published"))
    # templates.status
    with op.batch_alter_table("templates") as batch_op:
        batch_op.add_column(sa.Column("status", sa.String(length=20), nullable=False, server_default="published"))

    # audit_logs
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_email", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("entity", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("changes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # translations
    op.create_table(
        "translations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("entity", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("author_email", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # glossary_terms
    op.create_table(
        "glossary_terms",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("term", sa.String(length=255), unique=True, nullable=False),
        sa.Column("uk", sa.String(length=255), nullable=True),
        sa.Column("ru", sa.String(length=255), nullable=True),
        sa.Column("en", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table("glossary_terms")
    op.drop_table("translations")
    op.drop_table("audit_logs")
    with op.batch_alter_table("templates") as batch_op:
        batch_op.drop_column("status")
    with op.batch_alter_table("checklists") as batch_op:
        batch_op.drop_column("status")
    with op.batch_alter_table("guides") as batch_op:
        batch_op.drop_column("status")
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("role")


