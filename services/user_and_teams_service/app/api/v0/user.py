from api.dependencies import UOWAlchemyDep
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.core.auth import get_current_user
from app.database.schemas.user import UserCreate, UserSchema, UserUpdate
from app.database.schemas.user_tag import UserTagCreate, UserTagSchema
from app.services.user import UserService

user_router = APIRouter()


@user_router.get("/", response_model=list[UserSchema])
async def get_users(uow: UOWAlchemyDep):
    return await UserService().get_users(uow)


@user_router.post("/")
async def create_user(
    uow: UOWAlchemyDep, user: UserCreate, current_user=Depends(get_current_user)
):
    if current_user.role not in ["user"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission denied",
        )

    return await UserService().create_user(uow, user)


@user_router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    uow: UOWAlchemyDep, user_id: int, current_user=Depends(get_current_user)
):
    if current_user.role not in ["user"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission denied",
        )

    return await UserService().delete_user(uow, user_id)


@user_router.patch("/{user_id}", response_model=UserSchema)
async def update_user(
    uow: UOWAlchemyDep,
    user: UserUpdate,
    user_id: int,
    current_user=Depends(get_current_user),
):
    if current_user.role not in ["user"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission denied",
        )

    return await UserService().update_user(uow, user, user_id)


@user_router.post("/tag")
async def create_user_tag(
    uow: UOWAlchemyDep, tag: UserTagCreate, current_user=Depends(get_current_user)
):
    if current_user.role not in ["user"] and tag.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission denied",
        )

    return await UserService().create_user_tag(uow, tag)
