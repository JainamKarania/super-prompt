from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import EMBEDDING_DIM
from app.db.models import GuidanceChunk
from app.services.retrieval import PgRetriever


def _vec(i: int) -> list[float]:
    v = [0.0] * EMBEDDING_DIM
    v[i] = 1.0
    return v


class FakeEmbedder:
    def __init__(self, vector: list[float]) -> None:
        self._vector = vector

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._vector for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._vector


async def test_search_returns_the_nearest_notes_first(
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    async with session_maker() as session:
        session.add_all(
            GuidanceChunk(
                source=f"https://example.com/{i}",
                title=f"note {i}",
                content=f"content {i}",
                content_hash=str(i),
                embedding=_vec(i),
            )
            for i in range(3)
        )
        await session.commit()

    query = _vec(1)
    query[0] = 0.1  # closest to note 1, then note 0, then note 2
    retriever = PgRetriever(embedder=FakeEmbedder(query), session_factory=session_maker)

    found = await retriever.search("anything", 2)

    assert [g.title for g in found] == ["note 1", "note 0"]
    assert found[0].source == "https://example.com/1"
