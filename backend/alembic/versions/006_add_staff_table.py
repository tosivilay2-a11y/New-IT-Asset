"""Add staff table

Revision ID: 006
Revises: 005
Create Date: 2026-05-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create staff table
    op.create_table(
        'staff',
        sa.Column('staffid', sa.Integer(), nullable=False),
        sa.Column('employeeid', sa.String(), nullable=False),
        sa.Column('fullname', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('department', sa.String(), nullable=True),
        sa.Column('position', sa.String(), nullable=True),
        sa.Column('employmentstatus', sa.String(), nullable=False, server_default='Active'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('staffid')
    )
    op.create_index(op.f('ix_staff_employeeid'), 'staff', ['employeeid'], unique=True)
    op.create_index(op.f('ix_staff_email'), 'staff', ['email'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_staff_email'), table_name='staff')
    op.drop_index(op.f('ix_staff_employeeid'), table_name='staff')
    op.drop_table('staff')
