"""add content column into post table

Revision ID: 3a4d46ec14ea
Revises: 455213a27fc5
Create Date: 2024-07-03 19:54:47.177455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a4d46ec14ea'
down_revision: Union[str, None] = '455213a27fc5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('content', sa.String(), 
                            nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content') 
