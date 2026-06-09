from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

RuleType = Literal["freshness", "row_count", "custom_sql"]
RuleSeverity = Literal["info", "warning", "critical"]


class ContractRuleCreate(BaseModel):
    rule_type: RuleType
    severity: RuleSeverity
    name: str | None = Field(default=None, max_length=255)
    config: dict[str, Any]

    @field_validator("name")
    @classmethod
    def strip_optional_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped

    @model_validator(mode="after")
    def validate_rule_config(self) -> "ContractRuleCreate":
        required_keys = {
            "freshness": {"timestamp_column", "max_lag_minutes"},
            "row_count": {"min_count", "max_count"},
            "custom_sql": {"sql"},
        }[self.rule_type]
        missing = required_keys.difference(self.config)
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"{self.rule_type} config missing: {missing_list}")
        return self


class ContractCreate(BaseModel):
    dataset_id: UUID
    name: str = Field(min_length=1, max_length=255)
    change_reason: str = Field(min_length=1, max_length=1000)
    rules: list[ContractRuleCreate] = Field(min_length=1)

    @field_validator("name", "change_reason")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class ContractRuleRead(BaseModel):
    id: UUID
    rule_type: str
    severity: str
    name: str | None
    config: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContractVersionRead(BaseModel):
    id: UUID
    contract_id: UUID
    version_number: int
    change_reason: str
    previous_version_id: UUID | None
    created_at: datetime
    rules: list[ContractRuleRead]

    model_config = ConfigDict(from_attributes=True)


class ContractRead(BaseModel):
    id: UUID
    dataset_id: UUID
    name: str
    status: str
    current_version_id: UUID | None
    created_at: datetime
    updated_at: datetime
    current_version: ContractVersionRead | None

    model_config = ConfigDict(from_attributes=True)


class ContractList(BaseModel):
    items: list[ContractRead]
