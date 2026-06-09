from collections.abc import Generator
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models import ViolationModel
from app.db.session import get_db
from app.main import create_app
from app.schemas.violations import ViolationUpdate
from app.services.violations import (
    InvalidViolationTransitionError,
    update_violation,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
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
        engine.dispose()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def make_violation(
    db_session: Session,
    *,
    status: str = "open",
    dataset_id=None,
    rule_id=None,
) -> ViolationModel:
    violation = ViolationModel(
        dataset_id=dataset_id or uuid4(),
        rule_id=rule_id or uuid4(),
        rule_type="freshness",
        severity="critical",
        status=status,
        message="Freshness rule failed.",
        evidence={"expected_lag_minutes": 60, "observed_lag_minutes": 180},
    )
    db_session.add(violation)
    db_session.commit()
    db_session.refresh(violation)
    return violation


def test_list_violations_returns_persisted_records(
    client: TestClient,
    db_session: Session,
):
    violation = make_violation(db_session)

    response = client.get("/api/violations")

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == str(violation.id)
    assert body["items"][0]["status"] == "open"
    assert body["items"][0]["severity"] == "critical"
    assert body["items"][0]["evidence"]["observed_lag_minutes"] == 180


def test_list_violations_filters_by_status(
    client: TestClient,
    db_session: Session,
):
    open_violation = make_violation(db_session, status="open")
    make_violation(db_session, status="resolved")

    response = client.get("/api/violations", params={"status": "open"})

    assert response.status_code == 200
    items = response.json()["items"]
    assert [item["id"] for item in items] == [str(open_violation.id)]


def test_patch_acknowledges_open_violation(
    client: TestClient,
    db_session: Session,
):
    violation = make_violation(db_session)

    response = client.patch(
        f"/api/violations/{violation.id}",
        json={"status": "acknowledged"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "acknowledged"
    assert body["acknowledged_at"] is not None
    assert body["resolved_at"] is None


def test_patch_resolves_acknowledged_violation(
    client: TestClient,
    db_session: Session,
):
    violation = make_violation(db_session)
    update_violation(
        db_session,
        violation.id,
        ViolationUpdate(status="acknowledged"),
    )

    response = client.patch(
        f"/api/violations/{violation.id}",
        json={"status": "resolved", "resolution_note": "Source load caught up."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "resolved"
    assert body["resolved_at"] is not None
    assert body["resolution_note"] == "Source load caught up."


def test_service_rejects_acknowledging_resolved_violation(db_session: Session):
    violation = make_violation(db_session, status="resolved")

    with pytest.raises(InvalidViolationTransitionError):
        update_violation(
            db_session,
            violation.id,
            ViolationUpdate(status="acknowledged"),
        )


def test_migration_defines_unresolved_rule_unique_index():
    migration = Path(__file__).parents[1] / (
        "alembic/versions/20260609_0002_violations.py"
    )

    migration_text = migration.read_text()

    assert "uq_violations_unresolved_rule" in migration_text
    assert "status in ('open', 'acknowledged')" in migration_text
