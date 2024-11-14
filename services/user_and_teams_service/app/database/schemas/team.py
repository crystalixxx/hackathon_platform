from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TTeam(BaseModel):
    id: int
    title: str
    description: Optional[str]
    icon_link: Optional[str]
    captain_id: int
    is_looking_for_members: bool = True
    created_at: datetime.datetime.utcnow()
    updated_at: datetime.datetime.utcnow()


class TTeamCreate(BaseModel):
    id: int
    title: str
    captain_id: int
    is_looking_for_members: bool = True
    created_at: datetime.datetime.utcnow()
    updated_at: datetime.datetime.utcnow()


class TTeamUpdate(BaseModel):
    title: str
    description: Optional[str]
    icon_link: Optional[str]
    captain_id: int
    is_looking_for_members: bool
    updated_at: datetime.datetime.utcnow()


class TTeamResponse(BaseModel):
    id: int
    captain_id: int
    created_at: datetime.datetime.utcnow()
    updated_at: datetime.datetime.utcnow()

    model_config = {"from_attributes": True}


class TeamUserBase(BaseModel):
    team_id: int
    user_id: int
    role_name: str


class TeamUserCreate(TeamUserBase):
    pass


class TeamUserResponse(TeamUserBase):
    model_config = {"from_attributes": True}
