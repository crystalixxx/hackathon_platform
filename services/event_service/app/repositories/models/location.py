from sqlalchemy import Column, String
from app.database.schemas.location import LocationSchema
from . import base


class Location(base.BaseModel):
    __tablename__ = "location"

    title = Column(String, nullable=False)

    def to_read_model(self) -> LocationSchema:
        return LocationSchema(
            id=self.id,
            title=self.title,
        )

    @classmethod
    def convert_scheme(cls):
        return LocationSchema
