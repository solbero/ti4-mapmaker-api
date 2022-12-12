from fastapi import FastAPI

from ti4_mapmaker_api import view

description = """
TI4 Mapmaker API is the backend for the TI4 Mapmaker website.

Have you found a problem, or have a question?
Please [submit an issue](https://github.com/solbero/ti4-mapmaker-api/issues) on GitHub.
"""

tags_metadata = [
    {
        "name": "Maps",
        "description": "Information about Twilight Imperium 4 maps",
    },
    {
        "name": "Factions",
        "description": "Information about Twilight Imperium 4 factions",
    },
    {
        "name": "Tiles",
        "description": "Information about Twilight Imperium 4 tiles",
    },
]


def create() -> FastAPI:
    app = FastAPI(
        docs_url="/",
        redoc_url=None,
        title="TI4 Mapmaker API",
        description=description,
        license_info={
            "name": "GPLv3",
            "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
        },
        openapi_tags=tags_metadata,
    )
    app.include_router(view.router)
    return app
