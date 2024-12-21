from pydantic import BaseModel, ConfigDict


class TrackWinnerBase(BaseModel):
    track_id: int
    track_team_id: int
    place: int
    is_awardee: bool

    model_config = ConfigDict(from_attributes=True)


class TrackWinnerCreate(TrackWinnerBase):
    pass


class TrackWinnerUpdate(BaseModel):
    track_id: int | None = None
    t_track_team_id: int | None = None
    place: int | None = None
    is_awardee: bool | None = None


class TrackWinnerSchema(TrackWinnerBase):
    id: int
