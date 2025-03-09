"""Add processing enum to ORder class

Revision ID: 770a08849fe5
Revises: 67a0922ba237
Create Date: 2025-03-09 14:18:22.834325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '770a08849fe5'
down_revision: Union[str, None] = '67a0922ba237'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
