from app.database.models.base import Base
from fastapi import FastAPI
from uvicorn import run

metadate = Base.metadata

app = FastAPI()


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
