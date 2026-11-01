from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter

from app.schemas import Analysis, AnalyzeRequest, Dimension

router = APIRouter()


@router.post("/analyze", response_model=Analysis)
def analyze(req: AnalyzeRequest) -> Analysis:
    dimensions = [
        Dimension(name="clarity", score=6, feedback="The goal is understandable but vague."),
        Dimension(name="context", score=3, feedback="No background on audience or purpose."),
        Dimension(name="constraints", score=4, feedback="No limits on length, tone, or scope."),
        Dimension(name="format", score=2, feedback="The desired output format is not stated."),
        Dimension(name="examples", score=1, feedback="No example of a good answer."),
    ]
    overall = sum(d.score for d in dimensions) / len(dimensions)

    return Analysis(
        id=str(uuid4()),
        created_at=datetime.now(UTC).isoformat(),
        original=req.prompt,
        improved=(
            f"You are helping with a {req.task} task.\n\n"
            f"Task: {req.prompt}\n\n"
            "Audience and purpose: [describe who this is for and why]\n"
            "Constraints: [length, tone, scope]\n"
            "Output format: [bullets, table, JSON, etc.]\n"
            "Example of a good answer: [paste one]"
        ),
        overall=overall,
        dimensions=dimensions,
        changes=[
            "Added a role and a task type",
            "Added placeholders for audience, constraints, and format",
            "Added a slot for an example answer",
        ],
    )
