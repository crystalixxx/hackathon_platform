from pydantic import BaseModel


class UserTagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class UserTagCreateSchema(UserTagBase):
    user_id: int


class UserTagSchema(UserTagBase):
    user_tag_id: int
    user_id: int
