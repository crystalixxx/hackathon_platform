from uvicorn import run
from fastapi import FastAPI

app = FastAPI()


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8888)
