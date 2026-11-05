import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
