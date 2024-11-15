from fastapi import APIRouter

from auth.auth import auth_router

main_v0_router = APIRouter(prefix="/v0")
main_v0_router.include_router(auth_router, prefix="/auth")
