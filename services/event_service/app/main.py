from create_fastapi_app import init_app
from database.models.base import Base
from uvicorn import run

metadata = Base.metadata

fastapi = init_app()

if __name__ == "__main__":
    run("main:fastapi", host="0.0.0.0", reload=True, port=8000)
