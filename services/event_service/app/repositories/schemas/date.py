from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DateBase(BaseModel):
    date_start: datetime
    date_end: datetime

    model_config = ConfigDict(from_attributes=True)


class DateCreate(DateBase):
    pass


class DateUpdate(BaseModel):
    date_start: datetime
    date_end: datetime


class DateSchema(DateBase):
    id: int