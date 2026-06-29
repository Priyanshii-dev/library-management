"""create book table

Revision ID: 9a174de4afbf
Revises: 7cf562f06416
Create Date: 2026-06-29 13:22:45.292736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a174de4afbf'
down_revision: Union[str, Sequence[str], None] = '7cf562f06416'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
