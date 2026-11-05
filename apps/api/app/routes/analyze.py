from fastapi import APIRouter

from app.db import repository
from app.db.session import SessionDep
from app.mapping import to_analysis
from app.schemas import Analysis, AnalyzeRequest, Dimension

router = APIRouter()


@router.post("/analyze", response_model=Analysis)
async def analyze(req: AnalyzeRequest, session: SessionDep) -> Analysis:
    dimensions = [
        Dimension(name="clarity", score=6, feedback="The goal is understandable but vague."),
        Dimension(name="context", score=3, feedback="No background on audience or purpose."),
        Dimension(name="constraints", score=4, feedback="No limits on length, tone, or scope."),
        Dimension(name="format", score=2, feedback="The desired output format is not stated."),
        Dimension(name="examples", score=1, feedback="No example of a good answer."),
    ]
    overall = sum(d.score for d in dimensions) / len(dimensions)

    record = await repository.create(
        session,
        original=req.prompt,
        improved=(
            f"You are helping with a {req.task} task.\n\n"
            f"Task: {req.prompt}\n\n"
            "Audience and purpose: [describe who this is for and why]\n"
            "Constraints: [length, tone, scope]\n"
            "Output format: [bullets, table, JSON, etc.]\n"
            "Example of a good answer: [paste one]"
        ),
        task=req.task,
        overall=overall,
        dimensions=[d.model_dump() for d in dimensions],
        changes=[
            "Added a role and a task type",
            "Added placeholders for audience, constraints, and format",
            "Added a slot for an example answer",
        ],
    )
    return to_analysis(record)
