from sqlalchemy import Column, Integer, ForeignKey, Boolean

from . import base


class Request(base):
    __tablename__ = "t_request"

    request_team_id: int = Column(Integer, ForeignKey("t_team.id"), nullable=False)
    user_id: int = Column(Integer, ForeignKey("t_user.id"), nullable=False)
    sent_by_team: bool = Column(Boolean, nullable=False)
    is_ok: bool = Column(Boolean, nullable=False, default=False)
