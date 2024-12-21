from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.core.utils import SQLAlchemyRepository
from app.core.utils.cache import RedisCache
from app.core.utils.repository import AbstractRepository
from app.database.redis import RedisSingleton
from app.database.session import get_db
from app.repositories import (
    AcceptedRepository,
    DateRepository,
    EventRepository,
    EventLocationRepository,
    EventPrizeRepository,
    LocationRepository,
    StatusRepository,
    StatusEventRepository,
    StatusTrackRepository,
    TimelineRepository,
    TimelineStatusRepository,
    TrackRepository,
    TrackTeamRepository,
    TrackWinnersRepository
)


class AbstractUnitOfWork(ABC):
    batches: AbstractRepository

    @abstractmethod
    def __init__(self, session_factory):
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class CachedSQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory=Depends(get_db),
    ):
        self.session_factory = session_factory
        self.redis = RedisSingleton.get_instance(config.redis_connection_url)

    def get_repository(self, repo_class):
        return repo_class(
            repository=SQLAlchemyRepository(self.session), cache=RedisCache(self.redis)
        )

    async def __aenter__(self):
        self.session: AsyncSession = await anext(self.session_factory())

        self.accepted_team = self.get_repository(AcceptedRepository)
        self.date = self.get_repository(DateRepository)
        self.event = self.get_repository(EventRepository)
        self.event_location = self.get_repository(EventLocationRepository)
        self.event_prize = self.get_repository(EventPrizeRepository)
        self.location = self.get_repository(LocationRepository)
        self.status = self.get_repository(StatusRepository)
        self.status_event = self.get_repository(StatusEventRepository)
        self.status_track = self.get_repository(StatusTrackRepository)
        self.timeline = self.get_repository(TimelineRepository)
        self.timeline_status = self.get_repository(TimelineStatusRepository)
        self.track = self.get_repository(TrackRepository)
        self.track_team = self.get_repository(TrackTeamRepository)
        self.track_winners = self.get_repository(TrackWinnersRepository)

        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self.session:
                await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
