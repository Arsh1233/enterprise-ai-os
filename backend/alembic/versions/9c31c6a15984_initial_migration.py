"""Initial migration

Revision ID: 9c31c6a15984
Revises:
Create Date: 2026-07-08 19:16:14.989126

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "9c31c6a15984"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
