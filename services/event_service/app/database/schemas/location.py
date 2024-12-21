from pydantic import BaseModel, ConfigDict


class LocationBase(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    title: str | None = None


class LocationSchema(LocationBase):
    id: int
