import logging
from typing import Any, Literal, Protocol, TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from app.schemas import Dimension, TaskType
from app.services.retrieval import Guidance, Retriever

logger = logging.getLogger(__name__)

MAX_REWRITES = 2
TOP_K = 3
WEAK_DIMENSIONS = 2


class RewriteOut(BaseModel):
    improved: str
    changes: list[str]


class Steps(Protocol):
    async def score(self, prompt: str, task: TaskType) -> list[Dimension]: ...

    async def rewrite(
        self,
        prompt: str,
        task: TaskType,
        dimensions: list[Dimension],
        guidance: list[Guidance],
        retry: bool,
    ) -> RewriteOut: ...


class CoachState(TypedDict, total=False):
    prompt: str
    task: TaskType
    dimensions: list[Dimension]
    original_overall: float
    guidance: list[Guidance]
    improved: str
    changes: list[str]
    new_overall: float
    attempts: int
    best_overall: float
    best_improved: str
    best_changes: list[str]


def overall(dimensions: list[Dimension]) -> float:
    return sum(d.score for d in dimensions) / len(dimensions)


def build_query(prompt: str, dimensions: list[Dimension]) -> str:
    weakest = sorted(dimensions, key=lambda d: d.score)[:WEAK_DIMENSIONS]
    lines = [f"{d.name}: {d.feedback}" for d in weakest]
    return "\n".join(lines) + "\n\n" + prompt[:300]


def route_after_verify(state: CoachState) -> Literal["rewrite", "done"]:
    if state["new_overall"] > state["original_overall"]:
        return "done"
    if state["attempts"] >= MAX_REWRITES:
        return "done"
    return "rewrite"


def build_graph(steps: Steps, retriever: Retriever) -> Any:
    async def analyze(state: CoachState) -> dict[str, Any]:
        dimensions = await steps.score(state["prompt"], state["task"])
        return {
            "dimensions": dimensions,
            "original_overall": overall(dimensions),
            "attempts": 0,
            "best_overall": -1.0,
        }

    async def retrieve(state: CoachState) -> dict[str, Any]:
        query = build_query(state["prompt"], state["dimensions"])
        try:
            guidance = await retriever.search(query, TOP_K)
        except Exception:
            logger.warning("retrieval failed; continuing without guidance", exc_info=True)
            guidance = []
        return {"guidance": guidance}

    async def rewrite(state: CoachState) -> dict[str, Any]:
        attempts = state["attempts"]
        out = await steps.rewrite(
            state["prompt"],
            state["task"],
            state["dimensions"],
            state.get("guidance", []),
            retry=attempts > 0,
        )
        return {"improved": out.improved, "changes": out.changes, "attempts": attempts + 1}

    async def verify(state: CoachState) -> dict[str, Any]:
        scored = await steps.score(state["improved"], state["task"])
        new_overall = overall(scored)
        update: dict[str, Any] = {"new_overall": new_overall}
        if new_overall > state["best_overall"]:
            update["best_overall"] = new_overall
            update["best_improved"] = state["improved"]
            update["best_changes"] = state["changes"]
        return update

    graph = StateGraph(CoachState)
    graph.add_node("analyze", analyze)
    graph.add_node("retrieve", retrieve)
    graph.add_node("rewrite", rewrite)
    graph.add_node("verify", verify)
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "retrieve")
    graph.add_edge("retrieve", "rewrite")
    graph.add_edge("rewrite", "verify")
    graph.add_conditional_edges("verify", route_after_verify, {"rewrite": "rewrite", "done": END})
    return graph.compile()
