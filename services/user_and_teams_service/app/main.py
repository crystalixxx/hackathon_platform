from fastapi import FastAPI
from uvicorn import run

from app.api.v0.main import main_v0_router
from app.database.models.base import Base

metadate = Base.metadata

app = FastAPI(title="Hackathon Platform", docs_url="/api/docs", openapi_url="/api")
app.include_router(main_v0_router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
