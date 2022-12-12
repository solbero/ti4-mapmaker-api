import pytest

from scripts import faction_data, map_data, tile_data
from ti4_mapmaker_api import database


@pytest.fixture(scope="function")
async def teardown_db(db: database.AsyncBase):
    await db.delete_all()


@pytest.mark.slow
@pytest.mark.usefixtures("teardown_db")
class TestDatabase:
    @pytest.mark.anyio
    async def test_database_put(self, db: database.AsyncBase):
        record = {"key": "1", "foo": "bar"}
        response = await db.put(record)
        assert record == response

    @pytest.mark.anyio
    async def test_database_put_many(self, db: database.AsyncBase):
        records = [{"key": f"{num}", "foo": "bar"} for num in range(30)]
        response = await db.put_many(records)
        assert records == response["processed"]

    @pytest.mark.anyio
    async def test_database_get(self, db: database.AsyncBase):
        record = {"key": "1", "foo": "bar"}
        await db.put(record)
        response = await db.get("1")
        assert record == response

    @pytest.mark.anyio
    async def test_database_fetch_all(self, db: database.AsyncBase):
        records = [{"key": f"{num}", "foo": "bar"} for num in range(25)]
        await db.put_many(records)
        response = await db.fetch()
        assert all((key in records) for key in response)

    @pytest.mark.anyio
    async def test_database_fetch_one(self, db: database.AsyncBase):
        records = [{"key": f"{num}", "foo": "bar"} for num in range(25)]
        await db.put_many(records)
        record = [{"key": "1", "foo": "bar"}]
        response = await db.fetch(record)
        assert record == response

    @pytest.mark.anyio
    async def test_database_delete_one(self, db: database.AsyncBase):
        record = {"key": "1", "foo": "bar"}
        await db.put(record)
        await db.delete("1")
        response = await db.fetch()
        assert len(response) == 0

    @pytest.mark.anyio
    async def test_database_delete_all(self, db: database.AsyncBase):
        records = [{"key": f"{num}", "foo": "bar"} for num in range(25)]
        await db.put_many(records)
        await db.delete_all()
        response = await db.fetch()
        assert len(response) == 0


class TestParsing:
    def test_tile_data(self):
        tiles = tile_data.parsed()
        assert len(tiles) == 100

    def test_faction_data(self):
        factions = faction_data.parsed()
        assert len(factions) == 25

    def test_map_data(self):
        maps = map_data.parsed()
        assert len(maps) == 25


class TestQuery:
    def test_query_with_two_parameters_and_one_list(self):
        params = {
            "numbers": [1, 2],
            "colors": ["blue"],
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1, "colors": "blue"},
            {"numbers": 2, "colors": "blue"},
        ]
        assert result == expected

    def test_query_with_two_parameters_and_two_lists(self):
        params = {
            "numbers": [1, 2],
            "colors": ["blue", "green"],
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1, "colors": "blue"},
            {"numbers": 1, "colors": "green"},
            {"numbers": 2, "colors": "blue"},
            {"numbers": 2, "colors": "green"},
        ]
        assert result == expected

    def test_query_with_one_parameter_and_one_list(self):
        params = {
            "numbers": [1, 2],
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1},
            {"numbers": 2},
        ]
        assert result == expected

    def test_query_with_two_parameters_and_one_none(self):
        params = {
            "numbers": [1, 2],
            "colors": None,
        }
        result = database.create_query(**params)
        expected = [
            {"numbers": 1},
            {"numbers": 2},
        ]
        assert result == expected

    def test_query_with_two_parameters_and_only_none(self):
        params = {
            "numbers": None,
            "colors": None,
        }
        result = database.create_query(**params)
        expected = [{}]
        assert result == expected

    def test_query_with_no_parameters(self):
        params = {}
        result = database.create_query(**params)
        expected = [{}]
        assert result == expected
