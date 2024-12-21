from pydantic import BaseModel, ConfigDict


class EventPrizeBase(BaseModel):
    place: int
    primary_prize: str
    description: str
    icon_url: str
    event_id: int

    model_config = ConfigDict(from_attributes=True)


class EventPrizeCreate(EventPrizeBase):
    pass


class EventPrizeUpdate(BaseModel):
    place: int | None = None
    primary_prize: str | None = None
    description: str | None = None
    icon_url: str | None = None
    event_id: int | None = None


class EventPrizeSchema(EventPrizeBase):
    id: int
