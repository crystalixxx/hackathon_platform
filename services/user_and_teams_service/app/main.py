from uvicorn import run
from app import init_app
from app.database.models.base import Base

metadate = Base.metadata

app = init_app()

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
