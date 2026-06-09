from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

ViolationStatus = Literal["open", "acknowledged", "resolved"]
ViolationSeverity = Literal["low", "medium", "high", "critical"]


class ViolationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dataset_id: UUID
    contract_id: UUID | None
    contract_version_id: UUID | None
    rule_id: UUID
    evaluation_run_id: UUID | None
    evaluation_result_id: UUID | None
    rule_type: str
    severity: ViolationSeverity
    status: ViolationStatus
    message: str
    evidence: dict[str, Any]
    first_seen_at: datetime
    last_seen_at: datetime
    acknowledged_at: datetime | None
    resolved_at: datetime | None
    resolution_note: str | None
    created_at: datetime
    updated_at: datetime


class ViolationListResponse(BaseModel):
    items: list[ViolationRead]


class ViolationUpdate(BaseModel):
    status: Literal["acknowledged", "resolved"]
    resolution_note: str | None = Field(default=None, max_length=2000)
