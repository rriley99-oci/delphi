from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models import EvaluationResultModel, EvaluationRunModel


class Dataset(Base):
    __tablename__ = "datasets"
    __table_args__ = (
        UniqueConstraint(
            "database_name",
            "schema_name",
            "table_name",
            name="uq_datasets_identity",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    database_name: Mapped[str] = mapped_column(String(255), nullable=False)
    schema_name: Mapped[str] = mapped_column(String(255), nullable=False)
    table_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
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

    contracts: Mapped[list[Contract]] = relationship(
        back_populates="dataset",
        cascade="all, delete-orphan",
    )
    evaluations: Mapped[list[EvaluationRunModel]] = relationship(
        back_populates="dataset"
    )


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    dataset_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("datasets.id", name="fk_contracts_dataset_id_datasets"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    current_version_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey(
            "contract_versions.id",
            name="fk_contracts_current_version_id_contract_versions",
            use_alter=True,
        ),
        nullable=True,
    )
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

    dataset: Mapped[Dataset] = relationship(back_populates="contracts")
    versions: Mapped[list[ContractVersion]] = relationship(
        back_populates="contract",
        cascade="all, delete-orphan",
        foreign_keys="ContractVersion.contract_id",
    )
    current_version: Mapped[ContractVersion | None] = relationship(
        foreign_keys=[current_version_id],
        post_update=True,
    )


class ContractVersion(Base):
    __tablename__ = "contract_versions"
    __table_args__ = (
        UniqueConstraint(
            "contract_id",
            "version_number",
            name="uq_contract_versions_contract_id_version_number",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    contract_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("contracts.id", name="fk_contract_versions_contract_id_contracts"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    change_reason: Mapped[str] = mapped_column(Text, nullable=False)
    previous_version_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey(
            "contract_versions.id",
            name="fk_contract_versions_previous_version_id_contract_versions",
        ),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    contract: Mapped[Contract] = relationship(
        back_populates="versions",
        foreign_keys=[contract_id],
    )
    previous_version: Mapped[ContractVersion | None] = relationship(
        remote_side=[id],
        foreign_keys=[previous_version_id],
    )
    rules: Mapped[list[ContractRule]] = relationship(
        back_populates="version",
        cascade="all, delete-orphan",
    )
    evaluations: Mapped[list[EvaluationRunModel]] = relationship(
        back_populates="contract_version",
    )


class ContractRule(Base):
    __tablename__ = "contract_rules"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    contract_version_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey(
            "contract_versions.id",
            name="fk_contract_rules_contract_version_id_contract_versions",
        ),
        nullable=False,
        index=True,
    )
    rule_type: Mapped[str] = mapped_column(String(32), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    version: Mapped[ContractVersion] = relationship(back_populates="rules")
    evaluation_results: Mapped[list[EvaluationResultModel]] = relationship(
        back_populates="rule",
    )
