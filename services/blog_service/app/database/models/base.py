from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ManyToManyBase(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class BaseModel(ManyToManyBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)