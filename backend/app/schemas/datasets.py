from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DatasetCreate(BaseModel):
    database_name: str = Field(min_length=1, max_length=255)
    schema_name: str = Field(min_length=1, max_length=255)
    table_name: str = Field(min_length=1, max_length=255)
    owner: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator(
        "database_name", "schema_name", "table_name", "owner", "description"
    )
    @classmethod
    def strip_blank_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class DatasetRead(BaseModel):
    id: UUID
    database_name: str
    schema_name: str
    table_name: str
    owner: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetList(BaseModel):
    items: list[DatasetRead]
