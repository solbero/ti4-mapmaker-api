from deta import Deta
from fastapi import APIRouter, Depends, HTTPException, Query

from ti4_mapmaker_api import config
from ti4_mapmaker_api import database as db
from ti4_mapmaker_api import schema

settings = config.get_settings()
project_key = settings.deta_project_key

engine = Deta(project_key)
router = APIRouter()


@router.get("/maps/", response_model=list[schema.Map])
async def read_maps(query: schema.MapQuery = Depends()):  # noqa: B008
    async with db.AsyncBase(engine, "maps") as base:
        results = await base.fetch(query.dict(exclude_defaults=True))
        if results.count > 0:
            return [schema.Map.parse_obj(result) for result in results.items]
    raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/maps/{key}", response_model=schema.Map)
async def read_maps_by_key(key: str = Query(regex=r"^[1-8]{1}-[a-z]+$")):  # noqa: B008
    async with db.AsyncBase(engine, "maps") as base:
        result = await base.get(key)
        if result:
            return schema.Map.parse_obj(result)
    raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/factions/", response_model=list[schema.Faction])
async def read_factions(query: schema.FactionQuery = Depends()):  # noqa: B008
    async with db.AsyncBase(engine, "factions") as base:
        results = await base.fetch(query.dict(exclude_defaults=True))
        if results.count > 0:
            return [schema.Faction.parse_obj(result) for result in results.items]
    raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/factions/{key}", response_model=schema.Faction)
async def read_factions_by_key(key: schema.NameSlug):  # noqa: B008
    async with db.AsyncBase(engine, "factions") as base:
        result = await base.get(key.value)
        if result:
            return schema.Faction.parse_obj(result)
    raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/tiles/", response_model=list[schema.Tile])
async def read_tiles(query: schema.TileQuery = Depends()):  # noqa: B008
    async with db.AsyncBase(engine, "tiles") as base:
        results = await base.fetch(query.dict(exclude_defaults=True))
        if results.count > 0:
            return [schema.Tile.parse_obj(result) for result in results.items]
    raise HTTPException(status_code=404, detail="No entries matched query")


@router.get("/tiles/{key}", response_model=schema.Tile)
async def read_tiles_by_key(key: str = Query(regex=r"^\d{1,2}[A-B]?$")):  # noqa: B008
    async with db.AsyncBase(engine, "tiles") as base:
        result = await base.get(key)
        if result:
            return schema.Tile.parse_obj(result)
    raise HTTPException(status_code=404, detail="No entries matched key")


@router.get("/generate/")
async def generate():
    ...
