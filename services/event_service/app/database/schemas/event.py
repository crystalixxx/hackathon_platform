from typing import Optional
from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    title: str
    description: Optional[str]
    redirect_link: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class EventCreate(EventBase):
    date_id: int


class EventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    redirect_link: Optional[str]
    date_id: Optional[int]


class EventSchema(EventBase):
    id: int
    date_id: int
