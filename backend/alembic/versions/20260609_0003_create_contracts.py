"""Create contract tables.

Revision ID: 20260609_0003
Revises: 20260609_0002
Create Date: 2026-06-09 14:10:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260609_0003"
down_revision: str | Sequence[str] | None = "20260609_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "contracts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("current_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["datasets.id"],
            name="fk_contracts_dataset_id_datasets",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_contracts"),
    )
    op.create_index("ix_contracts_dataset_id", "contracts", ["dataset_id"])

    op.create_table(
        "contract_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("contract_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=False),
        sa.Column("previous_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["contract_id"],
            ["contracts.id"],
            name="fk_contract_versions_contract_id_contracts",
        ),
        sa.ForeignKeyConstraint(
            ["previous_version_id"],
            ["contract_versions.id"],
            name="fk_contract_versions_previous_version_id_contract_versions",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_contract_versions"),
        sa.UniqueConstraint(
            "contract_id",
            "version_number",
            name="uq_contract_versions_contract_id_version_number",
        ),
    )
    op.create_index(
        "ix_contract_versions_contract_id",
        "contract_versions",
        ["contract_id"],
    )

    op.create_table(
        "contract_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("contract_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rule_type", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["contract_version_id"],
            ["contract_versions.id"],
            name="fk_contract_rules_contract_version_id_contract_versions",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_contract_rules"),
    )
    op.create_index(
        "ix_contract_rules_contract_version_id",
        "contract_rules",
        ["contract_version_id"],
    )

    op.create_foreign_key(
        "fk_contracts_current_version_id_contract_versions",
        "contracts",
        "contract_versions",
        ["current_version_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_contracts_current_version_id_contract_versions",
        "contracts",
        type_="foreignkey",
    )
    op.drop_index("ix_contract_rules_contract_version_id", table_name="contract_rules")
    op.drop_table("contract_rules")
    op.drop_index("ix_contract_versions_contract_id", table_name="contract_versions")
    op.drop_table("contract_versions")
    op.drop_index("ix_contracts_dataset_id", table_name="contracts")
    op.drop_table("contracts")
