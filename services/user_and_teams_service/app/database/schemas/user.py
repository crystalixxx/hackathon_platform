import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class TUserBase(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    second_name: str
    hashed_password: str
    role: str
    link_cv: Optional[str]
    created_at: datetime.datetime.utcnow()
    updated_at: datetime.datetime.utcnow()


class TUserCreate(TUserBase):
    hashed_password: str


class TUserUpdate(TUserBase):
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    role: Optional[str]
    link_cv: Optional[str]
    updated_at = datetime.datetime.utcnow()


class UserResponse(TUserBase):
    id: uuid.UUID
    created_at: datetime.datetime.utcnow()
    updated_at: datetime.datetime.utcnow()

    model_config = {"from_attributes": True}
