import asyncio
from typing import Protocol

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import GuidanceChunk
from app.db.session import SessionLocal
from app.services.embedder import Embedder, get_embedder


class Guidance(BaseModel):
    title: str
    source: str
    content: str


class Retriever(Protocol):
    async def search(self, query: str, k: int) -> list[Guidance]: ...


class PgRetriever:
    def __init__(
        self,
        embedder: Embedder | None = None,
        session_factory: async_sessionmaker[AsyncSession] = SessionLocal,
    ) -> None:
        self._embedder = embedder
        self._session_factory = session_factory

    def _embed(self, query: str) -> list[float]:
        embedder = self._embedder or get_embedder()
        return embedder.embed_query(query)

    async def search(self, query: str, k: int) -> list[Guidance]:
        # embedding is CPU work, so keep it off the event loop
        vector = await asyncio.to_thread(self._embed, query)
        async with self._session_factory() as session:
            result = await session.execute(
                select(GuidanceChunk.title, GuidanceChunk.source, GuidanceChunk.content)
                .order_by(GuidanceChunk.embedding.op("<=>")(vector))
                .limit(k)
            )
            return [
                Guidance(title=row.title, source=row.source, content=row.content)
                for row in result.all()
            ]
