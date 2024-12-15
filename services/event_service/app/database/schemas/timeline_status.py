from pydantic import BaseModel, ConfigDict


class TimelineStatusBase(BaseModel):
    count_num: int

    model_config = ConfigDict(from_attributes=True)


class TimelineStatusSchema(TimelineStatusBase):
    id: int
