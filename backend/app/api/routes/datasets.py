from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.datasets import DatasetCreate, DatasetList, DatasetRead
from app.services.datasets import (
    DatasetAlreadyExistsError,
    create_dataset,
    get_dataset,
    list_datasets,
)

router = APIRouter()


@router.post("", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
async def register_dataset(
    dataset_create: DatasetCreate,
    db: Session = Depends(get_db),
) -> DatasetRead:
    try:
        return create_dataset(db, dataset_create)
    except DatasetAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Dataset already exists for database.schema.table identity.",
        ) from exc


@router.get("", response_model=DatasetList)
async def read_datasets(db: Session = Depends(get_db)) -> DatasetList:
    return DatasetList(items=list_datasets(db))


@router.get("/{dataset_id}", response_model=DatasetRead)
async def read_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
) -> DatasetRead:
    dataset = get_dataset(db, dataset_id)
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found.",
        )
    return dataset
