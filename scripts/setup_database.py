import asyncio
import functools
from collections.abc import Sequence

import deta

from scripts import faction_data, map_data, tile_data
from ti4_mapmaker_api import config, database

settings = config.get_settings()
project_key = settings.DETA_PROJECT_KEY

deta_engine = deta.Deta(project_key)
deta_db = functools.partial(database.AsyncBase, deta_engine)


async def _put_in_db(document: str, records: Sequence[dict]) -> None:
    """Puts items in Deta Base."""
    async with deta_db(document) as db:
        await db.put_many(records)


async def populate() -> None:
    """Main loop for database populate calls."""

    # Convert list of Pydantic models to list of dicts.
    tiles = [tile.dict() for tile in tile_data.parsed()]
    factions = [faction.dict() for faction in faction_data.parsed()]
    maps = [map.dict() for map in map_data.parsed()]

    tasks = [
        _put_in_db("tiles", tiles),
        _put_in_db("factions", factions),
        _put_in_db("maps", maps),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(populate())
