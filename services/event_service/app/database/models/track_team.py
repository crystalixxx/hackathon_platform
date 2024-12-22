from sqlalchemy import Boolean, Column, ForeignKey, Integer

from database.schemas.track_team import TrackTeamSchema

from . import base


class TrackTeam(base.BaseModel):
    __tablename__ = "track_team"

    track_id = Column(
        Integer, ForeignKey("track.id", ondelete="CASCADE"), nullable=False
    )
    team_id = Column(Integer, ForeignKey("team.id", ondelete="CASCADE"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    def to_read_model(self) -> TrackTeamSchema:
        return TrackTeamSchema(
            id=self.id,
            track_id=self.track_id,
            team_id=self.team_id,
            is_active=self.is_active,
        )

    @classmethod
    def convert_scheme(cls):
        return TrackTeamSchema
