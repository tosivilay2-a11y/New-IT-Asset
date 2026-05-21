"""Add cost_center column to assets table

Revision ID: 003
Revises: 002
Create Date: 2026-05-08 03:52:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add cost_center column to assets table
    op.add_column('assets', sa.Column('cost_center', sa.String(100), nullable=True))


def downgrade() -> None:
    # Remove cost_center column from assets table
    op.drop_column('assets', 'cost_center')
