"""add new column to posts table

Revision ID: 8cc7d5a38dd5
Revises: 2ec87316b570
Create Date: 2022-08-01 13:57:55.189639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cc7d5a38dd5'
down_revision = '2ec87316b570'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
