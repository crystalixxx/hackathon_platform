from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from database.schemas.accepted_team_action_status import AcceptedTeamActionStatusSchema

from . import base


class AcceptedTeamActionStatus(base.BaseModel):
    __tablename__ = "accepted_team_action_status"

    t_track_team_id = Column(
        Integer, ForeignKey("t_track_team.id", ondelete="CASCADE"), nullable=False
    )
    t_timeline_id = Column(
        Integer, ForeignKey("t_timeline.id", ondelete="CASCADE"), nullable=False
    )
    result_value = Column(String, nullable=True)
    resolution_link = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    def to_read_model(self) -> AcceptedTeamActionStatusSchema:
        return AcceptedTeamActionStatusSchema(
            id=self.id,
            t_track_team_id=self.t_track_team_id,
            t_timeline_id=self.t_timeline_id,
            result_value=self.result_value,
            resolution_link=self.resolution_link,
            completed_at=self.completed_at,
            notes=self.notes,
        )

    @classmethod
    def convert_scheme(cls):
        return AcceptedTeamActionStatusSchema
