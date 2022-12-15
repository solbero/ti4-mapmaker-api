from collections.abc import AsyncGenerator

import pytest
from deta import Deta
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ti4_mapmaker_api import application, config, database


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def settings() -> config.Settings:
    return config.get_settings()


@pytest.fixture(scope="session")
def project_key(settings: config.Settings) -> str:
    return settings.DETA_PROJECT_KEY


@pytest.fixture(scope="session")
def engine(project_key: str) -> Deta:
    return Deta(project_key)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return application.create()


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def document() -> str:
    return "testing"


@pytest.fixture(scope="session")
async def db(engine, document) -> AsyncGenerator[database.AsyncBase, None]:
    db = database.AsyncBase(engine, document)
    yield database.AsyncBase(engine, document)
    await db.close()
