"""Add timestamp fields to all tables

Revision ID: 67a0922ba237
Revises: 4814812fb4af
Create Date: 2025-03-09 14:06:57.701696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67a0922ba237'
down_revision: Union[str, None] = '4814812fb4af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('order_items', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('orders', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('orders', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('payments', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('payments', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('products', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('products', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('reviews', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('reviews', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('reviews', 'updated_at')
    op.drop_column('reviews', 'created_at')
    op.drop_column('products', 'updated_at')
    op.drop_column('products', 'created_at')
    op.drop_column('payments', 'updated_at')
    op.drop_column('payments', 'created_at')
    op.drop_column('orders', 'updated_at')
    op.drop_column('orders', 'created_at')
    op.drop_column('order_items', 'updated_at')
    op.drop_column('order_items', 'created_at')
    # ### end Alembic commands ###
