import uuid
from datetime import datetime
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Float, Index, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import EMBEDDING_DIM


class Base(DeclarativeBase):
    pass


class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original: Mapped[str] = mapped_column(Text)
    improved: Mapped[str] = mapped_column(Text)
    task: Mapped[str] = mapped_column(String(20))
    overall: Mapped[float] = mapped_column(Float)
    dimensions: Mapped[list[dict[str, Any]]] = mapped_column(JSONB)
    changes: Mapped[list[str]] = mapped_column(JSONB)
    prompt_hash: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    techniques: Mapped[list[dict[str, str]]] = mapped_column(
        JSONB, server_default=text("'[]'::jsonb")
    )


class GuidanceChunk(Base):
    __tablename__ = "guidance_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIM))

    __table_args__ = (
        Index(
            "ix_guidance_chunks_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )
