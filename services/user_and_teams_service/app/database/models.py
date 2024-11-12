from typing import Optional, List

from pydantic import EmailStr, AnyUrl
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime, timezone


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class ManyToManyBase(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class User(BaseModel):
    __tablename__ = "t_user"

    email: EmailStr = Column(String(256), unique=True, nullable=False)
    first_name: str = Column(String(256), nullable=False)
    last_name: str = Column(String(256), nullable=False)
    hashed_password: str = Column(String(256), nullable=False)
    role: Optional[str] = Column(String(256), default=None)
    link_cv: Optional[AnyUrl] = Column(String(256), default=None)

    tags: Mapped[List["UserTag"]] = relationship("UserTag")
    teams: Mapped[List["Team"]] = relationship("Team", secondary="t_team_user", back_populates="users")


class UserTag(BaseModel):
    __tablename__ = "t_user_tag"

    user_id: int = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    name: str = Column(String(256), nullable=False)


class Team(BaseModel):
    __tablename__ = "t_team"

    title: str = Column(String(256), unique=True, nullable=False)
    description: str = Column(Text, default="")
    icon_url: Optional[AnyUrl] = Column(String(256), default=None)
    captain_id: id = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    is_looking_for_members: bool = Column(Boolean, default=False)

    tags: Mapped[List["UserTag"]] = relationship("UserTag", secondary="t_team_tag")
    requests: Mapped[List["User"]] = relationship("User", secondary="t_request")
    users: Mapped[List["User"]] = relationship("User", secondary="t_team_user", back_populates="teams")


class TeamTag(ManyToManyBase):
    __tablename__ = "t_team_tag"

    team_id: int = Column(Integer, ForeignKey("t_team.id"), nullable=False)
    user_tag_id: int = Column(Integer, ForeignKey("t_user_tag.id"), nullable=False)


class Request(ManyToManyBase):
    __tablename__ = "t_request"

    request_team_id: int = Column(Integer, ForeignKey("t_team.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    sent_by_team: bool = Column(Boolean, nullable=False)
    is_ok: bool = Column(Boolean, nullable=False, default=False)


class TeamUser(ManyToManyBase):
    __tablename__ = "t_team_user"

    team_id: int = Column(Integer, ForeignKey("t_team.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    role_name: str = Column(String(256), nullable=False)
