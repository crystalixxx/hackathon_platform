from pydantic import BaseModel, ConfigDict, Field
from typing import List
from datetime import datetime


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")

    model_config = ConfigDict(from_attributes=True)


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagSchema(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagWithPostsCountSchema(TagSchema):
    posts_count: int

    model_config = ConfigDict(from_attributes=True)
    