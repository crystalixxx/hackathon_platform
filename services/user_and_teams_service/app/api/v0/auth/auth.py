from fastapi import APIRouter, Request

auth_router = APIRouter()


@auth_router.post("/sign_up")
async def sign_up(request: Request):
    return {"status": "ok"}
