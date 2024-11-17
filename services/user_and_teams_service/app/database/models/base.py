from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ManyToManyBase(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class BaseModel(ManyToManyBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
