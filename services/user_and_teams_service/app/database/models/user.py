from typing import List, Optional

from pydantic import AnyUrl, EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.database.schemas.user import UserSchema
from app.database.schemas.user_tag import UserTagSchema

from . import base, team


class User(base.BaseModel):
    __tablename__ = "t_user"

    email: EmailStr = Column(String(256), unique=True, nullable=False)
    first_name: str = Column(String(256), nullable=False)
    last_name: str = Column(String(256), nullable=False)
    hashed_password: str = Column(String(256), nullable=False)
    role: Optional[str] = Column(String(256), default=None)
    link_cv: Optional[AnyUrl] = Column(String(256), default=None)

    tags: Mapped[List["UserTag"]] = relationship("UserTag", lazy="selectin")
    teams: Mapped[List["team.Team"]] = relationship(
        "Team", secondary="t_team_user", back_populates="users", lazy="selectin"
    )

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            hashed_password=self.hashed_password,
            role=self.role,
            link_cv=self.link_cv,
            tags=self.tags,
        )

    @classmethod
    def convert_scheme(cls):
        return UserSchema


class UserTag(base.BaseModel):
    __tablename__ = "t_user_tag"

    user_id: int = Column(
        Integer, ForeignKey("t_user.id", ondelete="CASCADE"), nullable=False
    )
    name: str = Column(String(256), nullable=False)

    def to_read_model(self) -> UserTagSchema:
        return UserTagSchema(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
        )

    @classmethod
    def convert_scheme(cls):
        return UserTagSchema
