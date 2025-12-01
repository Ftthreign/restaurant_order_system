"""update menu_id to on delete set null

Revision ID: d23c0f9a5a76
Revises: 44a1addb7e40
Create Date: 2025-12-02 00:58:11.124148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd23c0f9a5a76'
down_revision: Union[str, Sequence[str], None] = '44a1addb7e40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Drop old FK
    op.drop_constraint('order_items_ibfk_1', 'order_items', type_='foreignkey')

    # 2. Alter column to nullable
    op.alter_column(
        'order_items',
        'menu_id',
        existing_type=sa.CHAR(36),
        nullable=True
    )

    # 3. Create new FK with ON DELETE SET NULL
    op.create_foreign_key(
        'order_items_ibfk_1',
        'order_items',
        'menus',
        ['menu_id'],
        ['id'],
        ondelete="SET NULL"
    )


def downgrade():
    # balikkan jika perlu

    op.drop_constraint('order_items_ibfk_1', 'order_items', type_='foreignkey')

    op.alter_column(
        'order_items',
        'menu_id',
        existing_type=sa.CHAR(36),
        nullable=False
    )

    op.create_foreign_key(
        'order_items_ibfk_1',
        'order_items',
        'menus',
        ['menu_id'],
        ['id']
    )
