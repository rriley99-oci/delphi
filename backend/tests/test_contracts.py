import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.domain.models import Contract, ContractVersion
from app.main import create_app
from app.schemas.contracts import ContractCreate
from app.schemas.datasets import DatasetCreate
from app.services.contracts import (
    DatasetNotFoundError,
    create_contract,
    get_contract,
    list_contracts,
)
from app.services.datasets import create_dataset


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = session_factory()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def client(db_session):
    app = create_app()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def dataset(db_session):
    return create_dataset(
        db_session,
        DatasetCreate(
            database_name="warehouse",
            schema_name="analytics",
            table_name="orders",
        ),
    )


def contract_payload(dataset_id):
    return ContractCreate(
        dataset_id=dataset_id,
        name="Orders quality contract",
        change_reason="Initial contract definition",
        rules=[
            {
                "rule_type": "freshness",
                "severity": "critical",
                "name": "Orders arrive within one hour",
                "config": {
                    "timestamp_column": "updated_at",
                    "max_lag_minutes": 60,
                },
            },
            {
                "rule_type": "row_count",
                "severity": "warning",
                "config": {
                    "min_count": 1,
                    "max_count": 1000000,
                },
            },
            {
                "rule_type": "custom_sql",
                "severity": "info",
                "config": {
                    "sql": "select true as passed",
                },
            },
        ],
    )


def test_create_contract_persists_initial_version_and_rules(db_session, dataset):
    contract = create_contract(db_session, contract_payload(dataset.id))

    stored = get_contract(db_session, contract.id)

    assert stored is not None
    assert stored.dataset_id == dataset.id
    assert stored.current_version is not None
    assert stored.current_version.version_number == 1
    assert stored.current_version.change_reason == "Initial contract definition"
    assert stored.current_version_id == stored.current_version.id
    assert {rule.rule_type for rule in stored.current_version.rules} == {
        "freshness",
        "row_count",
        "custom_sql",
    }
    assert {rule.severity for rule in stored.current_version.rules} == {
        "critical",
        "warning",
        "info",
    }


def test_create_contract_requires_existing_dataset(db_session):
    payload = contract_payload("00000000-0000-0000-0000-000000000000")

    with pytest.raises(DatasetNotFoundError):
        create_contract(db_session, payload)


def test_list_contracts_returns_persisted_records(db_session, dataset):
    first = create_contract(db_session, contract_payload(dataset.id))
    second_payload = contract_payload(dataset.id)
    second_payload.name = "Second orders contract"
    second = create_contract(db_session, second_payload)

    contracts = list_contracts(db_session)

    assert {contract.id for contract in contracts} == {first.id, second.id}


def test_register_contract_api_persists_and_reads_contract(client, dataset):
    response = client.post(
        "/api/contracts",
        json=contract_payload(dataset.id).model_dump(mode="json"),
    )

    assert response.status_code == 201
    created = response.json()
    assert created["dataset_id"] == str(dataset.id)
    assert created["current_version"]["version_number"] == 1
    assert len(created["current_version"]["rules"]) == 3

    list_response = client.get("/api/contracts")
    assert list_response.status_code == 200
    assert list_response.json()["items"][0]["id"] == created["id"]

    get_response = client.get(f"/api/contracts/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


def test_register_contract_api_returns_not_found_for_unknown_dataset(client):
    response = client.post(
        "/api/contracts",
        json=contract_payload("00000000-0000-0000-0000-000000000000").model_dump(
            mode="json",
        ),
    )

    assert response.status_code == 404


def test_register_contract_api_validates_rule_config(client, dataset):
    payload = contract_payload(dataset.id).model_dump(mode="json")
    payload["rules"][0]["config"].pop("timestamp_column")

    response = client.post("/api/contracts", json=payload)

    assert response.status_code == 422


def test_contract_model_declares_version_constraints():
    contract_constraints = {constraint.name for constraint in Contract.__table__.constraints}
    version_constraints = {
        constraint.name for constraint in ContractVersion.__table__.constraints
    }

    assert "fk_contracts_dataset_id_datasets" in contract_constraints
    assert "uq_contract_versions_contract_id_version_number" in version_constraints
