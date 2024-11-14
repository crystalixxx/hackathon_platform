from sqlalchemy.orm import Session

from app.core.security import get_hashed_password
from app.database.models import User
from app.database.schemas.user import UserCreate, UserUpdate, UserSchema


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserSchema]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int) -> UserSchema | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserSchema | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserSchema) -> UserSchema | None:
    if get_user_by_email(db, user.email):
        return None

    dict_create_user = user.dict(exclude_none=True)
    hashed_password = get_hashed_password(user.password)

    user = User(**dict_create_user)
    user.hashed_password = hashed_password

    db.add(user)
    db.commit()

    return user


def update_user(db: Session, user_id: int, user: UserUpdate) -> UserSchema | None:
    old_user = get_user_by_id(db, user_id)

    if old_user is None:
        return None

    dict_new_user = user.dict(exclude_none=True)

    if dict_new_user["password"] is not None:
        setattr(old_user, "hashed_password", get_hashed_password(dict_new_user["password"]))
        del dict_new_user["password"]

    for key, value in dict_new_user.items():
        if value is not None:
            setattr(old_user, key, value)

    db.add(old_user)
    db.commit()
    db.refresh(old_user)

    return old_user


def delete_user(db: Session, user_id: int) -> User | None:
    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    db.delete(user)
    db.commit()

    return user