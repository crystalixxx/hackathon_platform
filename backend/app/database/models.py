from typing import Optional, List

from pydantic import EmailStr
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
    __tablename__ = "user"

    email: EmailStr = Column(String, unique=True, nullable=False)
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False, default="user")
    link_cv: str = Column(String, nullable=False)

    teams: Mapped[Optional["Team"]] = relationship("Team", secondary="TeamUser", back_populates="users")


class Icon(BaseModel):
    __tablename__ = "icon"

    title: str = Column(String, nullable=False, unique=True)
    icon_link: str = Column(String, nullable=False)

    teams: Mapped[Optional["Team"]] = relationship("Team", secondary="TeamIconSocial", back_populates="icons")


class Team(BaseModel):
    __tablename__ = "team"

    title: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=False)
    icon_link: str = Column(String, nullable=False)
    captain_id: int = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_looking_for_members: bool = Column(Boolean, nullable=False, default=False)

    users: Mapped[List["User"]] = relationship("User", secondary="TeamUser", back_populates="teams")
    icons: Mapped[Optional[List["Icon"]]] = relationship("Icon", secondary="TeamIconSocial", back_populates="teams")
    common_tags: Mapped[Optional[List["CommonTag"]]] = relationship("CommonTag", secondary="TeamCommonTag",
                                                                    back_populates="teams")
    field_tags: Mapped[Optional[List["FieldTag"]]] = relationship("FieldTag", secondary="TeamFieldTag",
                                                                  back_populates="teams")


class TeamRole(BaseModel):
    __tablename__ = "team_role"

    title: str = Column(String, nullable=False)


class TeamUser(ManyToManyBase):
    __tablename__ = "team_user"

    team_id: int = Column(Integer, ForeignKey("team.id"), primary_key=True, nullable=False)
    user_id: int = Column(Integer, ForeignKey("user.id"), primary_key=True, nullable=False)
    is_accepted: bool = Column(Boolean, nullable=False, default=False)
    team_role_id: int = Column(Integer, ForeignKey("team_role.id"), nullable=False)

    team_role: Mapped[Optional[TeamRole]] = relationship("TeamRole")


class TeamIconSocial(ManyToManyBase):
    __tablename__ = "team_icon_social"

    icon_id: int = Column(Integer, ForeignKey("icon.id"), primary_key=True, nullable=False)
    team_id: int = Column(Integer, ForeignKey("team.id"), primary_key=True, nullable=False)

    icon: Mapped["Icon"] = relationship("Icon")
    team: Mapped["Team"] = relationship("Team")


class CommonTag(BaseModel):
    __tablename__ = "common_tag"

    title: str = Column(String, nullable=False)
    color: str = Column(String, nullable=False, default="#000000")

    teams: Mapped[Optional[List["Team"]]] = relationship("Team", secondary="TeamCommonTag", back_populates="common_tags")


class FieldTag(BaseModel):
    __tablename__ = "field_tag"

    title: str = Column(String, nullable=False)
    color: str = Column(String, nullable=False, default="#000000")

    teams: Mapped[Optional[List["Team"]]] = relationship("Team", secondary="TeamFieldTag", back_populates="field_tags")


class TeamCommonTag(ManyToManyBase):
    __tablename__ = "team_common_tag"

    team_id: int = Column(Integer, ForeignKey("team.id"), primary_key=True, nullable=False)
    common_tag_id: int = Column(Integer, ForeignKey("common_tag.id"), primary_key=True, nullable=False)


class TeamFieldTag(ManyToManyBase):
    __tablename__ = "team_field_tag"

    team_id: int = Column(Integer, ForeignKey("team.id"), primary_key=True, nullable=False)
    field_tag_id: int = Column(Integer, ForeignKey("field_tag.id"), primary_key=True, nullable=False)
