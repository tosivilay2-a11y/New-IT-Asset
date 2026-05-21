"""Remove foreign key constraint from assignedto column

Revision ID: 009
Revises: 008
Create Date: 2026-05-11 04:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the foreign key constraint on assignedto
    op.drop_constraint('assets_assignedto_fkey', 'assets', type_='foreignkey')


def downgrade() -> None:
    # Recreate the foreign key constraint
    op.create_foreign_key('assets_assignedto_fkey', 'assets', 'users', ['assignedto'], ['userid'])
