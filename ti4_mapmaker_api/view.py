import functools
from typing import Optional

from deta import Deta
from fastapi import APIRouter, Depends, HTTPException, Query

from ti4_mapmaker_api import config, database, schema

settings = config.get_settings()
project_key = settings.deta_project_key

engine = Deta(project_key)
router = APIRouter()


def get_detabase():
    return functools.partial(database.AsyncBase, engine)


@router.get("/maps/", response_model=list[schema.Map])
async def read_maps(
    players: Optional[list[schema.Players]] = Query(None),  # noqa: B008
    style: Optional[list[schema.Style]] = Query(None),  # noqa: B008
    detabase=Depends(get_detabase),  # noqa: B008
):
    query = database.create_query(players=players, style=style)

    async with detabase(document="maps") as base:
        results = await base.fetch(query)
    if results.count > 0:
        return [schema.Map.parse_obj(result) for result in results.items]
    else:
        raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/maps/{key}", response_model=schema.Map)
async def read_maps_by_key(
    key: str = Query(regex=r"^[1-8]{1}-[a-z]+$"),  # noqa: B008
    detabase=Depends(get_detabase),  # noqa: B008
):
    async with detabase(document="maps") as base:
        result = await base.get(key)
    if result:
        return schema.Map.parse_obj(result)
    else:
        raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/factions/", response_model=list[schema.Faction])
async def read_factions(
    release: Optional[list[schema.Release]] = Query(None),  # noqa: B008
    detabase=Depends(get_detabase),  # noqa: B008
):
    query = database.create_query(release=release)

    async with detabase(document="factions") as base:
        results = await base.fetch(query)
    if results.count > 0:
        return [schema.Faction.parse_obj(result) for result in results.items]
    else:
        raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/factions/{key}", response_model=schema.Faction)
async def read_factions_by_key(
    key: schema.NameSlug,
    detabase=Depends(get_detabase),  # noqa: B008
):
    async with detabase(document="factions") as base:
        result = await base.get(key)
    if result:
        return schema.Faction.parse_obj(result)
    else:
        raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/tiles/", response_model=list[schema.Tile])
async def read_tiles(
    tag: Optional[list[schema.Tag]] = Query(None),  # noqa: B008
    release: Optional[list[schema.Release]] = Query(None),  # noqa: B008
    detabase=Depends(get_detabase),  # noqa: B008
):
    query = database.create_query(tag=tag, release=release)

    async with detabase(document="tiles") as base:
        results = await base.fetch(query)
    if results.count > 0:
        return [schema.Tile.parse_obj(result) for result in results.items]
    else:
        raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/tiles/{key}", response_model=schema.Tile)
async def read_tiles_by_key(
    key: str = Query(regex=r"^\d{1,2}[A-B]?$"),  # noqa: B008
    detabase=Depends(get_detabase),  # noqa: B008
):
    async with detabase(document="tiles") as base:
        result = await base.get(key)
    if result:
        return schema.Tile.parse_obj(result)
    else:
        raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/generate/")
async def generate():
    ...
