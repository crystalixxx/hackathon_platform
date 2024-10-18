from fastapi import HTTPException
from database import models, schemas
from sqlalchemy.orm import Session


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.User]:
    return db.query(models.User).offset(skip).limit(limit).all()
