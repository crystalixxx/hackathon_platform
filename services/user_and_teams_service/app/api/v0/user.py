from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.dependencies import UOWAlchemyDep
from app.core.auth import get_current_user
from app.database.schemas.user import UserCreate, UserSchema, UserUpdate
from app.database.schemas.user_tag import UserTagCreate, UserTagSchema, UserTagUpdate
from app.services.user import UserService

user_router = APIRouter()


@user_router.get("/", response_model=list[UserSchema])
async def get_users(uow: UOWAlchemyDep):
    return await UserService().get_users(uow)


@user_router.get("/id/{user_id}", response_model=UserSchema)
async def get_user_by_id(uow: UOWAlchemyDep, user_id: int):
    return await UserService().get_user_by_id(uow, user_id)


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
    if current_user.role not in ["user"] and user_id != current_user.id:
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


@user_router.get("/tag/{user_id}", response_model=list[UserTagSchema])
async def get_user_tags(uow: UOWAlchemyDep, user_id: int):
    return await UserService().get_user_tags(uow, user_id)


@user_router.get("/tag/{user_id}/{tag_name}", response_model=Optional[UserTagSchema])
async def get_user_tags_by_name(uow: UOWAlchemyDep, user_id: int, tag_name: str):
    return await UserService().get_user_tag_by_name(uow, user_id, tag_name)


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


@user_router.patch("/tag/{user_id}/{tag_name}")
async def update_user_tag(
    uow: UOWAlchemyDep,
    user_id: int,
    tag_name: str,
    tag: UserTagUpdate,
    current_user=Depends(get_current_user),
):
    if current_user.role not in ["user"] and tag.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission denied",
        )

    return await UserService().update_user_tag(uow, tag, user_id, tag_name)


@user_router.delete("/tag/{user_id}/{tag_name}", response_model=UserTagSchema)
async def delete_user_tag(
    uow: UOWAlchemyDep,
    user_id: int,
    tag_name: str,
    current_user=Depends(get_current_user),
):
    deleting_tag = await UserService().get_user_tag_by_name(uow, user_id, tag_name)

    if current_user.role not in ["user"] and deleting_tag.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission denied",
        )

    return await UserService().delete_user_tag(uow, user_id, tag_name)
