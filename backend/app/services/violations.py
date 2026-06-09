from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db.models import ViolationModel
from app.schemas.violations import ViolationUpdate


class ViolationNotFoundError(ValueError):
    pass


class InvalidViolationTransitionError(ValueError):
    pass


def list_violations(
    db: Session,
    *,
    status: str | None = None,
    dataset_id: UUID | None = None,
) -> list[ViolationModel]:
    statement: Select[tuple[ViolationModel]] = select(ViolationModel).order_by(
        ViolationModel.status.asc(),
        ViolationModel.last_seen_at.desc(),
    )
    if status is not None:
        statement = statement.where(ViolationModel.status == status)
    if dataset_id is not None:
        statement = statement.where(ViolationModel.dataset_id == dataset_id)
    return list(db.scalars(statement).all())


def get_violation(db: Session, violation_id: UUID) -> ViolationModel:
    violation = db.get(ViolationModel, violation_id)
    if violation is None:
        raise ViolationNotFoundError(f"Violation {violation_id} was not found.")
    return violation


def update_violation(
    db: Session,
    violation_id: UUID,
    update: ViolationUpdate,
) -> ViolationModel:
    violation = get_violation(db, violation_id)
    now = datetime.now(UTC)

    if update.status == "acknowledged":
        if violation.status != "open":
            raise InvalidViolationTransitionError(
                "Only open violations can be acknowledged."
            )
        violation.status = "acknowledged"
        violation.acknowledged_at = now
    elif update.status == "resolved":
        if violation.status not in {"open", "acknowledged"}:
            raise InvalidViolationTransitionError(
                "Only open or acknowledged violations can be resolved."
            )
        violation.status = "resolved"
        violation.resolved_at = now
        violation.resolution_note = update.resolution_note

    db.add(violation)
    db.commit()
    db.refresh(violation)
    return violation
