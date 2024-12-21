from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict


class ActionStatusBase(BaseModel):
    track_team_id: int
    timeline_id: int
    result_value: str | None = None
    resolution_link: str | None = None
    completed_at: datetime | None = datetime.now(timezone.utc)
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ActionStatusCreate(ActionStatusBase):
    pass


class ActionStatusUpdate(BaseModel):
    t_track_team_id: int | None = None
    t_timeline_id: int | None = None
    result_value: str | None = None
    resolution_link: str | None = None
    completed_at: str | None = None
    notes: str | None = None


class AcceptedTeamActionStatusSchema(ActionStatusBase):
    id: int
