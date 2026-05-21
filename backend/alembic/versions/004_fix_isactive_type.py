"""Fix isactive column type from smallint to boolean

Revision ID: 004_fix_isactive_type
Revises: 003
Create Date: 2026-05-08 06:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_fix_isactive_type'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Fix isactive column type from smallint to boolean
    # First, alter the column type
    op.alter_column('assets', 'isactive',
                    existing_type=sa.SmallInteger(),
                    type_=sa.Boolean(),
                    existing_nullable=True,
                    nullable=False,
                    server_default=sa.true())


def downgrade() -> None:
    # Revert back to smallint if needed
    op.alter_column('assets', 'isactive',
                    existing_type=sa.Boolean(),
                    type_=sa.SmallInteger(),
                    existing_nullable=False,
                    nullable=True,
                    server_default=None)
