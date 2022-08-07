"""Add foreign key to post table

Revision ID: ac70907887b5
Revises: 279467fc06f2
Create Date: 2022-08-01 14:06:49.913804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac70907887b5'
down_revision = '279467fc06f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id' ,sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fkey',source_table='posts', referent_table='users', 
            local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass



def downgrade() -> None:
    op.drop_constraint('posts_users_fkey',table_name = 'posts')
    op.drop_column('posts','owner_id')
    pass
