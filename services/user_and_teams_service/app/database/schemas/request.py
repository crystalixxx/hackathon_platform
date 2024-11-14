from pydantic import BaseModel


class RequestBase(BaseModel):
    request_team_id: int
    sent_by_team: bool
    is_ok: bool

    class Config:
        from_attributes = True


class RequestCreateSchema(RequestBase):
    user_id: int


class RequestSchema(RequestBase):
    id: int
    user_id: int
