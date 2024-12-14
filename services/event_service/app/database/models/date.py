from sqlalchemy import Column, DateTime
from app.database.schemas.date import DateSchema
from . import base


class Date(base.BaseModel):
    __tablename__ = "date"

    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)

    def to_read_model(self) -> DateSchema:
        return DateSchema(
            id=self.id,
            date_start=self.date_start,
            date_end=self.date_end,
        )

    @classmethod
    def convert_scheme(cls):
        return DateSchema
