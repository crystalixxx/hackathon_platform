from typing import Optional
from pydantic import BaseModel, ConfigDict


class EventPrizeBase(BaseModel):
    place: int
    primary_prize: str
    description: Optional[str]
    icon_url: Optional[str]
    event_id: int

    model_config = ConfigDict(from_attributes=True)


class EventPrizeCreate(EventPrizeBase):
    pass


class EventPrizeUpdate(BaseModel):
    place: Optional[int]
    primary_prize: Optional[str]
    description: Optional[str]
    icon_url: Optional[str]
    event_id: Optional[int]


class EventPrizeSchema(EventPrizeBase):
    id: int
