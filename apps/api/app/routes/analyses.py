import uuid

from fastapi import APIRouter, HTTPException

from app.db import repository
from app.db.session import SessionDep
from app.mapping import to_analysis
from app.schemas import Analysis

router = APIRouter()


@router.get("/analyses", response_model=list[Analysis])
async def list_analyses(session: SessionDep) -> list[Analysis]:
    records = await repository.list_recent(session)
    return [to_analysis(r) for r in records]


@router.get("/analyses/{analysis_id}", response_model=Analysis)
async def get_analysis(analysis_id: uuid.UUID, session: SessionDep) -> Analysis:
    record = await repository.get(session, analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return to_analysis(record)
