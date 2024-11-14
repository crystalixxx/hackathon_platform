from sqlalchemy.orm import Session

from app.database.models import UserTag
from app.database.schemas.user import UserTagCreate, UserTagUpdate, UserTagSchema
from app.database.crud.user import get_user_by_id


def get_user_tags(db: Session, user_id: int) -> list[UserTagSchema]:
    return db.query(UserTag).filter(UserTag.user_id == user_id).all()


def get_tag_by_name(db: Session, user_id: str, tag_name: str) -> UserTagSchema | None:
    return db.query(UserTag).filter(UserTag.user_id == user_id).filter(UserTag.name == tag_name).first()


def get_tag_by_id(db: Session, tag_id: int) -> UserTagSchema | None:
    return db.query(UserTag).filter(UserTag.id == tag_id).first()


def create_user_tag(db: Session, user_tag: UserTagCreate) -> UserTagSchema | None:
    if get_user_by_id(db, user_tag.user_id) is None:
        return None

    if get_tag_by_name(db, user_tag.user_id, user_tag.name) is not None:
        return None

    dict_user_tag = user_tag.dict(exclude_none=True)
    tag = UserTag(**dict_user_tag)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def update_user_tag(db: Session, user_tag_id: int, user_tag: UserTagUpdate) -> UserTagSchema | None:
    old_tag = get_tag_by_id(db, user_tag_id)

    if old_tag is None:
        return None

    dict_user_tag = user_tag.dict(exclude_none=True)
    for key, value in dict_user_tag.items():
        setattr(old_tag, key, value)

    db.add(old_tag)
    db.commit()
    db.refresh(old_tag)

    return old_tag


def delete_user_tag(db: Session, user_tag_id: int) ->  UserTagSchema | None:
    user_tag = get_tag_by_id(db, user_tag_id)

    if user_tag is None:
        return None

    db.delete(user_tag)
    db.commit()

    return user_tag
