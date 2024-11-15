from sqlalchemy import Column, Integer, ForeignKey, Boolean

from app.database.schemas.request import RequestSchema
from . import base


class Request(base.BaseModel):
    __tablename__ = "t_request"

    request_team_id: int = Column(Integer, ForeignKey("t_team.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    sent_by_team: bool = Column(Boolean, nullable=False)
    is_ok: bool = Column(Boolean, nullable=False, default=False)

    def to_read_model(self) -> RequestSchema:
        return RequestSchema(
            id=self.id,
            user_id=self.user_id,
            sent_by_team=self.sent_by_team,
            is_ok=self.is_ok,
        )
