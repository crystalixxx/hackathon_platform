from pydantic import BaseModel, ConfigDict


class TrackBase(BaseModel):
    title: str
    description: str
    is_score_based: bool
    event_id: int
    date_id: int

    model_config = ConfigDict(from_attributes=True)


class TrackCreate(TrackBase):
    pass


class TrackUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_score_based: bool | None = None
    event_id: int | None = None
    date_id: int | None = None


class TrackSchema(TrackBase):
    id: int
