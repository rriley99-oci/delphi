import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.schemas.datasets import DatasetCreate
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
        get_settings.cache_clear()


def test_debug_sql_select_returns_rows(client, db_session):
    create_dataset(
        db_session,
        DatasetCreate(
            database_name="warehouse",
            schema_name="analytics",
            table_name="orders",
        ),
    )

    response = client.post(
        "/api/debug/sql",
        json={"query": "select database_name, schema_name, table_name from datasets"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["committed"] is True
    assert payload["row_count"] == 1
    assert payload["columns"] == ["database_name", "schema_name", "table_name"]
    assert payload["rows"][0] == {
        "database_name": "warehouse",
        "schema_name": "analytics",
        "table_name": "orders",
    }


def test_debug_sql_insert_can_mutate_database(client):
    response = client.post(
        "/api/debug/sql",
        json={
            "query": """
            insert into datasets
                (id, database_name, schema_name, table_name, created_at, updated_at)
            values
                ('00000000-0000-0000-0000-000000000001', 'warehouse', 'finance', 'invoices', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """
        },
    )

    assert response.status_code == 200
    assert response.json()["row_count"] == 1

    select_response = client.post(
        "/api/debug/sql",
        json={"query": "select table_name from datasets where schema_name = 'finance'"},
    )

    assert select_response.status_code == 200
    assert select_response.json()["rows"] == [{"table_name": "invoices"}]


def test_debug_sql_returns_bad_request_for_invalid_sql(client):
    response = client.post("/api/debug/sql", json={"query": "select * from missing_table"})

    assert response.status_code == 400


def test_debug_sql_returns_forbidden_when_disabled(client):
    get_settings.cache_clear()
    client.app.dependency_overrides[get_settings] = lambda: type(
        "SettingsOverride",
        (),
        {"debug_sql_enabled": False},
    )()

    response = client.post("/api/debug/sql", json={"query": "select 1"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Debug SQL endpoint is disabled."
