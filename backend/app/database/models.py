from typing import Optional, List

from pydantic import EmailStr
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime, timezone

from sqlalchemy.testing.schema import mapped_column

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

    teams: Mapped[Optional[List["Team"]]] = relationship("Team", secondary="TeamCommonTag",
                                                         back_populates="common_tags")


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


class Date(BaseModel):
    __tablename__ = "date"

    date_start: DateTime = Column(DateTime, nullable=False)
    date_end: DateTime = Column(DateTime, nullable=False)


class Status(BaseModel):
    __tablename__ = "status"

    title: str = Column(String, nullable=False, unique=True)

    events: Mapped[Optional[List["Event"]]] = relationship("Event", back_populates="status")
    tracks: Mapped[Optional[List["Track"]]] = relationship("Track", back_populates="status")


class Event(BaseModel):
    __tablename__ = "event"

    title: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=False)
    redirect_link: str = Column(String, nullable=False)
    status_id: int = Column(Integer, ForeignKey("status.id"), nullable=False)
    date_id: int = Column(Integer, ForeignKey("date.id"), nullable=False)

    date: Mapped["Date"] = relationship("Date")
    status: Mapped["Status"] = relationship("Status", back_populates="events")

    tracks: Mapped[Optional[List["Track"]]] = relationship("Track", back_populates="event")
    prizes: Mapped[Optional[List["EventPrize"]]] = relationship("EventPrize", back_populates="event")
    locations: Mapped[Optional[List["Location"]]] = relationship("Location", secondary="EventLocation",
                                                                 back_populates="events")
    icons: Mapped[Optional[List["Icon"]]] = relationship("Icon", secondary="EventIconSocial")


class Track(BaseModel):
    __tablename__ = "track"

    title: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=False)
    is_score_based: bool = Column(Boolean, nullable=False, default=False)
    event_id: int = Column(Integer, ForeignKey("event.id"), nullable=False)
    date_id: int = Column(Integer, ForeignKey("date.id"), nullable=False)
    status_id: int = Column(Integer, ForeignKey("status.id"), nullable=False)

    event: Mapped["Event"] = relationship("Event", back_populates="tracks")
    date: Mapped["Date"] = relationship("Date")
    status: Mapped["Status"] = relationship("Status", back_populates="tracks")


class AcceptedTeam(BaseModel):
    __tablename__ = "accepted_team"

    team_id: int = Column(Integer, ForeignKey("team.id"), primary_key=True, nullable=False)
    track_id: int = Column(Integer, ForeignKey("track.id"), primary_key=True, nullable=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)


class TrackWinner(BaseModel):
    __tablename__ = "track_winner"

    track_id: int = Column(Integer, ForeignKey("track.id"), primary_key=True, nullable=False)
    accepted_team_id: int = Column(Integer, ForeignKey("accepted_team.id"), nullable=False)
    place: int = Column(Integer, nullable=False)
    is_awardee: bool = Column(Boolean, nullable=False, default=False)


class EventPrize(BaseModel):
    __tablename__ = "event_prize"

    place: int = Column(Integer, nullable=False)
    primary_prize: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=False)
    icon_id: int = Column(Integer, ForeignKey("icon.id"), nullable=False)
    event_id: int = Column(Integer, ForeignKey("event.id"), nullable=False)

    icon: Mapped["Icon"] = relationship("Icon")
    event: Mapped["Event"] = relationship("Event")


class Location(BaseModel):
    title: str = Column(String, nullable=False, unique=True)

    events: Mapped[Optional[List["Event"]]] = relationship("Event", secondary="EventLocation",
                                                           back_populates="locations")


class EventLocation(ManyToManyBase):
    __tablename__ = "event_location"

    location_id: int = Column(Integer, ForeignKey("location.id"), primary_key=True, nullable=False)
    event_id: int = Column(Integer, ForeignKey("event.id"), nullable=False)


class EventIconSocial(ManyToManyBase):
    __tablename__ = "event_icon_social"

    icon_id: int = Column(Integer, ForeignKey("icon.id"), primary_key=True, nullable=False)
    event_id: int = Column(Integer, ForeignKey("event.id"), nullable=False)


class ActionType(BaseModel):
    __tablename__ = "action_type"

    title: str = Column(String, nullable=False)
    comparator: str = Column(String, nullable=False)
    threshold_value: int = Column(Integer, nullable=False)

    timeline_points: Mapped["TimelinePoint"] = relationship("TimelinePoint", back_populates="action_type")


class TimelinePoint(BaseModel):
    __tablename__ = "timeline_point"

    title: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=False)
    deadline: DateTime = Column(DateTime, nullable=False)
    is_blocking: bool = Column(Boolean, nullable=False, default=False)
    prev_timeline_point_id: int = Column(Integer, ForeignKey("timeline_point.id", ondelete="SET NULL"), nullable=False)
    next_timeline_point_id: int = Column(Integer, ForeignKey("timeline_point.id", ondelete="SET NULL"), nullable=False)
    action_type_id: int = Column(Integer, ForeignKey("action_type.id"), nullable=False)

    prev_timeline_point: Mapped[Optional["TimelinePoint"]] = relationship("TimelinePoint",
                                                                          foreign_keys=[prev_timeline_point_id], )

    next_timeline_point: Mapped[Optional["TimelinePoint"]] = relationship("TimelinePoint",
                                                                          foreign_keys=[next_timeline_point_id], )
    action_type: Mapped["ActionType"] = relationship("ActionType", back_populates="timeline_points")


class Timeline(BaseModel):
    __tablename__ = "timeline"

    track_id: int = Column(Integer, ForeignKey("track.id"), primary_key=True, nullable=False)
    start_timeline_point: int = Column(Integer, ForeignKey("timeline_point.id"), primary_key=True, nullable=False)
