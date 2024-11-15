from pydantic import EmailStr, AnyUrl
from typing import Optional, List
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from . import base, team


class User(base.BaseModel):
    __tablename__ = "t_user"

    email: EmailStr = Column(String(256), unique=True, nullable=False)
    first_name: str = Column(String(256), nullable=False)
    last_name: str = Column(String(256), nullable=False)
    hashed_password: str = Column(String(256), nullable=False)
    role: Optional[str] = Column(String(256), default=None)
    link_cv: Optional[AnyUrl] = Column(String(256), default=None)

    tags: Mapped[List["UserTag"]] = relationship("UserTag")
    teams: Mapped[List["team.Team"]] = relationship(
        "Team", secondary="t_team_user", back_populates="users"
    )


class UserTag(base.BaseModel):
    __tablename__ = "t_user_tag"

    user_id: int = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    name: str = Column(String(256), nullable=False)
