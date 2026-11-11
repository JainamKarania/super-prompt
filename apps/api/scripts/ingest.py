import asyncio
import sys

from sqlalchemy import delete, select

from app.db.models import GuidanceChunk
from app.db.session import SessionLocal, engine
from app.services.embedder import FastEmbedder
from app.services.knowledge import KNOWLEDGE_DIR, content_hash, parse_note


async def main() -> None:
    paths = sorted(KNOWLEDGE_DIR.glob("*.md"))
    if not paths:
        sys.exit(f"No notes found in {KNOWLEDGE_DIR}")

    wanted = {}
    for path in paths:
        title, source, content = parse_note(path)
        wanted[content_hash(title, content)] = (title, source, content)

    async with SessionLocal() as session:
        existing = set((await session.scalars(select(GuidanceChunk.content_hash))).all())
        stale = existing - wanted.keys()
        new = [h for h in wanted if h not in existing]

        if stale:
            await session.execute(
                delete(GuidanceChunk).where(GuidanceChunk.content_hash.in_(stale))
            )
        if new:
            texts = [f"{wanted[h][0]}\n\n{wanted[h][2]}" for h in new]
            vectors = FastEmbedder().embed_documents(texts)
            session.add_all(
                GuidanceChunk(
                    source=wanted[h][1],
                    title=wanted[h][0],
                    content=wanted[h][2],
                    content_hash=h,
                    embedding=vector,
                )
                for h, vector in zip(new, vectors, strict=True)
            )
        await session.commit()

    await engine.dispose()
    print(f"notes: {len(wanted)}, added: {len(new)}, removed: {len(stale)}")


if __name__ == "__main__":
    asyncio.run(main())
