"""migrate if changes are there

Revision ID: 752b4dc02d4d
Revises: 770a08849fe5
Create Date: 2025-03-09 18:53:02.291284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '752b4dc02d4d'
down_revision: Union[str, None] = '770a08849fe5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
