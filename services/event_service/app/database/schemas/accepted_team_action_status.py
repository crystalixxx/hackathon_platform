from typing import Optional
from pydantic import BaseModel, ConfigDict
from .track_team import TrackTeamSchema
from .timeline import TimelineSchema


class ActionStatusBase(BaseModel):
    result_value: Optional[str]
    resolution_link: Optional[str]
    completed_at: Optional[str]
    notes: Optional[str]
    track_team: Optional[TrackTeamSchema] = None
    timeline: Optional[TimelineSchema] = None

    model_config = ConfigDict(from_attributes=True)


class ActionStatusCreate(ActionStatusBase):
    pass


class ActionStatusUpdate(BaseModel):
    t_track_team_id: Optional[int]
    t_timeline_id: Optional[int]
    result_value: Optional[str]
    resolution_link: Optional[str]
    completed_at: Optional[str]
    notes: Optional[str]


class AcceptedTeamActionStatusSchema(ActionStatusBase):
    id: int
