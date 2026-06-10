"""Add violation lifecycle persistence.

Revision ID: 20260609_0005
Revises: 20260609_0004
Create Date: 2026-06-09 14:20:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "20260609_0005"
down_revision: str | Sequence[str] | None = "20260609_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "violations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("dataset_id", sa.Uuid(), nullable=False),
        sa.Column("contract_id", sa.Uuid(), nullable=True),
        sa.Column("contract_version_id", sa.Uuid(), nullable=True),
        sa.Column("rule_id", sa.Uuid(), nullable=False),
        sa.Column("evaluation_run_id", sa.Uuid(), nullable=True),
        sa.Column("evaluation_result_id", sa.Uuid(), nullable=True),
        sa.Column("rule_type", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column(
            "evidence",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "first_seen_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolution_note", sa.Text(), nullable=True),
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
        sa.CheckConstraint(
            "severity in ('low', 'medium', 'high', 'critical')",
            name="ck_violations_severity",
        ),
        sa.CheckConstraint(
            "status in ('open', 'acknowledged', 'resolved')",
            name="ck_violations_status",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_violations_contract_id", "violations", ["contract_id"])
    op.create_index(
        "ix_violations_contract_version_id",
        "violations",
        ["contract_version_id"],
    )
    op.create_index("ix_violations_dataset_id", "violations", ["dataset_id"])
    op.create_index(
        "ix_violations_evaluation_result_id",
        "violations",
        ["evaluation_result_id"],
    )
    op.create_index(
        "ix_violations_evaluation_run_id",
        "violations",
        ["evaluation_run_id"],
    )
    op.create_index("ix_violations_rule_id", "violations", ["rule_id"])
    op.create_index(
        "uq_violations_unresolved_rule",
        "violations",
        ["dataset_id", "rule_id"],
        unique=True,
        postgresql_where=sa.text("status in ('open', 'acknowledged')"),
    )


def downgrade() -> None:
    op.drop_index("uq_violations_unresolved_rule", table_name="violations")
    op.drop_index("ix_violations_rule_id", table_name="violations")
    op.drop_index("ix_violations_evaluation_run_id", table_name="violations")
    op.drop_index("ix_violations_evaluation_result_id", table_name="violations")
    op.drop_index("ix_violations_dataset_id", table_name="violations")
    op.drop_index("ix_violations_contract_version_id", table_name="violations")
    op.drop_index("ix_violations_contract_id", table_name="violations")
    op.drop_table("violations")
