from fastapi import FastAPI

from ti4_mapmaker_api import view


def create() -> FastAPI:
    app = FastAPI(debug=True, docs_url="/", redoc_url=None)
    app.include_router(view.router)
    return app
