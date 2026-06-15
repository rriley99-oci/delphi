from typing import Any

from pydantic import BaseModel, Field


class DebugSQLRequest(BaseModel):
    query: str = Field(min_length=1)


class DebugSQLResponse(BaseModel):
    query: str
    row_count: int
    columns: list[str] = Field(default_factory=list)
    rows: list[dict[str, Any]] = Field(default_factory=list)
    committed: bool
