from sqlalchemy import Column, ForeignKey, Integer, String, Text

from database.schemas.event_prize import EventPrizeSchema

from . import base


class EventPrize(base.BaseModel):
    __tablename__ = "event_prize"

    place = Column(Integer, nullable=False)
    primary_prize = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String, nullable=True)
    event_id = Column(
        Integer, ForeignKey("event.id", ondelete="CASCADE"), nullable=False
    )

    def to_read_model(self) -> EventPrizeSchema:
        return EventPrizeSchema(
            id=self.id,
            place=self.place,
            primary_prize=self.primary_prize,
            description=self.description,
            icon_url=self.icon_url,
            event_id=self.event_id,
        )

    @classmethod
    def convert_scheme(cls):
        return EventPrizeSchema
