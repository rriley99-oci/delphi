from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.models import Contract, ContractRule, ContractVersion, Dataset
from app.schemas.contracts import ContractCreate


class DatasetNotFoundError(Exception):
    pass


def create_contract(db: Session, contract_create: ContractCreate) -> Contract:
    dataset = db.get(Dataset, contract_create.dataset_id)
    if dataset is None:
        raise DatasetNotFoundError

    contract = Contract(
        dataset_id=contract_create.dataset_id,
        name=contract_create.name,
    )
    db.add(contract)
    db.flush()

    version = ContractVersion(
        contract_id=contract.id,
        version_number=1,
        change_reason=contract_create.change_reason,
        rules=[
            ContractRule(
                rule_type=rule.rule_type,
                severity=rule.severity,
                name=rule.name,
                config=rule.config,
            )
            for rule in contract_create.rules
        ],
    )
    db.add(version)
    db.flush()

    contract.current_version_id = version.id
    db.commit()

    return get_contract(db, contract.id) or contract


def list_contracts(db: Session) -> list[Contract]:
    result = db.execute(
        select(Contract)
        .options(
            selectinload(Contract.current_version).selectinload(
                ContractVersion.rules,
            ),
        )
        .order_by(Contract.created_at, Contract.id),
    )
    return list(result.scalars())


def get_contract(db: Session, contract_id: UUID) -> Contract | None:
    result = db.execute(
        select(Contract)
        .where(Contract.id == contract_id)
        .options(
            selectinload(Contract.current_version).selectinload(
                ContractVersion.rules,
            ),
        ),
    )
    return result.scalar_one_or_none()
