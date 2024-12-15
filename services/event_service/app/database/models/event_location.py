from sqlalchemy import Column, ForeignKey, Integer
from app.database.schemas.event_location import EventLocationSchema
from . import base


class EventLocation(base.BaseModel):
    __tablename__ = "event_location"

    event_id = Column(Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("location.id", ondelete="CASCADE"), nullable=False)

    def to_read_model(self) -> EventLocationSchema:
        return EventLocationSchema(
            id=self.id,
            event_id=self.event_id,
            location_id=self.location_id,
        )

    @classmethod
    def convert_scheme(cls):
        return EventLocationSchema
