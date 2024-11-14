import uuid

from pydantic import BaseModel


class UserTagBase(BaseModel):
    user_tag_id: uuid.UUID
    user_id: uuid.UUID
    name: str


class UserTagCreate(UserTagBase):
    user_id: uuid.UUID


class UserTagResponse(UserTagBase):
    user_tag_id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}
