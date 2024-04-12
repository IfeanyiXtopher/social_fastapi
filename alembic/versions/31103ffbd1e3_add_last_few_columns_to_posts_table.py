"""add last few columns to posts table

Revision ID: 31103ffbd1e3
Revises: c6849b0149f4
Create Date: 2024-04-09 07:50:20.132375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31103ffbd1e3'
down_revision: Union[str, None] = 'c6849b0149f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
