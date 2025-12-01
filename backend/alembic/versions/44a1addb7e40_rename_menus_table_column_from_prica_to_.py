"""rename menus table column from prica to price

Revision ID: 44a1addb7e40
Revises: 3612adbfa139
Create Date: 2025-12-01 14:29:44.394256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44a1addb7e40'
down_revision: Union[str, Sequence[str], None] = '3612adbfa139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'menus',
        'prica',
        new_column_name='price',
        existing_type=sa.Integer()
    )


def downgrade() -> None:
    op.alter_column(
        'menus',
        'price',
        new_column_name='prica',
        existing_type=sa.Integer()
    )
