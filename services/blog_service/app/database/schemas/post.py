from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PostType(str, Enum):
    ARTICLE = "article"
    NEWS = "news"
    TUTORIAL = "tutorial"
    REVIEW = "review"


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SCHEDULED = "scheduled"


class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=10)
    type: PostType = Field(default=PostType.ARTICLE)
    status: PostStatus = Field(default=PostStatus.DRAFT)
    publication_date: Optional[datetime] = None
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    content: Optional[str] = Field(None, min_length=10)
    type: Optional[PostType] = None
    status: Optional[PostStatus] = None
    publication_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PostSchema(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostDetailSchema(PostSchema):
    comments_count: int = 0
    tags: List["TagSchema"] = []
    categories: List["CategorySchema"] = []

    model_config = ConfigDict(from_attributes=True)
