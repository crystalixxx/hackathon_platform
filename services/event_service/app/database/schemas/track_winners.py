from typing import Optional
from pydantic import BaseModel, ConfigDict


class TrackWinnerBase(BaseModel):
    track_id: int
    t_track_team_id: int
    place: Optional[int]
    is_awardee: Optional[bool]

    model_config = ConfigDict(from_attributes=True)


class TrackWinnerCreate(TrackWinnerBase):
    pass


class TrackWinnerUpdate(BaseModel):
    track_id: Optional[int]
    t_track_team_id: Optional[int]
    place: Optional[int]
    is_awardee: Optional[bool]


class TrackWinnerSchema(TrackWinnerBase):
    id: int
