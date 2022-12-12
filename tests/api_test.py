import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from scripts import faction_data, map_data, tile_data
from ti4_mapmaker_api import database, view


@pytest.fixture(scope="class")
async def maps_db(db: database.AsyncBase):
    maps = [map.dict() for map in map_data.parsed()]
    await db.put_many(maps)
    yield
    await db.delete_all()


@pytest.fixture(scope="class")
async def factions_db(db: database.AsyncBase):
    factions = [faction.dict() for faction in faction_data.parsed()]
    await db.put_many(factions)
    yield
    await db.delete_all()


@pytest.fixture(scope="class")
async def tiles_db(db: database.AsyncBase):
    tiles = [tile.dict() for tile in tile_data.parsed()]
    await db.put_many(tiles)
    yield
    await db.delete_all()


@pytest.fixture(scope="class")
def document_override(app: FastAPI):
    app.dependency_overrides[view.get_maps_document] = lambda: "testing"
    yield
    app.dependency_overrides = {}


class TestRoot:
    def test_read_root(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200


@pytest.mark.slow
@pytest.mark.usefixtures("maps_db", "document_override")
class TestMapEndpoints:
    @pytest.mark.anyio
    async def test_read_maps(self, client: TestClient):
        response = client.get("/maps/")
        assert response.status_code == 200

    def test_read_maps_key(self, client: TestClient):
        response = client.get("/maps/6-normal")
        assert response.status_code == 200

    def test_read_maps_key_not_exist(self, client: TestClient):
        response = client.get("/maps/1-foo")
        assert response.status_code == 404


@pytest.mark.slow
@pytest.mark.usefixtures("factions_db", "document_override")
class TestFactionEndpoints:
    def test_read_factions(self, client: TestClient):
        response = client.get("/factions/")
        assert response.status_code == 200

    def test_read_factions_key(self, client: TestClient):
        response = client.get("/factions/arborec")
        assert response.status_code == 200

    def test_read_factions_key_not_exist(self, client: TestClient):
        response = client.get("/factions/foo")
        assert response.status_code == 422


@pytest.mark.slow
@pytest.mark.usefixtures("tiles_db", "document_override")
class TestTileEndpoints:
    def test_read_tiles(self, client: TestClient):
        response = client.get("/tiles/")
        assert response.status_code == 200

    def test_read_tiles_key(self, client: TestClient):
        response = client.get("/tiles/1")
        assert response.status_code == 200

    def test_read_tiles_key_not_exists(self, client: TestClient):
        response = client.get("/tiles/foo")
        assert response.status_code == 404
