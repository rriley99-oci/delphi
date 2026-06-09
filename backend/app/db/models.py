from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, TypeDecorator, Uuid

from app.db.base import Base
from app.domain.models import Contract, ContractRule, ContractVersion, Dataset


class JSONBWithFallback(TypeDecorator[dict[str, Any]]):
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB)
        return dialect.type_descriptor(JSON)


DatasetModel = Dataset
ContractModel = Contract
ContractVersionModel = ContractVersion
ContractRuleModel = ContractRule


class EvaluationRunModel(Base):
    __tablename__ = "evaluation_runs"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    dataset_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    contract_version_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("contract_versions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    summary_status: Mapped[str] = mapped_column(String(32), nullable=False)
    total_rules: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passed_rules: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failed_rules: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    dataset: Mapped[Dataset] = relationship(back_populates="evaluations")
    contract_version: Mapped[ContractVersion] = relationship(
        back_populates="evaluations"
    )
    results: Mapped[list[EvaluationResultModel]] = relationship(
        back_populates="evaluation_run",
        cascade="all, delete-orphan",
    )


class EvaluationResultModel(Base):
    __tablename__ = "evaluation_results"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    evaluation_run_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("evaluation_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rule_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("contract_rules.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    rule_type: Mapped[str] = mapped_column(String(32), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    evaluation_run: Mapped[EvaluationRunModel] = relationship(back_populates="results")
    rule: Mapped[ContractRule] = relationship(back_populates="evaluation_results")


class ViolationModel(Base):
    __tablename__ = "violations"
    __table_args__ = (
        CheckConstraint(
            "status in ('open', 'acknowledged', 'resolved')",
            name="ck_violations_status",
        ),
        CheckConstraint(
            "severity in ('low', 'medium', 'high', 'critical')",
            name="ck_violations_severity",
        ),
        Index(
            "uq_violations_unresolved_rule",
            "dataset_id",
            "rule_id",
            unique=True,
            postgresql_where=text("status in ('open', 'acknowledged')"),
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    dataset_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    contract_id: Mapped[UUID | None] = mapped_column(Uuid, nullable=True, index=True)
    contract_version_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        nullable=True,
        index=True,
    )
    rule_id: Mapped[UUID] = mapped_column(Uuid, nullable=False, index=True)
    evaluation_run_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        nullable=True,
        index=True,
    )
    evaluation_result_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        nullable=True,
        index=True,
    )
    rule_type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="open")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict[str, Any]] = mapped_column(
        JSONBWithFallback,
        nullable=False,
        default=dict,
    )
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolution_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
