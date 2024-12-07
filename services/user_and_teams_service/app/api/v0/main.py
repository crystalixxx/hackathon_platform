from fastapi import APIRouter

from .auth import auth_router
from .team import team_router
from .user import user_router

main_v0_router = APIRouter(prefix="/api/v0")
main_v0_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_v0_router.include_router(user_router, prefix="/user", tags=["user"])
main_v0_router.include_router(team_router, prefix="/team", tags=["team"])
