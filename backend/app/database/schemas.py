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


class TagBase(BaseModel):
    name: str
    transparency: float = 1.0
    color: str = "rgba(255, 87, 51, transparency)"


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    users: list[User] = []

    class Config:
        orm_mode = True
        schema_extra = {}


class HackathonBase(BaseModel):
    name: str
    description: str
