from typing import Optional
from pydantic import BaseModel, ConfigDict


class TimelineBase(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[str]
    is_blocking: bool

    model_config = ConfigDict(from_attributes=True)


class TimelineCreate(TimelineBase):
    track_id: int
    t_timeline_status_id: int


class TimelineUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[str]
    is_blocking: Optional[bool]
    track_id: Optional[int]
    t_timeline_status_id: Optional[int]


class TimelineSchema(TimelineBase):
    id: int
    track_id: int
    t_timeline_status_id: int
