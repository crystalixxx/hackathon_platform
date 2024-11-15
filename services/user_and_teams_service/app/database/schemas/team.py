from pydantic import BaseModel, ConfigDict
from typing import Optional


class TeamBase(BaseModel):
    title: str
    description: Optional[str]
    icon_link: Optional[str]
    is_looking_for_members: bool

    model_config = ConfigDict(from_attributes=True)


class TeamCreate(TeamBase):
    captain_id: int


class TeamUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    icon_link: Optional[str]
    is_looking_for_members: Optional[bool]
    captain_id: Optional[int]


class TeamSchema(TeamBase):
    id: int
    captain_id: int
