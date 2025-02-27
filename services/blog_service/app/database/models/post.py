from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Enum, Integer
from sqlalchemy.orm import relationship
import enum

from app.database.models.base import BaseModel


class PostType(enum.Enum):
    ARTICLE = "article"
    NEWS = "news"
    TUTORIAL = "tutorial"
    REVIEW = "review"


class PostStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SCHEDULED = "scheduled"


class Post(BaseModel):
    __tablename__ = "posts"

    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    type = Column(Enum(PostType), nullable=False, default=PostType.ARTICLE)
    status = Column(Enum(PostStatus), nullable=False, default=PostStatus.DRAFT)
    publication_date = Column(DateTime, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", backref="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="posts_tags", back_populates="posts")
    categories = relationship("Category", secondary="posts_categories", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', type={self.type}, status={self.status})>"
    