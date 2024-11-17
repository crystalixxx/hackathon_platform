from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


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
    email: Optional[EmailStr]
    first_name: Optional[str]
    second_name: Optional[str]
    role: Optional[str]
    link_cv: Optional[str]
    password: Optional[str]


class UserSchema(UserBase):
    id: int
    hashed_password: str
