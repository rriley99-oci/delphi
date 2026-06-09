import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.domain.models import Dataset
from app.main import create_app
from app.schemas.datasets import DatasetCreate
from app.services.datasets import (
    DatasetAlreadyExistsError,
    create_dataset,
    get_dataset,
    list_datasets,
)


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


def test_create_dataset_persists_identity_fields(db_session):
    dataset = create_dataset(
        db_session,
        DatasetCreate(
            database_name="warehouse",
            schema_name="analytics",
            table_name="orders",
            owner="data-platform",
        ),
    )

    stored = get_dataset(db_session, dataset.id)

    assert stored is not None
    assert stored.database_name == "warehouse"
    assert stored.schema_name == "analytics"
    assert stored.table_name == "orders"
    assert stored.owner == "data-platform"


def test_create_dataset_rejects_duplicate_identity(db_session):
    payload = DatasetCreate(
        database_name="warehouse",
        schema_name="analytics",
        table_name="orders",
    )
    create_dataset(db_session, payload)

    with pytest.raises(DatasetAlreadyExistsError):
        create_dataset(db_session, payload)


def test_list_datasets_returns_persisted_records(db_session):
    first = create_dataset(
        db_session,
        DatasetCreate(
            database_name="warehouse",
            schema_name="analytics",
            table_name="orders",
        ),
    )
    second = create_dataset(
        db_session,
        DatasetCreate(
            database_name="warehouse",
            schema_name="finance",
            table_name="invoices",
        ),
    )

    datasets = list_datasets(db_session)

    assert {dataset.id for dataset in datasets} == {first.id, second.id}


def test_register_dataset_api_persists_and_reads_dataset(client):
    response = client.post(
        "/api/datasets",
        json={
            "database_name": "warehouse",
            "schema_name": "analytics",
            "table_name": "orders",
            "description": "Trusted order facts",
        },
    )

    assert response.status_code == 201
    created = response.json()
    assert created["database_name"] == "warehouse"
    assert created["schema_name"] == "analytics"
    assert created["table_name"] == "orders"
    assert created["description"] == "Trusted order facts"

    list_response = client.get("/api/datasets")
    assert list_response.status_code == 200
    assert list_response.json()["items"][0]["id"] == created["id"]

    get_response = client.get(f"/api/datasets/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]


def test_register_dataset_api_returns_conflict_for_duplicate_identity(client):
    payload = {
        "database_name": "warehouse",
        "schema_name": "analytics",
        "table_name": "orders",
    }
    assert client.post("/api/datasets", json=payload).status_code == 201

    response = client.post("/api/datasets", json=payload)

    assert response.status_code == 409


def test_get_dataset_api_returns_not_found_for_unknown_id(client):
    response = client.get("/api/datasets/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_dataset_model_declares_identity_unique_constraint():
    constraints = {constraint.name for constraint in Dataset.__table__.constraints}

    assert "uq_datasets_identity" in constraints
