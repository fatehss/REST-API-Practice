"""remove stock from product model

Revision ID: ef0d6bd6acfc
Revises: 752b4dc02d4d
Create Date: 2025-03-09 18:57:40.990618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef0d6bd6acfc'
down_revision: Union[str, None] = '752b4dc02d4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
