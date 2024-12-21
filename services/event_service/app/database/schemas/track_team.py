from pydantic import BaseModel, ConfigDict


class TrackTeamBase(BaseModel):
    track_id: int
    team_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TrackTeamCreate(TrackTeamBase):
    pass


class TrackTeamUpdate(BaseModel):
    track_id: int | None = None
    team_id: int | None = None
    is_active: bool | None = None


class TrackTeamSchema(TrackTeamBase):
    id: int
