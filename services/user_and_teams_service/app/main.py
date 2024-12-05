from fastapi import FastAPI
from uvicorn import run

from app import init_app
from app.api.v0.main import main_v0_router
from app.core.config import config
from app.database.models.base import Base
from app.database.session import sessionmanager

metadate = Base.metadata

app = init_app()

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
