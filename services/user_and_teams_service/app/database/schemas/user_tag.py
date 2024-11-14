from pydantic import BaseModel


class UserTagBase(BaseModel):
    user_tag_id: int
    user_id: int
    name: str


class UserTagCreate(UserTagBase):
    user_id: int


class UserTagResponse(UserTagBase):
    user_tag_id: int
    user_id: int

    model_config = {"from_attributes": True}
