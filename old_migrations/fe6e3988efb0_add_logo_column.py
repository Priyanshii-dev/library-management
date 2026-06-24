"""add logo column

Revision ID: fe6e3988efb0
Revises: 88cfe6cee905
Create Date: 2026-06-24 15:50:18.994042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe6e3988efb0'
down_revision: Union[str, Sequence[str], None] = '88cfe6cee905'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
