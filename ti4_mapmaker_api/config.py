from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ "Class containing project settings."""

    deta_project_key: str
    deta_project_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@cache
def get_settings() -> Settings:
    return Settings()
