from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.contracts import ContractCreate, ContractList, ContractRead
from app.services.contracts import (
    DatasetNotFoundError,
    create_contract,
    get_contract,
    list_contracts,
)

router = APIRouter()


@router.post("", response_model=ContractRead, status_code=status.HTTP_201_CREATED)
async def register_contract(
    contract_create: ContractCreate,
    db: Session = Depends(get_db),
) -> ContractRead:
    try:
        return create_contract(db, contract_create)
    except DatasetNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found.",
        ) from exc


@router.get("", response_model=ContractList)
async def read_contracts(db: Session = Depends(get_db)) -> ContractList:
    return ContractList(items=list_contracts(db))


@router.get("/{contract_id}", response_model=ContractRead)
async def read_contract(
    contract_id: UUID,
    db: Session = Depends(get_db),
) -> ContractRead:
    contract = get_contract(db, contract_id)
    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found.",
        )
    return contract
