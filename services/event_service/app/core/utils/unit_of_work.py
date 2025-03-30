from abc import ABC, abstractmethod

from database.redis import RedisSingleton
from database.session import get_db
from fastapi import Depends
from repositories.event import EventRepository
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import CachingConfig
from core.utils import SQLAlchemyRepository
from core.utils.cache import RedisKeyValueCache
from core.utils.repository import AbstractRepository


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
        self.redis = RedisSingleton.get_instance(str(CachingConfig.url))

    def get_repository(self, repo_class):
        return repo_class(
            repository=SQLAlchemyRepository(self.session),
            cache=RedisKeyValueCache(self.redis),
        )

    async def __aenter__(self):
        self.session: AsyncSession = await anext(self.session_factory())

        self.events = self.get_repository(EventRepository)

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
