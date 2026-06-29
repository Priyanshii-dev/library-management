"""create book table

Revision ID: 0441cd358134
Revises: 9a174de4afbf
Create Date: 2026-06-29 15:03:46.971509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0441cd358134'
down_revision: Union[str, Sequence[str], None] = '9a174de4afbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
