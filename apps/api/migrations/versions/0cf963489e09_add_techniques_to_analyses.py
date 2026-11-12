"""add techniques to analyses

Revision ID: 0cf963489e09
Revises: 84d6d10b2545
Create Date: 2026-11-12 17:57:14.297581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0cf963489e09'
down_revision: Union[str, Sequence[str], None] = '84d6d10b2545'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "analyses",
        sa.Column(
            "techniques",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("analyses", "techniques")
