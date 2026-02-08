"""add_imagecolumn

Revision ID: b3f1620fb5a8
Revises: ad2fbe9e404c
Create Date: 2026-02-08 23:44:57.651705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f1620fb5a8'
down_revision: Union[str, Sequence[str], None] = 'ad2fbe9e404c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('pizzas', sa.Column('image_url', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('pizzas', 'image_url')
    pass
