"""Add cost center field to assets

Revision ID: 002_add_cost_center_field
Revises: 001_add_po_fields_to_assets
Create Date: 2026-05-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_cost_center_field'
down_revision = '001_add_po_fields'
branch_labels = None
depends_on = None

def upgrade():
    # Add cost_center column to assets table
    op.add_column('assets', sa.Column('cost_center', sa.String(100), nullable=True))

def downgrade():
    # Remove cost_center column from assets table
    op.drop_column('assets', 'cost_center')