from typing import Optional
from pydantic import BaseModel, ConfigDict


class TrackTeamBase(BaseModel):
    track_id: int
    team_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TrackTeamCreate(TrackTeamBase):
    pass


class TrackTeamUpdate(BaseModel):
    track_id: Optional[int]
    team_id: Optional[int]
    is_active: Optional[bool]


class TrackTeamSchema(TrackTeamBase):
    id: int
