from pydantic import BaseModel, ConfigDict


class RequestBase(BaseModel):
    request_team_id: int
    sent_by_team: bool
    is_ok: bool

    model_config = ConfigDict(from_attributes=True)


class RequestCreate(RequestBase):
    user_id: int


class RequestSchema(RequestBase):
    id: int
    user_id: int
    request_team_id: int
