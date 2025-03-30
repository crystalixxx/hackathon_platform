from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimelineBase(BaseModel):
    title: str
    description: str
    deadline: datetime
    is_blocking: bool
    track_id: int
    timeline_status_id: int

    model_config = ConfigDict(from_attributes=True)


class TimelineCreate(TimelineBase):
    pass


class TimelineUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    deadline: datetime | None = None
    is_blocking: bool | None = None
    track_id: int | None = None
    t_timeline_status_id: int | None = None


class TimelineSchema(TimelineBase):
    id: int
