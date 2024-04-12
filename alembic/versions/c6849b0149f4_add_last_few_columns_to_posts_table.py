"""add last few columns to posts table

Revision ID: c6849b0149f4
Revises: d4480ab8adcc
Create Date: 2024-04-09 07:09:47.304450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6849b0149f4'
down_revision: Union[str, None] = 'd4480ab8adcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    
    pass


def downgrade() -> None:
    op.drop_column('post', 'published')
    op.drop_column('posts', 'created_at')
    pass
