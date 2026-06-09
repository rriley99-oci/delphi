from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.violations import (
    ViolationListResponse,
    ViolationRead,
    ViolationStatus,
    ViolationUpdate,
)
from app.services.violations import (
    InvalidViolationTransitionError,
    ViolationNotFoundError,
)
from app.services.violations import (
    list_violations as list_violations_service,
)
from app.services.violations import (
    update_violation as update_violation_service,
)

router = APIRouter()


@router.get("", response_model=ViolationListResponse)
def list_violations(
    status_filter: ViolationStatus | None = Query(default=None, alias="status"),
    dataset_id: UUID | None = None,
    db: Session = Depends(get_db),
) -> ViolationListResponse:
    violations = list_violations_service(
        db,
        status=status_filter,
        dataset_id=dataset_id,
    )
    return ViolationListResponse(items=violations)


@router.patch("/{violation_id}", response_model=ViolationRead)
def update_violation(
    violation_id: UUID,
    update: ViolationUpdate,
    db: Session = Depends(get_db),
) -> ViolationRead:
    try:
        return update_violation_service(db, violation_id, update)
    except ViolationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidViolationTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
