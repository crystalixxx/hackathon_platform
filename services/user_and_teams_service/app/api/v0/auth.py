from datetime import timedelta
from typing import Annotated

from app.api.dependencies import UOWAlchemyDep
from app.core.config import settings
from app.core.security import create_access_token
from app.database.schemas.user import UserCreate
from app.services.user import UserService
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

auth_router = APIRouter()


@auth_router.post("/sign_up")
async def sign_up(uow: UOWAlchemyDep, user: UserCreate):
    # user_dict = user.model_dump(exclude_none=True)
    new_user = await UserService().sign_up_new_user(uow, user)
    new_user = await UserService().get_user_by_id(uow, new_user)

    access_token_expires = timedelta(
        minutes=settings.security.access_token_expires_minutes
    )

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

    access_token_expires = timedelta(
        minutes=settings.security.access_token_expires_minutes
    )

    access_token = create_access_token(
        data={"sub": form_data.username, "permissions": "user"},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
