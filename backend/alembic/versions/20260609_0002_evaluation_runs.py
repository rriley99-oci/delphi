"""Add evaluation run persistence.

Revision ID: 20260609_0002
Revises: 20260609_0001
Create Date: 2026-06-09 14:10:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260609_0002"
down_revision: str | Sequence[str] | None = "20260609_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "datasets",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("database_name", sa.String(length=255), nullable=False),
        sa.Column("schema_name", sa.String(length=255), nullable=False),
        sa.Column("table_name", sa.String(length=255), nullable=False),
        sa.Column("owner", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "database_name",
            "schema_name",
            "table_name",
            name="uq_datasets_identity",
        ),
    )
    op.create_table(
        "contracts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("dataset_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("current_version_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contract_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("contract_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=False),
        sa.Column("previous_version_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["contract_id"], ["contracts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["previous_version_id"],
            ["contract_versions.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "contract_id",
            "version_number",
            name="uq_contract_versions_number",
        ),
    )
    op.create_index(
        op.f("ix_contract_versions_contract_id"),
        "contract_versions",
        ["contract_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_contracts_current_version_id_contract_versions",
        "contracts",
        "contract_versions",
        ["current_version_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(op.f("ix_contracts_dataset_id"), "contracts", ["dataset_id"], unique=False)
    op.create_table(
        "contract_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("contract_version_id", sa.Uuid(), nullable=False),
        sa.Column("rule_type", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["contract_version_id"],
            ["contract_versions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_contract_rules_contract_version_id"),
        "contract_rules",
        ["contract_version_id"],
        unique=False,
    )
    op.create_table(
        "evaluation_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("dataset_id", sa.Uuid(), nullable=False),
        sa.Column("contract_version_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("summary_status", sa.String(length=32), nullable=False),
        sa.Column("total_rules", sa.Integer(), nullable=False),
        sa.Column("passed_rules", sa.Integer(), nullable=False),
        sa.Column("failed_rules", sa.Integer(), nullable=False),
        sa.Column(
            "triggered_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["contract_version_id"],
            ["contract_versions.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_evaluation_runs_contract_version_id"),
        "evaluation_runs",
        ["contract_version_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_runs_dataset_id"),
        "evaluation_runs",
        ["dataset_id"],
        unique=False,
    )
    op.create_table(
        "evaluation_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("evaluation_run_id", sa.Uuid(), nullable=False),
        sa.Column("rule_id", sa.Uuid(), nullable=False),
        sa.Column("rule_type", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["evaluation_run_id"],
            ["evaluation_runs.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(["rule_id"], ["contract_rules.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_evaluation_results_evaluation_run_id"),
        "evaluation_results",
        ["evaluation_run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_rule_id"),
        "evaluation_results",
        ["rule_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_evaluation_results_rule_id"), table_name="evaluation_results")
    op.drop_index(
        op.f("ix_evaluation_results_evaluation_run_id"),
        table_name="evaluation_results",
    )
    op.drop_table("evaluation_results")
    op.drop_index(op.f("ix_evaluation_runs_dataset_id"), table_name="evaluation_runs")
    op.drop_index(
        op.f("ix_evaluation_runs_contract_version_id"),
        table_name="evaluation_runs",
    )
    op.drop_table("evaluation_runs")
    op.drop_index(op.f("ix_contract_rules_contract_version_id"), table_name="contract_rules")
    op.drop_table("contract_rules")
    op.drop_index(op.f("ix_contracts_dataset_id"), table_name="contracts")
    op.drop_constraint(
        "fk_contracts_current_version_id_contract_versions",
        "contracts",
        type_="foreignkey",
    )
    op.drop_index(op.f("ix_contract_versions_contract_id"), table_name="contract_versions")
    op.drop_table("contract_versions")
    op.drop_table("contracts")
    op.drop_table("datasets")
