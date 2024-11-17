from auth.auth import auth_router
from fastapi import APIRouter

main_v0_router = APIRouter(prefix="/v0")
main_v0_router.include_router(auth_router, prefix="/auth")
