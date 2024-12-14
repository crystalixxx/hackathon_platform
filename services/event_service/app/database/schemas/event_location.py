from typing import Optional
from pydantic import BaseModel, ConfigDict
from .location import LocationSchema
from .event import EventSchema


class EventLocationBase(BaseModel):
    event: Optional[EventSchema] = None
    location: Optional[LocationSchema] = None

    model_config = ConfigDict(from_attributes=True)


class EventLocationSchema(EventLocationBase):
    pass
