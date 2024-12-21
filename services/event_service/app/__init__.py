from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v0.main import main_v0_router
from app.core.config import config
from app.database.session import sessionmanager


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(config.database_connection_url)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    server = FastAPI(
        title="FastAPI server",
        docs_url="/api/docs",
        openapi_url="/api",
        lifespan=lifespan,
    )
    server.include_router(main_v0_router)

    return server
