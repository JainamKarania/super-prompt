from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.db import repository
from app.db.session import SessionDep
from app.mapping import to_analysis
from app.schemas import Analysis, AnalyzeRequest
from app.services.coach import Coach, CoachError, CoachRateLimited, get_coach
from app.services.ratelimit import rate_limit

router = APIRouter()

CoachDep = Annotated[Coach, Depends(get_coach)]


@router.post("/analyze", response_model=Analysis, dependencies=[Depends(rate_limit)])
async def analyze(req: AnalyzeRequest, session: SessionDep, coach: CoachDep) -> Analysis:
    try:
        out = await coach.coach(req.prompt, req.task)
    except CoachRateLimited as exc:
        raise HTTPException(429, "The model is rate limited. Try again in a minute.") from exc
    except CoachError as exc:
        raise HTTPException(502, "The coaching model failed. Please try again.") from exc

    overall = sum(d.score for d in out.dimensions) / len(out.dimensions)
    record = await repository.create(
        session,
        original=req.prompt,
        improved=out.improved,
        task=req.task,
        overall=overall,
        dimensions=[d.model_dump() for d in out.dimensions],
        changes=out.changes,
        techniques=[t.model_dump() for t in out.techniques],
    )
    return to_analysis(record)
