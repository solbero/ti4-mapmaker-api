from functools import cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """ "Class containing project settings."""

    deta_project_key: str = Field(env="DETA_PROJECT_KEY")
    deta_project_id: str = Field(env="DETA_PROJECT_ID")

    class Config:
        env_file = ".env"


@cache
def get_settings() -> Settings:
    return Settings()
