from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.evaluations import EvaluationRunRead, EvaluationTriggerRequest
from app.services.evaluations import (
    EvaluationNotFoundError,
    EvaluationTriggerError,
)
from app.services.evaluations import (
    get_evaluation as get_evaluation_run,
)
from app.services.evaluations import (
    trigger_evaluation as trigger_evaluation_run,
)

router = APIRouter()


@router.post("", response_model=EvaluationRunRead, status_code=status.HTTP_201_CREATED)
async def trigger_evaluation(
    request: EvaluationTriggerRequest,
    db: Session = Depends(get_db),
) -> EvaluationRunRead:
    try:
        return trigger_evaluation_run(db, request.dataset_id)
    except EvaluationTriggerError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/{evaluation_id}", response_model=EvaluationRunRead)
async def get_evaluation(
    evaluation_id: UUID,
    db: Session = Depends(get_db),
) -> EvaluationRunRead:
    try:
        return get_evaluation_run(db, evaluation_id)
    except EvaluationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
