from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    second_name: str
    hashed_password: str
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserEdit(UserBase):
    password: str | None = None


class User(UserBase):
    id: int
