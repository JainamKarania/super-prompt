import asyncio
import sys

from app.db.session import engine
from app.services.retrieval import PgRetriever


async def main(query: str) -> None:
    for g in await PgRetriever().search(query, 3):
        print(f"- {g.title}  ({g.source})")
    await engine.dispose()


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "format: the desired output format is not stated"
    asyncio.run(main(text))
