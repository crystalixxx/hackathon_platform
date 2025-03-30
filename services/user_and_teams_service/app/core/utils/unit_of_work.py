from abc import ABC, abstractmethod

import fakeredis
from app.core.utils import SQLAlchemyRepository
from app.core.utils.cache import RedisCache
from app.core.utils.repository import AbstractRepository
from app.database.session import get_db
from app.repositories import (
    RequestRepository,
    TeamRepository,
    TeamUserRepository,
    UserRepository,
    UserTagRepository,
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


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
        self.redis = fakeredis.FakeAsyncRedis()

    def get_repository(self, repo_class):
        return repo_class(
            repository=SQLAlchemyRepository(self.session), cache=RedisCache(self.redis)
        )

    async def __aenter__(self):
        self.session: AsyncSession = await anext(self.session_factory())

        self.users = self.get_repository(UserRepository)
        self.team = self.get_repository(TeamRepository)
        self.request = self.get_repository(RequestRepository)
        self.user_tags = self.get_repository(UserTagRepository)
        self.team_user = self.get_repository(TeamUserRepository)

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
