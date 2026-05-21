"""Add asset check-in/check-out history table

Revision ID: 008
Revises: 007
Create Date: 2026-05-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create asset_checkinout_history table
    op.create_table(
        'asset_checkinout_history',
        sa.Column('historyid', sa.Integer(), nullable=False),
        sa.Column('assetid', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('userid', sa.Integer(), nullable=True),
        sa.Column('staffid', sa.Integer(), nullable=True),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('condition_before', sa.String(), nullable=True),
        sa.Column('condition_after', sa.String(), nullable=True),
        sa.Column('location_before', sa.Integer(), nullable=True),
        sa.Column('location_after', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('historyid')
    )
    op.create_index(op.f('ix_asset_checkinout_history_assetid'), 'asset_checkinout_history', ['assetid'])
    op.create_index(op.f('ix_asset_checkinout_history_created_at'), 'asset_checkinout_history', ['created_at'])


def downgrade() -> None:
    op.drop_index(op.f('ix_asset_checkinout_history_created_at'), table_name='asset_checkinout_history')
    op.drop_index(op.f('ix_asset_checkinout_history_assetid'), table_name='asset_checkinout_history')
    op.drop_table('asset_checkinout_history')
