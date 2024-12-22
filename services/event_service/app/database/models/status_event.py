from sqlalchemy import Column, ForeignKey, Integer

from database.schemas.status import StatusEventSchema

from . import base


class StatusEvent(base.BaseModel):
    __tablename__ = "status_event"

    event_id = Column(
        Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False
    )
    status_id = Column(
        Integer, ForeignKey("status.id", ondelete="CASCADE"), nullable=False
    )

    def to_read_model(self) -> StatusEventSchema:
        return StatusEventSchema(
            id=self.id,
            event_id=self.event_id,
            status_id=self.status_id,
        )

    @classmethod
    def convert_scheme(cls):
        return StatusEventSchema
