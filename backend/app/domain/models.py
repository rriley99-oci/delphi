from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Dataset:
    dataset_id: str
    database_name: str
    schema_name: str
    table_name: str
    created_at: datetime


@dataclass
class ContractRule:
    rule_id: str
    rule_type: str
    severity: str
    config: dict[str, Any]
