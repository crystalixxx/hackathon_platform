from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    second_name: str
    hashed_password: str
    role: str
    link_cv: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    role: Optional[str]
    link_cv: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}


class UserResponse(UserBase):
    id: int
    created_at: datetime.utcnow()
    updated_at: datetime.utcnow()

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}
