"""add content to posts table

Revision ID: 551d335d25ce
Revises: f4959387be71
Create Date: 2024-04-08 15:10:17.829740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '551d335d25ce'
down_revision: Union[str, None] = 'f4959387be71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
