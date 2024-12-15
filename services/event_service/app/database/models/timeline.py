from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from app.database.schemas.timeline import TimelineSchema
from . import base


class Timeline(base.BaseModel):
    __tablename__ = "timeline"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    is_blocking = Column(Boolean, nullable=False, default=False)
    track_id = Column(Integer, ForeignKey("track.id", ondelete="CASCADE"), nullable=False)
    t_timeline_status_id = Column(Integer, ForeignKey("timeline_status.id", ondelete="SET NULL"), nullable=True)

    def to_read_model(self) -> TimelineSchema:
        return TimelineSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            deadline=self.deadline,
            is_blocking=self.is_blocking,
            track_id=self.track_id,
            t_timeline_status_id=self.t_timeline_status_id,
        )

    @classmethod
    def convert_scheme(cls):
        return TimelineSchema
