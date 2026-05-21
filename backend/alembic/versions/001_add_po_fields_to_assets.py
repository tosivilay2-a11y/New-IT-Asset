"""Add PO fields to assets table

Revision ID: 001_add_po_fields
Revises: 
Create Date: 2026-05-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_add_po_fields'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add PO number and attachment path columns to assets table
    op.add_column('assets', sa.Column('po_number', sa.String(100), nullable=True))
    op.add_column('assets', sa.Column('po_attachment_path', sa.String(500), nullable=True))

def downgrade():
    # Remove PO columns
    op.drop_column('assets', 'po_attachment_path')
    op.drop_column('assets', 'po_number')