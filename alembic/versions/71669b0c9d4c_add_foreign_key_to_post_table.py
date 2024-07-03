"""add foreign key to post table

Revision ID: 71669b0c9d4c
Revises: 4c04f97139c6
Create Date: 2024-07-03 20:04:40.900224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71669b0c9d4c'
down_revision: Union[str, None] = '4c04f97139c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))

    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
