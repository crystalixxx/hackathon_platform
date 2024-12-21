from pydantic import AnyUrl, BaseModel, ConfigDict


class EventBase(BaseModel):
    title: str
    description: str
    redirect_link: AnyUrl
    date_id: int

    model_config = ConfigDict(from_attributes=True)


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    redirect_link: AnyUrl | None = None
    date_id: int | None = None


class EventSchema(EventBase):
    id: int
