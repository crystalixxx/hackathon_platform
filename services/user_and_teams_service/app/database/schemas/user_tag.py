from pydantic import BaseModel, ConfigDict


class UserTagBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserTagCreate(UserTagBase):
    user_id: int


class UserTagUpdate(BaseModel):
    name: str


class UserTagSchema(UserTagBase):
    user_tag_id: int
    user_id: int
