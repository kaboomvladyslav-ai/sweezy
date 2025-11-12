"""create job favorites and search events

Revision ID: 0008_jobs
Revises: 0007_roles_status_translations
Create Date: 2025-11-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0008_jobs'
down_revision = '0007_roles_status_translations'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'job_favorites',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('canton', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )
    op.create_index('ix_job_favorites_user', 'job_favorites', ['user_id'])
    op.create_index('ix_job_favorites_job', 'job_favorites', ['job_id', 'source'])

    op.create_table(
        'job_search_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('keyword', sa.String(), nullable=False),
        sa.Column('canton', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )
    op.create_index('ix_job_search_keyword', 'job_search_events', ['keyword'])


def downgrade() -> None:
    op.drop_index('ix_job_search_keyword', table_name='job_search_events')
    op.drop_table('job_search_events')
    op.drop_index('ix_job_favorites_job', table_name='job_favorites')
    op.drop_index('ix_job_favorites_user', table_name='job_favorites')
    op.drop_table('job_favorites')


