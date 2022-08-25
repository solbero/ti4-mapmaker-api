from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """ "Class containing project settings."""

    deta_project_key: str
    deta_project_id: str
    deta_base_document_maps: str = "maps"
    deta_base_document_tiles: str = "tiles"
    deta_base_document_factions: str = "factions"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@cache
def get_settings() -> Settings:
    return Settings()
