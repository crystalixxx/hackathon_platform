from typing import Optional
from pydantic import BaseModel, HttpUrl


class UserBase(BaseModel):
    email: str
    first_name: str
    second_name: str
    hashed_password: str
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserEdit(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # заменил orm_mode


class TagBase(BaseModel):
    name: str
    color: str = "#000000"


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True  # заменил orm_mode
        json_schema_extra = {}  # заменил schema_extra


class HackathonBase(BaseModel):
    name: str
    description: str
    status: Optional[int] = None
    redirect_link: Optional[HttpUrl] = None
    poster_link: Optional[HttpUrl] = None

    class Config:
        from_attributes = True  # заменил orm_mode
