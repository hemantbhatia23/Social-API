"""add user table

Revision ID: 279467fc06f2
Revises: 8cc7d5a38dd5
Create Date: 2022-08-01 14:01:15.866100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '279467fc06f2'
down_revision = '8cc7d5a38dd5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
        sa.Column('id', sa.Integer(), nullable = False),
        sa.Column('email', sa.String(), nullable = False),
        sa.Column('password', sa.String(), nullable = False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default = sa.text('now()'),nullable = False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
