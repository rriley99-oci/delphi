from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import DatasetModel
from app.schemas.datasets import DatasetCreate


class DatasetAlreadyExistsError(Exception):
    pass


def create_dataset(db: Session, dataset_create: DatasetCreate) -> DatasetModel:
    dataset = DatasetModel(**dataset_create.model_dump())
    db.add(dataset)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DatasetAlreadyExistsError from exc

    db.refresh(dataset)
    return dataset


def list_datasets(db: Session) -> list[DatasetModel]:
    result = db.execute(
        select(DatasetModel).order_by(DatasetModel.created_at, DatasetModel.id)
    )
    return list(result.scalars())


def get_dataset(db: Session, dataset_id: UUID) -> DatasetModel | None:
    return db.get(DatasetModel, dataset_id)
