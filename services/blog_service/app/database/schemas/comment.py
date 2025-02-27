from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    post_id: int
    author_id: int
    parent_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    is_approved: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class CommentSchema(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_approved: bool

    model_config = ConfigDict(from_attributes=True)


class CommentDetailSchema(CommentSchema):
    replies: List["CommentSchema"] = []

    model_config = ConfigDict(from_attributes=True)


CommentDetailSchema.model_rebuild()
