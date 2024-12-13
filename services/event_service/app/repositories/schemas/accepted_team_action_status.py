from typing import Optional
from pydantic import BaseModel, ConfigDict


class AcceptedTeamActionStatusBase(BaseModel):
    t_track_team_id: int
    t_timeline_id: int
    result_value: Optional[str]
    resolution_link: Optional[str]
    completed_at: Optional[str]
    notes: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class AcceptedTeamActionStatusCreate(AcceptedTeamActionStatusBase):
    pass


class AcceptedTeamActionStatusUpdate(BaseModel):
    t_track_team_id: Optional[int]
    t_timeline_id: Optional[int]
    result_value: Optional[str]
    resolution_link: Optional[str]
    completed_at: Optional[str]
    notes: Optional[str]


class AcceptedTeamActionStatusSchema(AcceptedTeamActionStatusBase):
    id: int
