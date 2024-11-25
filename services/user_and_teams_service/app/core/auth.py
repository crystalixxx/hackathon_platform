from app.core.config import config
from app.core.security import oauth2_scheme, verify_password
from app.core.utils import SqlAlchemyUnitOfWork
from app.database.schemas.user import UserCreate, UserSchema
from app.database.session import get_db
from app.services import UserService
from fastapi import Depends, HTTPException
from jwt import DecodeError, decode
from sqlalchemy.orm import Session
from starlette import status


async def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(token, config.SECURITY_KEY, algorithms=[config.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    uow = SqlAlchemyUnitOfWork()
    user = UserService.get_user_by_email(uow, email)
    if user is None:
        raise credentials_exception

    return user


def authenticate_user(email: str, password: str, db):
    uow = SqlAlchemyUnitOfWork()
    user = UserService.get_user_by_email(uow, email)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def sign_up_new_user(
    db: Session,
    email: str,
    first_name: str,
    second_name: str,
    password: str,
    link_cv: str = None,
) -> UserSchema:
    uow = SqlAlchemyUnitOfWork()
    user = UserService.get_user_by_email(uow, email)

    if user:
        return False

    new_user = UserService.create_user(
        uow,
        UserCreate(
            email=email,
            first_name=first_name,
            second_name=second_name,
            password=password,
            link_cv=link_cv,
        ),
    )

    if new_user is None:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Can't create user with specified data",
        )

    return new_user
