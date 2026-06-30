"""create book table

Revision ID: d7e74ab92191
Revises: 0441cd358134
Create Date: 2026-06-30 14:27:53.732314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7e74ab92191'
down_revision: Union[str, Sequence[str], None] = '0441cd358134'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
