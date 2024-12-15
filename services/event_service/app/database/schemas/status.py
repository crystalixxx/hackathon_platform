from pydantic import BaseModel, ConfigDict
from typing import Optional


class StatusBase(BaseModel):
    name: str
    text: str

    model_config = ConfigDict(from_attributes=True)


class StatusCreate(StatusBase):
    pass


class StatusUpdate(BaseModel):
    name: Optional[str]
    text: Optional[str]


class StatusSchema(StatusBase):
    id: int


class StatusEventBase(BaseModel):
    event_id: int
    status_id: int


class StatusEventSchema(StatusEventBase):
    pass


class StatusTrackBase(BaseModel):
    event_id: int
    status_id: int


class StatusTrackSchema(StatusTrackBase):
    pass
