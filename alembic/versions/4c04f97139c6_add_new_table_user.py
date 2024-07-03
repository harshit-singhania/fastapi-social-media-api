"""add new table - user

Revision ID: 4c04f97139c6
Revises: 3a4d46ec14ea
Create Date: 2024-07-03 19:59:10.437865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c04f97139c6'
down_revision: Union[str, None] = '3a4d46ec14ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False), 
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False), 
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
