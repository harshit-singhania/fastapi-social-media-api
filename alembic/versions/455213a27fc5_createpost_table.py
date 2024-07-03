"""createpost table

Revision ID: 455213a27fc5
Revises: 
Create Date: 2024-07-03 19:32:40.387061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '455213a27fc5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
