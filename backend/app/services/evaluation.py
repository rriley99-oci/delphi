from dataclasses import dataclass
from typing import Protocol

from app.domain.models import ContractRule


@dataclass
class EvaluationContext:
    dataset_id: str
    contract_version_id: str


@dataclass
class RuleOutcome:
    status: str
    message: str
    evidence: dict


class RuleExecutor(Protocol):
    rule_type: str

    async def evaluate(self, context: EvaluationContext, rule: ContractRule) -> RuleOutcome:
        ...
