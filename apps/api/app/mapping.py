from app.db.models import AnalysisRecord
from app.schemas import Analysis, Dimension, Technique


def to_analysis(record: AnalysisRecord) -> Analysis:
    return Analysis(
        id=str(record.id),
        created_at=record.created_at.isoformat(),
        original=record.original,
        improved=record.improved,
        overall=record.overall,
        dimensions=[Dimension(**d) for d in record.dimensions],
        changes=record.changes,
        techniques=[Technique(**t) for t in record.techniques],
    )
