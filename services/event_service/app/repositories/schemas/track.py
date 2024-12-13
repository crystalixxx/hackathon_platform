from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class TrackBase(BaseModel):
    title: str
    description: Optional[str]
    is_score_based: bool

    model_config = ConfigDict(from_attributes=True)


class TrackCreate(TrackBase):
    event_id: int
    date_id: int


class TrackUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_score_based: Optional[bool]
    event_id: Optional[int]
    date_id: Optional[int]


class TrackSchema(TrackBase):
    id: int
    event_id: int
    date_id: int
