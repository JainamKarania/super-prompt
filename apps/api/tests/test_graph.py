from typing import Any

from app.schemas import Dimension, DimensionName, TaskType
from app.services.graph import (
    MAX_REWRITES,
    CoachState,
    RewriteOut,
    build_graph,
    build_query,
    route_after_verify,
)
from app.services.retrieval import Guidance

NAMES: list[DimensionName] = ["clarity", "context", "constraints", "format", "examples"]

NOTE = Guidance(
    title="Specify the output format",
    source="https://example.com/format",
    content="Name the format.",
)


def _dims(score: float) -> list[Dimension]:
    return [Dimension(name=n, score=score, feedback="f") for n in NAMES]


class FakeSteps:
    """Returns the given overall scores, one per score() call, in order."""

    def __init__(self, scores: list[float]) -> None:
        self._scores = list(scores)
        self.score_calls = 0
        self.rewrite_calls = 0
        self.retry_flags: list[bool] = []
        self.guidance_seen: list[list[Guidance]] = []

    async def score(self, prompt: str, task: TaskType) -> list[Dimension]:
        self.score_calls += 1
        return _dims(self._scores.pop(0))

    async def rewrite(
        self,
        prompt: str,
        task: TaskType,
        dimensions: list[Dimension],
        guidance: list[Guidance],
        retry: bool,
    ) -> RewriteOut:
        self.rewrite_calls += 1
        self.retry_flags.append(retry)
        self.guidance_seen.append(guidance)
        return RewriteOut(improved=f"rewrite {self.rewrite_calls}", changes=["c"])


class FakeRetriever:
    def __init__(self, found: list[Guidance] | None = None, fail: bool = False) -> None:
        self.found = found or []
        self.fail = fail
        self.queries: list[str] = []

    async def search(self, query: str, k: int) -> list[Guidance]:
        self.queries.append(query)
        if self.fail:
            raise RuntimeError("database is down")
        return self.found


async def _run(
    scores: list[float], retriever: FakeRetriever | None = None
) -> tuple[FakeSteps, dict[str, Any]]:
    steps = FakeSteps(scores)
    graph = build_graph(steps, retriever or FakeRetriever())
    final = await graph.ainvoke({"prompt": "p", "task": "writing"})
    return steps, final


async def test_stops_when_first_rewrite_improves() -> None:
    steps, final = await _run([2, 8])
    assert steps.rewrite_calls == 1
    assert steps.score_calls == 2
    assert final["best_improved"] == "rewrite 1"


async def test_retries_once_when_first_rewrite_is_not_better() -> None:
    steps, final = await _run([5, 4, 7])
    assert steps.rewrite_calls == 2
    assert steps.retry_flags == [False, True]
    assert final["best_improved"] == "rewrite 2"


async def test_gives_up_after_max_rewrites_and_keeps_the_best() -> None:
    steps, final = await _run([5, 4, 3])
    assert steps.rewrite_calls == MAX_REWRITES == 2
    assert final["best_improved"] == "rewrite 1"


async def test_guidance_is_passed_to_every_rewrite_and_searched_once() -> None:
    retriever = FakeRetriever(found=[NOTE])
    steps, final = await _run([5, 4, 7], retriever)
    assert steps.guidance_seen == [[NOTE], [NOTE]]
    assert final["guidance"] == [NOTE]
    assert len(retriever.queries) == 1


async def test_a_retrieval_failure_does_not_stop_the_coach() -> None:
    steps, final = await _run([2, 8], FakeRetriever(fail=True))
    assert final["best_improved"] == "rewrite 1"
    assert steps.guidance_seen == [[]]
    assert final["guidance"] == []


def test_build_query_uses_the_two_weakest_dimensions() -> None:
    dims = [
        Dimension(name="clarity", score=9, feedback="clear enough"),
        Dimension(name="context", score=2, feedback="no audience"),
        Dimension(name="constraints", score=8, feedback="limits fine"),
        Dimension(name="format", score=1, feedback="no format"),
        Dimension(name="examples", score=5, feedback="one example"),
    ]
    query = build_query("write a blog", dims)
    assert "format: no format" in query
    assert "context: no audience" in query
    assert "clarity" not in query
    assert query.endswith("write a blog")


def _state(original: float, new: float, attempts: int) -> CoachState:
    return {"original_overall": original, "new_overall": new, "attempts": attempts}


def test_route_done_when_improved() -> None:
    assert route_after_verify(_state(3, 6, 1)) == "done"


def test_route_retries_when_not_improved() -> None:
    assert route_after_verify(_state(5, 5, 1)) == "rewrite"


def test_route_stops_at_the_attempt_limit() -> None:
    assert route_after_verify(_state(5, 4, MAX_REWRITES)) == "done"
