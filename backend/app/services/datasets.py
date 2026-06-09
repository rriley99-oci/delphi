from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.models import Dataset
from app.schemas.datasets import DatasetCreate


class DatasetAlreadyExistsError(Exception):
    pass


def create_dataset(db: Session, dataset_create: DatasetCreate) -> Dataset:
    dataset = Dataset(**dataset_create.model_dump())
    db.add(dataset)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DatasetAlreadyExistsError from exc

    db.refresh(dataset)
    return dataset


def list_datasets(db: Session) -> list[Dataset]:
    result = db.execute(select(Dataset).order_by(Dataset.created_at, Dataset.id))
    return list(result.scalars())


def get_dataset(db: Session, dataset_id: UUID) -> Dataset | None:
    return db.get(Dataset, dataset_id)
