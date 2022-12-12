import functools

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ "Class containing project settings."""

    deta_project_key: str

    class Config:
        env_file = ".env"


@functools.cache
def get_settings() -> Settings:
    return Settings()
