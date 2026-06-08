from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Delphi API"
    api_prefix: str = "/api"
