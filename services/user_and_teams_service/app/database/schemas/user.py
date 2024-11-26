from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from .user_tag import UserTagSchema


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    link_cv: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    role: Optional[str] = None
    link_cv: Optional[str] = None
    password: Optional[str] = None


class UserSchema(UserBase):
    id: int
    hashed_password: str

    tags: Optional[list[UserTagSchema]] = None
