from pydantic import BaseModel, ConfigDict


class EventLocationBase(BaseModel):
    event_id: int
    location_id: int

    model_config = ConfigDict(from_attributes=True)


class EventLocationSchema(EventLocationBase):
    pass
