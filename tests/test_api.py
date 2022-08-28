import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from ti4_mapmaker_api import application, schema

app = application.create()
client = TestClient(app)


@pytest.fixture()
def anyio_backend():
    return "asyncio"


class TestRoot:
    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200


class TestMaps:
    def test_read_maps(self):
        response = client.get("/maps/")
        assert response.status_code == 200

    @pytest.mark.anyio()
    @pytest.mark.parametrize("players", [num for num in range(2, 9)])
    async def test_read_maps_valid_players(self, players: int):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/maps/", params={"players": players})
        assert len(response.json()) >= 1

    @pytest.mark.anyio()
    @pytest.mark.parametrize("style", [style for style in schema.Style])
    async def test_read_maps_valid_styles(self, style: str):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/maps/", params={"styles": style})
        assert len(response.json()) >= 1


class TestFactions:
    ...
