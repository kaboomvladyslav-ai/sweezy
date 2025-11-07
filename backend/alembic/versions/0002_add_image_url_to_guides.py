"""add image_url to guides

Revision ID: 0002_add_image
Revises: 0001_init
Create Date: 2025-11-06
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_add_image'
down_revision = '0001_init'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('guides') as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('guides') as batch_op:
        batch_op.drop_column('image_url')


