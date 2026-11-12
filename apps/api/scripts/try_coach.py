import asyncio

from app.db.session import engine
from app.services.coach import get_coach

PROMPT = (
    "Write a 600-word blog post for junior developers about Git branching. "
    "Use a friendly tone, three headings, and one example per heading. Output in Markdown"
)


async def main() -> None:
    out = await get_coach().coach(PROMPT, "writing")
    print(out.model_dump_json(indent=2))
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
