from pydantic import BaseModel, ConfigDict


class TimelineStatusBase(BaseModel):
    count_num: int

    model_config = ConfigDict(from_attributes=True)


class TimelineStatusCreate(TimelineStatusBase):
    pass


class TimelineStatusUpdate(BaseModel):
    count_num: int | None = None


class TimelineStatusSchema(TimelineStatusBase):
    id: int
