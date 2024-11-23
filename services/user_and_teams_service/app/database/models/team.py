from typing import List, Optional

from app.database.schemas.team import TeamSchema
from pydantic import AnyUrl
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
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

    def to_read_model(self) -> TeamSchema:
        return TeamSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            icon_url=self.icon_url,
            captain_id=self.captain_id,
            is_looking_for_members=self.is_looking_for_members,
        )


class TeamTag(base.ManyToManyBase):
    __tablename__ = "t_team_tag"

    team_id: int = Column(
        Integer, ForeignKey("t_team.id"), nullable=False, primary_key=True
    )
    user_tag_id: int = Column(
        Integer, ForeignKey("t_user_tag.id"), nullable=False, primary_key=True
    )


class TeamUser(base.ManyToManyBase):
    __tablename__ = "t_team_user"

    team_id: int = Column(
        Integer, ForeignKey("t_team.id"), nullable=False, primary_key=True
    )
    user_id: int = Column(
        Integer, ForeignKey("t_user.id"), nullable=False, primary_key=True
    )
    role_name: str = Column(String(256), nullable=False)
