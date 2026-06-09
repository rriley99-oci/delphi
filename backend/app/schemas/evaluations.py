from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

EvaluationRunStatus = Literal["queued", "running", "completed", "failed"]
EvaluationSummaryStatus = Literal["healthy", "unhealthy", "unknown"]
EvaluationResultStatus = Literal["pass", "fail", "error"]


class EvaluationTriggerRequest(BaseModel):
    dataset_id: UUID


class EvaluationResultRead(BaseModel):
    id: UUID
    rule_id: UUID
    rule_type: str
    severity: str
    status: EvaluationResultStatus
    message: str
    evidence: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EvaluationRunRead(BaseModel):
    id: UUID
    dataset_id: UUID
    contract_version_id: UUID
    status: EvaluationRunStatus
    summary_status: EvaluationSummaryStatus
    total_rules: int
    passed_rules: int
    failed_rules: int
    triggered_at: datetime
    completed_at: datetime | None
    results: list[EvaluationResultRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
