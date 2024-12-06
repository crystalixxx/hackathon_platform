from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.dependencies import UOWAlchemyDep
from app.core.config import config
from app.core.security import create_access_token
from app.database.schemas.user import UserCreate
from app.services.user import UserService

auth_router = APIRouter()


@auth_router.post("/sign_up")
async def sign_up(uow: UOWAlchemyDep, user: UserCreate):
    user_dict = user.model_dump(exclude_none=True)
    del user_dict["role"]

    new_user = await UserService().sign_up_new_user(uow, **user_dict)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": new_user.email, "permissions": "user"},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login")
async def login(
    uow: UOWAlchemyDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    access = await UserService().authenticate_user(
        uow, form_data.username, form_data.password
    )

    if not access:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": form_data.username, "permissions": "user"},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
