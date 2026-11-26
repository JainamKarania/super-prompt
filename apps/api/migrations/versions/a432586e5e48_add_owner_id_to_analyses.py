"""add owner id to analyses

Revision ID: a432586e5e48
Revises: 3405b5374877
Create Date: 2026-11-26 12:24:59.487676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a432586e5e48'
down_revision: Union[str, Sequence[str], None] = '3405b5374877'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "analyses",
        sa.Column("owner_id", sa.String(length=64), nullable=False, server_default="legacy"),
    )
    op.alter_column("analyses", "owner_id", server_default=None)
    op.create_index(op.f("ix_analyses_owner_id"), "analyses", ["owner_id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_analyses_owner_id"), table_name="analyses")
    op.drop_column("analyses", "owner_id")
