from pydantic import BaseModel


class RequestBase(BaseModel):
    user_id: int
    sent_by_team: bool
    is_ok: bool

    class Config:
        from_attributes = True


class RequestCreateSchema(RequestBase):
    request_team_id: int


class RequestSchema(RequestBase):
    id: int
    request_team_id: int

    class Config:
        from_attributes = True
