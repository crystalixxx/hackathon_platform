from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8888)
