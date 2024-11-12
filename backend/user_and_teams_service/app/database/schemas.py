from typing import Optional
from pydantic import BaseModel, HttpUrl, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class TagBase(BaseModel):
    name: str
    color: str = "#000000"


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True, json_schema_extra={})


class HackathonBase(BaseModel):
    name: str
    description: str
    status: Optional[int] = None
    redirect_link: Optional[HttpUrl] = None
    poster_link: Optional[HttpUrl] = None

    model_config = ConfigDict(from_attributes=True)
