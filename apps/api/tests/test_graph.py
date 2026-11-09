from app.schemas import Dimension, DimensionName, TaskType
from app.services.graph import (
    MAX_REWRITES,
    CoachState,
    RewriteOut,
    build_graph,
    route_after_verify,
)

NAMES: list[DimensionName] = ["clarity", "context", "constraints", "format", "examples"]


def _dims(score: float) -> list[Dimension]:
    return [Dimension(name=n, score=score, feedback="f") for n in NAMES]


class FakeSteps:
    """Returns the given overall scores, one per score() call, in order."""

    def __init__(self, scores: list[float]) -> None:
        self._scores = list(scores)
        self.score_calls = 0
        self.rewrite_calls = 0
        self.retry_flags: list[bool] = []

    async def score(self, prompt: str, task: TaskType) -> list[Dimension]:
        self.score_calls += 1
        return _dims(self._scores.pop(0))

    async def rewrite(
        self, prompt: str, task: TaskType, dimensions: list[Dimension], retry: bool
    ) -> RewriteOut:
        self.rewrite_calls += 1
        self.retry_flags.append(retry)
        return RewriteOut(improved=f"rewrite {self.rewrite_calls}", changes=["c"])


async def _run(scores: list[float]) -> tuple[FakeSteps, dict[str, object]]:
    steps = FakeSteps(scores)
    final = await build_graph(steps).ainvoke({"prompt": "p", "task": "writing"})
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


def _state(original: float, new: float, attempts: int) -> CoachState:
    return {"original_overall": original, "new_overall": new, "attempts": attempts}


def test_route_done_when_improved() -> None:
    assert route_after_verify(_state(3, 6, 1)) == "done"


def test_route_retries_when_not_improved() -> None:
    assert route_after_verify(_state(5, 5, 1)) == "rewrite"


def test_route_stops_at_the_attempt_limit() -> None:
    assert route_after_verify(_state(5, 4, MAX_REWRITES)) == "done"
