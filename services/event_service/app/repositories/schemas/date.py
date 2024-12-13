from typing import Optional
from pydantic import BaseModel, ConfigDict


class DateBase(BaseModel):
    date_start: str
    date_end: str

    model_config = ConfigDict(from_attributes=True)


class DateCreate(DateBase):
    pass


class DateUpdate(BaseModel):
    date_start: Optional[str]
    date_end: Optional[str]


class DateSchema(DateBase):
    id: int
