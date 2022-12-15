import functools

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ "Class containing project settings."""

    DETA_PROJECT_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


@functools.cache
def get_settings() -> Settings:
    return Settings()
