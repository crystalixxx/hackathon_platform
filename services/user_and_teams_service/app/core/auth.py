from app.core.config import settings
from app.core.security import oauth2_scheme
from app.core.utils.unit_of_work import CachedSQLAlchemyUnitOfWork
from app.services.user import UserService
from fastapi import Depends, HTTPException
from jwt import DecodeError, decode
from starlette import status


async def get_current_user(
    uow=Depends(CachedSQLAlchemyUnitOfWork), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.security.key, algorithms=[settings.security.algorithm]
        )
        email = payload.get("sub")

        if email is None:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = await UserService().get_user_by_email(uow, email)

    if user is None:
        raise credentials_exception

    return user
