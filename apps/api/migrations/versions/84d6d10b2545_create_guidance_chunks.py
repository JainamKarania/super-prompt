"""create guidance chunks

Revision ID: 84d6d10b2545
Revises: cf803d5d2169
Create Date: 2026-11-10 18:42:53.692354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84d6d10b2545'
down_revision: Union[str, Sequence[str], None] = 'cf803d5d2169'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute(
        """
        CREATE TABLE guidance_chunks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            content_hash VARCHAR(64) NOT NULL UNIQUE,
            embedding vector(384) NOT NULL
        )
        """
    )
    op.execute(
        "CREATE INDEX ix_guidance_chunks_embedding "
        "ON guidance_chunks USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    op.execute("DROP TABLE guidance_chunks")