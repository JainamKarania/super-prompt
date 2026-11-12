import hashlib
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AnalysisRecord


def prompt_hash(prompt: str, task: str) -> str:
    normalized = " ".join(prompt.split()).lower()
    return hashlib.sha256(f"{task}|{normalized}".encode()).hexdigest()


async def create(
    session: AsyncSession,
    *,
    original: str,
    improved: str,
    task: str,
    overall: float,
    dimensions: list[dict[str, Any]],
    changes: list[str],
    techniques: list[dict[str, str]],
) -> AnalysisRecord:
    record = AnalysisRecord(
        original=original,
        improved=improved,
        task=task,
        overall=overall,
        dimensions=dimensions,
        changes=changes,
        techniques=techniques,
        prompt_hash=prompt_hash(original, task),
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


async def get(session: AsyncSession, analysis_id: uuid.UUID) -> AnalysisRecord | None:
    return await session.get(AnalysisRecord, analysis_id)


async def list_recent(session: AsyncSession, limit: int = 50) -> list[AnalysisRecord]:
    result = await session.scalars(
        select(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit)
    )
    return list(result)
