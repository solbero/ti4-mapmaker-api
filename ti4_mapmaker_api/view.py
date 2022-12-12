import functools
from typing import Optional

import deta
from fastapi import APIRouter, Depends, HTTPException, Query

from ti4_mapmaker_api import config, database, schema

router = APIRouter()

project_settings = config.get_settings()
project_key = project_settings.deta_project_key

deta_engine = deta.Deta(project_key)
deta_db = functools.partial(database.AsyncBase, deta_engine)


def get_maps_document() -> str:
    """Returns the name of the maps document used in the database. Name is overridden during testing."""
    return "maps"


def get_factions_document() -> str:
    """Returns the name of the factions document used in the database. Name is overridden during testing."""
    return "factions"


def get_tiles_document() -> str:
    """Returns the name of the tiles document used in the database. Name is overridden during testing."""
    return "tiles"


@router.get("/maps/", response_model=list[schema.Map], tags=["Maps"])
async def read_maps(
    players: Optional[list[schema.Players]] = Query(None),  # noqa: B008
    style: Optional[list[schema.Style]] = Query(None),  # noqa: B008
    document: str = Depends(get_maps_document),  # noqa: B008
):
    """Endpoint for fetching all the maps or quering the maps database."""

    query = database.create_query(players=players, style=style)

    async with deta_db(document) as db:
        results = await db.fetch(query)
    if len(results) > 0:
        return [schema.Map.parse_obj(result) for result in results]
    else:
        raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/maps/{key}", response_model=schema.Map, tags=["Maps"])
async def read_maps_by_key(
    key: str = Query(regex=r"^[1-8]{1}-[a-z]+$"),  # noqa: B008
    document: str = Depends(get_maps_document),  # noqa: B008
):
    """Endpoint for fetching a map by key from the maps database."""

    async with deta_db(document) as db:
        result = await db.get(key)
    if result:
        return schema.Map.parse_obj(result)
    else:
        raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/factions/", response_model=list[schema.Faction], tags=["Factions"])
async def read_factions(
    release: Optional[list[schema.Release]] = Query(None),  # noqa: B008
    document: str = Depends(get_factions_document),  # noqa: B008
):
    """Endpoint for fetching all the factions or quering the factions database."""

    query = database.create_query(release=release)

    async with deta_db(document) as db:
        results = await db.fetch(query)
    if len(results) > 0:
        return [schema.Faction.parse_obj(result) for result in results]
    else:
        raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/factions/{key}", response_model=schema.Faction, tags=["Factions"])
async def read_factions_by_key(
    key: schema.NameSlug,
    document: str = Depends(get_factions_document),  # noqa: B008
):
    """Endpoint for fetching a faction by key from the factions database."""

    async with deta_db(document) as db:
        result = await db.get(key)
    if result:
        return schema.Faction.parse_obj(result)
    else:
        raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/tiles/", response_model=list[schema.Tile], tags=["Tiles"])
async def read_tiles(
    tag: Optional[list[schema.Tag]] = Query(None),  # noqa: B008
    release: Optional[list[schema.Release]] = Query(None),  # noqa: B008
    document: str = Depends(get_tiles_document),  # noqa: B008
):
    """Endpoint for fetching all the tiles or quering the tiles database."""

    query = database.create_query(tag=tag, release=release)

    async with deta_db(document) as db:
        results = await db.fetch(query)
    if len(results) > 0:
        return [schema.Tile.parse_obj(result) for result in results]
    else:
        raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/tiles/{key}", response_model=schema.Tile, tags=["Tiles"])
async def read_tiles_by_key(
    key: str = Query(regex=r"^\d{1,2}[A-B]?$"),  # noqa: B008
    document: str = Depends(get_tiles_document),  # noqa: B008
):
    """Endpoint for fetching a tile by key from the tiles database."""

    async with deta_db(document) as db:
        result = await db.get(key)
    if result:
        return schema.Tile.parse_obj(result)
    else:
        raise HTTPException(status_code=404, detail="No entries matched key")
