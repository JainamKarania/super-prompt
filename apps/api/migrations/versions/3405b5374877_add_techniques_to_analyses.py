"""add techniques to analyses

Revision ID: 3405b5374877
Revises: 0cf963489e09
Create Date: 2026-11-12 18:50:32.723611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3405b5374877'
down_revision: Union[str, Sequence[str], None] = '0cf963489e09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
