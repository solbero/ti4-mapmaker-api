from fastapi.testclient import TestClient

from ti4_mapmaker_api import application

app = application.create()
client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_read_maps():
    response = client.get("/maps/")
    assert response.status_code == 200


def test_read_maps_key():
    response = client.get("/maps/6-normal")
    assert response.status_code == 200


def test_read_maps_key_not_exist():
    response = client.get("/maps/1-foo")
    assert response.status_code == 404


def test_read_factions():
    response = client.get("/factions/")
    assert response.status_code == 200


def test_read_factions_key():
    response = client.get("/factions/arborec")
    assert response.status_code == 200


def test_read_factions_key_not_exist():
    response = client.get("/factions/foo")
    assert response.status_code == 422


def test_read_tiles():
    response = client.get("/tiles/")
    assert response.status_code == 200


def test_read_tiles_key():
    response = client.get("/tiles/1")
    assert response.status_code == 200


def test_read_tiles_key_not_exists():
    response = client.get("/tiles/foo")
    assert response.status_code == 404
