from sqlalchemy.orm import Session

from app.database.models import Request
from app.database.schemas.request import RequestCreate, RequestSchema


def get_requests(db: Session, skip: int = 0, limit: int = 100) -> list[RequestSchema]:
    return db.query(Request).offset(skip).limit(limit).all()


def get_request_by_id(db: Session, request_id: int) -> RequestSchema | None:
    return db.query(Request).filter(Request.id == request_id).first()


def create_request(db: Session, request: RequestCreate) -> RequestSchema:
    dict_create_request = request.dict(exclude_none=True)
    new_request = Request(**dict_create_request)

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


def update_request(db: Session, request_id: int, request: RequestCreate) -> RequestSchema | None:
    old_request = get_request_by_id(db, request_id)

    if old_request is None:
        return None

    dict_update_request = request.dict(exclude_none=True)

    for key, value in dict_update_request.items():
        if value is not None:
            setattr(old_request, key, value)

    db.add(old_request)
    db.commit()
    db.refresh(old_request)

    return old_request


def delete_request(db: Session, request_id: int) -> Request | None:
    request = get_request_by_id(db, request_id)

    if request is None:
        return None

    db.delete(request)
    db.commit()

    return request
