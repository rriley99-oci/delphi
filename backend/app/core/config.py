from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(
        default="Delphi API",
        validation_alias=AliasChoices("DELPHI_APP_NAME", "APP_NAME"),
    )
    api_prefix: str = Field(
        default="/api",
        validation_alias=AliasChoices("DELPHI_API_PREFIX", "API_PREFIX"),
    )
    database_url: str = Field(
        default="postgresql+psycopg://delphi:delphi@localhost:5432/delphi",
        validation_alias=AliasChoices("DELPHI_DATABASE_URL", "DATABASE_URL"),
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
