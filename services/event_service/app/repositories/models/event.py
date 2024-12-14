from sqlalchemy import Column, String, ForeignKey, Text
from app.database.schemas.event import EventSchema
from . import base


class Event(base.BaseModel):
    __tablename__ = "event"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    redirect_link = Column(String, nullable=True)
    date_id = Column(ForeignKey("date.id", ondelete="CASCADE"), nullable=False)

    def to_read_model(self) -> EventSchema:
        return EventSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            redirect_link=self.redirect_link,
            date_id=self.date_id,
        )

    @classmethod
    def convert_scheme(cls):
        return EventSchema
