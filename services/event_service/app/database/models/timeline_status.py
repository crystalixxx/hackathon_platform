from sqlalchemy import Column, Integer

from database.schemas.timeline_status import TimelineStatusSchema

from . import base


class TimelineStatus(base.BaseModel):
    __tablename__ = "timeline_status"

    count_num = Column(Integer, nullable=False)

    def to_read_model(self) -> TimelineStatusSchema:
        return TimelineStatusSchema(
            id=self.id,
            count_num=self.count_num,
        )

    @classmethod
    def convert_scheme(cls):
        return TimelineStatusSchema
