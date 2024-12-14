from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey
from app.database.schemas.track import TrackSchema
from . import base


class Track(base.BaseModel):
    __tablename__ = "track"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_score_based = Column(Boolean, nullable=False, default=False)
    event_id = Column(Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False)
    date_id = Column(Integer, ForeignKey("date.id", ondelete="CASCADE"), nullable=False)

    def to_read_model(self) -> TrackSchema:
        return TrackSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            is_score_based=self.is_score_based,
            event_id=self.event_id,
            date_id=self.date_id,
        )

    @classmethod
    def convert_scheme(cls):
        return TrackSchema
