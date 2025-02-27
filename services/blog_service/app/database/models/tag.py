from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.models.base import BaseModel, ManyToManyBase


class Tag(BaseModel):
    __tablename__ = "tag"

    name = Column(String(50), nullable=False, unique=True, index=True)

    posts = relationship("Post", secondary="posts_tags", back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


class PostTag(ManyToManyBase):
    __tablename__ = "posts_tags"

    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)
    