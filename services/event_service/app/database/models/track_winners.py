from sqlalchemy import Boolean, Column, ForeignKey, Integer

from database.schemas.track_winners import TrackWinnerSchema

from . import base


class TrackWinner(base.BaseModel):
    __tablename__ = "track_winner"

    track_id = Column(
        Integer, ForeignKey("track.id", ondelete="CASCADE"), nullable=False
    )
    t_track_team_id = Column(
        Integer, ForeignKey("track_team.id", ondelete="CASCADE"), nullable=False
    )
    place = Column(Integer, nullable=True)
    is_awardee = Column(Boolean, nullable=True, default=False)

    def to_read_model(self) -> TrackWinnerSchema:
        return TrackWinnerSchema(
            id=self.id,
            track_id=self.track_id,
            t_track_team_id=self.t_track_team_id,
            place=self.place,
            is_awardee=self.is_awardee,
        )

    @classmethod
    def convert_scheme(cls):
        return TrackWinnerSchema
