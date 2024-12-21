from pydantic import BaseModel, ConfigDict


class EventLocationSchema(BaseModel):
    event_id: int
    location_id: int

    model_config = ConfigDict(from_attributes=True)
