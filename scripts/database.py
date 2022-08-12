import asyncio
from typing import cast

from deta import Deta

from scripts import faction_data, map_data, tile_data
from ti4_mapmaker_api import config
from ti4_mapmaker_api import database as db

settings = config.get_settings()
project_key = settings.deta_project_key

engine = Deta(project_key)


async def _put_in_db(engine: Deta, collection: str, items: list[dict]):
    """Puts items in Deta Base."""
    batch_size = 25
    async with db.AsyncBase(engine, collection) as base:
        for index in range(0, len(items), batch_size):
            batch = cast(list, items[index : index + batch_size])
            await base.put_many(batch)


def populate():
    """Main loop for database async calls."""
    # Convert list of Pydantic models to list of dicts.
    tile_list = [tile.dict() for tile in tile_data.parsed()]
    faction_list = [faction.dict() for faction in faction_data.parsed()]
    map_list = [map.dict() for map in map_data.parsed()]

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(_put_in_db(engine, "tiles", tile_list)),
        loop.create_task(_put_in_db(engine, "factions", faction_list)),
        loop.create_task(_put_in_db(engine, "maps", map_list)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close


if __name__ == "__main__":
    populate()
