from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import ContractModel, ContractRuleModel, ContractVersionModel, DatasetModel
from app.schemas.contracts import ContractCreate


class DatasetNotFoundError(Exception):
    pass


def create_contract(db: Session, contract_create: ContractCreate) -> ContractModel:
    dataset = db.get(DatasetModel, contract_create.dataset_id)
    if dataset is None:
        raise DatasetNotFoundError

    contract = ContractModel(
        dataset_id=contract_create.dataset_id,
        name=contract_create.name,
    )
    db.add(contract)
    db.flush()

    version = ContractVersionModel(
        contract_id=contract.id,
        version_number=1,
        change_reason=contract_create.change_reason,
        rules=[
            ContractRuleModel(
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


def list_contracts(db: Session) -> list[ContractModel]:
    result = db.execute(
        select(ContractModel)
        .options(
            selectinload(ContractModel.current_version).selectinload(
                ContractVersionModel.rules,
            ),
        )
        .order_by(ContractModel.created_at, ContractModel.id),
    )
    return list(result.scalars())


def get_contract(db: Session, contract_id: UUID) -> ContractModel | None:
    result = db.execute(
        select(ContractModel)
        .where(ContractModel.id == contract_id)
        .options(
            selectinload(ContractModel.current_version).selectinload(
                ContractVersionModel.rules,
            ),
        ),
    )
    return result.scalar_one_or_none()
