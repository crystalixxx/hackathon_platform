from pydantic import AnyUrl
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, relationship

from . import base, user

class Team(base.BaseModel):
    __tablename__ = "t_team"

    title: str = Column(String(256), unique=True, nullable=False)
    description: str = Column(Text, default="")
    icon_url: Optional[AnyUrl] = Column(String(256), default=None)
    captain_id: id = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    is_looking_for_members: bool = Column(Boolean, default=False)

    tags: Mapped[List["user.UserTag"]] = relationship("UserTag", secondary="t_team_tag")
    requests: Mapped[List["user.User"]] = relationship("User", secondary="t_request")
    users: Mapped[List["user.User"]] = relationship(
        "User", secondary="t_team_user", back_populates="teams"
    )


class TeamTag(base.ManyToManyBase):
    __tablename__ = "t_team_tag"

    team_id: int = Column(Integer, ForeignKey("t_team.id"), nullable=False)
    user_tag_id: int = Column(Integer, ForeignKey("t_user_tag.id"), nullable=False)


class TeamUser(base.ManyToManyBase):
    __tablename__ = "t_team_user"

    team_id: int = Column(Integer, ForeignKey("t_team.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    role_name: str = Column(String(256), nullable=False)
