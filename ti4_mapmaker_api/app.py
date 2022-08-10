from fastapi import FastAPI

from ti4_mapmaker_api import view


def create_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(view.router)
    return app
