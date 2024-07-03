"""add some more cols to post table

Revision ID: c1a94d574b4d
Revises: 71669b0c9d4c
Create Date: 2024-07-03 20:13:18.792717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1a94d574b4d'
down_revision: Union[str, None] = '71669b0c9d4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', 
                                     sa.Boolean(), nullable=False, 
                                     server_default='TRUE'),) 
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
        server_default=sa.text('NOW')
    ),)


def downgrade() -> None:
    op.drop_column('posts', 'published') 
    op.drop_column('posts', 'created_at')
