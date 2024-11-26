from app.database.models.base import Base
from fastapi import FastAPI
from uvicorn import run
from redis_client import RedisClient

metadate = Base.metadata
app = FastAPI()

redis_client = RedisClient()


@app.get("/")
def root():
    return {"message": "редис в салате"}


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
