from contextlib import asynccontextmanager

from app.api.v0.main import main_v0_router
from app.core.config import settings
from app.database.session import sessionmanager
from fastapi import FastAPI


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(
            str(settings.db.url),
            echo=settings.db.echo,
            echo_pool=settings.db.echo_pool,
            pool_size=settings.db.pool_size,
            max_overflow=settings.db.max_overflow,
        )

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
