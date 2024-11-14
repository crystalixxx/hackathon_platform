import uuid
from pydantic import BaseModel


class TRequestBase(BaseModel):
    request_team_id: uuid.UUID
    user_id: uuid.UUID
    sent_by_team: bool
    is_ok: bool


class TRequestCreate(TRequestBase):
    request_team_id: uuid.UUID


class TRequestResponse(TRequestBase):
    id: uuid.UUID
    request_team_id: uuid.UUID

    model_config = {"from_attributes": True}
