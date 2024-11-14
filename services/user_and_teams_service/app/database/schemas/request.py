from pydantic import BaseModel


class TRequestBase(BaseModel):
    request_team_id: int
    user_id: int
    sent_by_team: bool
    is_ok: bool


class TRequestCreate(TRequestBase):
    request_team_id: int


class TRequestResponse(TRequestBase):
    id: int
    request_team_id: int

    model_config = {"from_attributes": True}
