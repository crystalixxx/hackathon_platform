from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    second_name: str
    role: str
    link_cv: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserCreateSchema(UserBase):
    hashed_password: str


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    second_name: Optional[str]
    role: Optional[str]
    link_cv: Optional[str]
    hashed_password: Optional[str]

    class Config:
        from_attributes = True


class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True
