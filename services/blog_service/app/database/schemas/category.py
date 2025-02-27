from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CategorySchema(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryWithPostsCountSchema(CategorySchema):
    posts_count: int

    model_config = ConfigDict(from_attributes=True)
