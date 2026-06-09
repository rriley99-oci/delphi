from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import (
    ContractModel,
    ContractRuleModel,
    ContractVersionModel,
    DatasetModel,
    EvaluationResultModel,
    EvaluationRunModel,
)


class EvaluationNotFoundError(ValueError):
    pass


class EvaluationTriggerError(ValueError):
    pass


@dataclass(frozen=True)
class NormalizedRuleOutcome:
    status: str
    message: str
    evidence: dict[str, Any]


def trigger_evaluation(db: Session, dataset_id: UUID) -> EvaluationRunModel:
    dataset = db.get(DatasetModel, dataset_id)
    if dataset is None:
        raise EvaluationTriggerError("dataset not found")

    contract = db.scalar(
        select(ContractModel)
        .where(ContractModel.dataset_id == dataset_id, ContractModel.status == "active")
        .options(selectinload(ContractModel.current_version))
    )
    if contract is None or contract.current_version_id is None:
        raise EvaluationTriggerError("dataset has no active contract version")

    contract_version = db.scalar(
        select(ContractVersionModel)
        .where(ContractVersionModel.id == contract.current_version_id)
        .options(selectinload(ContractVersionModel.rules))
    )
    if contract_version is None:
        raise EvaluationTriggerError("current contract version not found")

    outcomes = [
        _evaluate_rule(dataset=dataset, contract_version=contract_version, rule=rule)
        for rule in contract_version.rules
    ]
    failed_rules = sum(1 for outcome in outcomes if outcome.status != "pass")
    passed_rules = len(outcomes) - failed_rules
    completed_at = datetime.now(UTC)

    evaluation = EvaluationRunModel(
        dataset_id=dataset.id,
        contract_version_id=contract_version.id,
        status="completed",
        summary_status="unhealthy" if failed_rules else "healthy",
        total_rules=len(outcomes),
        passed_rules=passed_rules,
        failed_rules=failed_rules,
        completed_at=completed_at,
    )
    db.add(evaluation)
    db.flush()

    for rule, outcome in zip(contract_version.rules, outcomes, strict=True):
        db.add(
            EvaluationResultModel(
                evaluation_run_id=evaluation.id,
                rule_id=rule.id,
                rule_type=rule.rule_type,
                severity=rule.severity,
                status=outcome.status,
                message=outcome.message,
                evidence=outcome.evidence,
            )
        )

    db.commit()
    return get_evaluation(db, evaluation.id)


def get_evaluation(db: Session, evaluation_id: UUID) -> EvaluationRunModel:
    evaluation = db.scalar(
        select(EvaluationRunModel)
        .where(EvaluationRunModel.id == evaluation_id)
        .options(selectinload(EvaluationRunModel.results))
    )
    if evaluation is None:
        raise EvaluationNotFoundError("evaluation not found")
    return evaluation


def _evaluate_rule(
    *,
    dataset: DatasetModel,
    contract_version: ContractVersionModel,
    rule: ContractRuleModel,
) -> NormalizedRuleOutcome:
    return NormalizedRuleOutcome(
        status="pass",
        message="Rule recorded with placeholder executor.",
        evidence={
            "executor": "placeholder",
            "dataset": {
                "database_name": dataset.database_name,
                "schema_name": dataset.schema_name,
                "table_name": dataset.table_name,
            },
            "contract_version_id": str(contract_version.id),
            "rule_config": rule.config,
        },
    )
