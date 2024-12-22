from sqlalchemy import Column, String, Text

from database.schemas.status import StatusSchema

from . import base


class Status(base.BaseModel):
    __tablename__ = "status"

    name = Column(String, nullable=False)
    text = Column(Text, nullable=False)

    def to_read_model(self) -> StatusSchema:
        return StatusSchema(
            id=self.id,
            name=self.name,
            text=self.text,
        )

    @classmethod
    def convert_scheme(cls):
        return StatusSchema
