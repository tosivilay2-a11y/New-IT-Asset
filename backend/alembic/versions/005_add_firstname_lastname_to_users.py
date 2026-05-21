"""Add firstname and lastname columns to users table

Revision ID: 005_add_firstname_lastname
Revises: 004_fix_isactive_type
Create Date: 2026-05-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_add_firstname_lastname'
down_revision = '004_fix_isactive_type'
branch_labels = None
depends_on = None

def upgrade():
    # Add firstname and lastname columns to users table
    op.add_column('users', sa.Column('firstname', sa.String(100), nullable=True))
    op.add_column('users', sa.Column('lastname', sa.String(100), nullable=True))

def downgrade():
    # Remove firstname and lastname columns
    op.drop_column('users', 'lastname')
    op.drop_column('users', 'firstname')
