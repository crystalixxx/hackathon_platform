from api.v0.main import main_v0_router
from database.models.base import Base
from fastapi import FastAPI
from uvicorn import run

metadate = Base.metadata

app = FastAPI(title="Hackathon Platform", docs_url="/api/docs", openapi_url="/api")
app.include_router(main_v0_router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
