from uvicorn import run

from app import init_app
from app.database.models.base import Base

from app.api.routes import router

metadata = Base.metadata

app = init_app()
app.include_router(router)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
