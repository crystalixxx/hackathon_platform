from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.database.schemas.user import UserSchema


class TeamBase(BaseModel):
    title: str
    description: Optional[str]
    icon_url: Optional[str]
    is_looking_for_members: bool

    model_config = ConfigDict(from_attributes=True)


class TeamCreate(TeamBase):
    captain_id: int


class TeamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    is_looking_for_members: Optional[bool] = None
    captain_id: Optional[int] = None


class TeamSchema(TeamBase):
    id: int
    captain_id: int


class TeamUserSchema(BaseModel):
    id: int
    team_id: int
    user_id: int
    role_name: str
    user: UserSchema

    model_config = ConfigDict(from_attributes=True)
