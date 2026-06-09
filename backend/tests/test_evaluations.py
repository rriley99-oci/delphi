from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.db.models import (
    ContractModel,
    ContractRuleModel,
    ContractVersionModel,
    DatasetModel,
)
from app.services.evaluations import (
    EvaluationTriggerError,
    get_evaluation,
    trigger_evaluation,
)


@pytest.fixture()
def db() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def seed_contract(db: Session) -> DatasetModel:
    dataset = DatasetModel(
        database_name="warehouse",
        schema_name="public",
        table_name="orders",
    )
    db.add(dataset)
    db.flush()

    contract = ContractModel(
        dataset_id=dataset.id, name="Orders contract", status="active"
    )
    db.add(contract)
    db.flush()

    version = ContractVersionModel(
        contract_id=contract.id,
        version_number=1,
        change_reason="Initial expectations",
    )
    db.add(version)
    db.flush()
    contract.current_version_id = version.id

    db.add_all(
        [
            ContractRuleModel(
                contract_version_id=version.id,
                rule_type="freshness",
                severity="critical",
                config={"timestamp_column": "updated_at", "max_lag_minutes": 60},
            ),
            ContractRuleModel(
                contract_version_id=version.id,
                rule_type="row_count",
                severity="warning",
                config={"min_count": 1},
            ),
        ]
    )
    db.commit()
    return dataset


def test_trigger_evaluation_persists_run_and_rule_results(db: Session):
    dataset = seed_contract(db)

    evaluation = trigger_evaluation(db, dataset.id)

    assert evaluation.dataset_id == dataset.id
    assert evaluation.status == "completed"
    assert evaluation.summary_status == "healthy"
    assert evaluation.total_rules == 2
    assert evaluation.passed_rules == 2
    assert evaluation.failed_rules == 0
    assert len(evaluation.results) == 2
    assert {result.rule_type for result in evaluation.results} == {
        "freshness",
        "row_count",
    }
    assert all(
        result.evidence["executor"] == "placeholder" for result in evaluation.results
    )


def test_get_evaluation_returns_persisted_rule_results(db: Session):
    dataset = seed_contract(db)
    created = trigger_evaluation(db, dataset.id)

    fetched = get_evaluation(db, created.id)

    assert fetched.id == created.id
    assert len(fetched.results) == 2


def test_trigger_evaluation_requires_registered_dataset(db: Session):
    with pytest.raises(EvaluationTriggerError, match="dataset not found"):
        trigger_evaluation(db, uuid4())
