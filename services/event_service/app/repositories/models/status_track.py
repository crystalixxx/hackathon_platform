from sqlalchemy import Column, Integer, ForeignKey
from app.database.schemas.status_track import StatusTrackSchema
from . import base


class StatusTrack(base.BaseModel):
    __tablename__ = "status_track"

    event_id = Column(Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id", ondelete="CASCADE"), nullable=False)

    def to_read_model(self) -> StatusTrackSchema:
        return StatusTrackSchema(
            id=self.id,
            event_id=self.event_id,
            status_id=self.status_id,
        )

    @classmethod
    def convert_scheme(cls):
        return StatusTrackSchema
