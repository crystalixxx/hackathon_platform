from pydantic import BaseModel
from typing import Optional


class TeamBase(BaseModel):
    title: str
    description: Optional[str]
    icon_link: Optional[str]
    is_looking_for_members: bool

    class Config:
        from_attributes = True


class TeamCreateSchema(TeamBase):
    captain_id: int


class TeamUpdateSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    icon_link: Optional[str]
    is_looking_for_members: Optional[bool]
    captain_id: Optional[int]

    class Config:
        from_attributes = True


class TeamSchema(TeamBase):
    id: int
    captain_id: int

    class Config:
        from_attributes = True
