from api.v0.auth import auth_router
from api.v0.user import user_router
from fastapi import APIRouter

main_v0_router = APIRouter(prefix="/api/v0")
main_v0_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_v0_router.include_router(user_router, prefix="/user", tags=["user"])
