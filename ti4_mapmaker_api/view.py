from deta import Deta
from fastapi import APIRouter

from ti4_mapmaker_api import config
from ti4_mapmaker_api import database as db
from ti4_mapmaker_api import schema

settings = config.get_settings()
project_key = settings.deta_project_key

engine = Deta(project_key)
router = APIRouter()


@router.get("/maps/", response_model=list[schema.Map])
async def read_maps() -> list[schema.Map]:
    ...


@router.get("/factions/")
async def read_factions():
    ...


@router.get("/tiles/")
async def read_tiles():
    async with db.AsyncBase(engine, "tile") as base:
        results = await base.fetch()
    db_tiles = [schema.Tile(**result) for result in results.items]
    return db_tiles


@router.get("/generate/")
async def generate():
    ...
