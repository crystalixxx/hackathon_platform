from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.models.base import BaseModel, ManyToManyBase


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    posts = relationship("Post", secondary="posts_categories", back_populates="categories")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class PostCategory(ManyToManyBase):
    __tablename__ = "posts_categories"

    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
