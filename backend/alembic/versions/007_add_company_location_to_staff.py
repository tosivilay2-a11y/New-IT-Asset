"""Add company and location to staff table

Revision ID: 007
Revises: 006
Create Date: 2026-05-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add company and location columns to staff table
    op.add_column('staff', sa.Column('companyid', sa.Integer(), nullable=True))
    op.add_column('staff', sa.Column('locationid', sa.Integer(), nullable=True))
    
    # Create foreign key constraints
    op.create_foreign_key('fk_staff_company', 'staff', 'company', ['companyid'], ['companyid'])
    op.create_foreign_key('fk_staff_location', 'staff', 'location', ['locationid'], ['locationid'])
    
    # Create indexes
    op.create_index(op.f('ix_staff_companyid'), 'staff', ['companyid'])
    op.create_index(op.f('ix_staff_locationid'), 'staff', ['locationid'])


def downgrade() -> None:
    op.drop_index(op.f('ix_staff_locationid'), table_name='staff')
    op.drop_index(op.f('ix_staff_companyid'), table_name='staff')
    op.drop_constraint('fk_staff_location', 'staff', type_='foreignkey')
    op.drop_constraint('fk_staff_company', 'staff', type_='foreignkey')
    op.drop_column('staff', 'locationid')
    op.drop_column('staff', 'companyid')
