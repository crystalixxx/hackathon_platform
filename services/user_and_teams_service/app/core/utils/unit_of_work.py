from abc import ABC, abstractmethod

from app.core.utils.repository import AbstractRepository
from app.database.session import get_db
from app.repositories import (
    RequestRepository,
    TeamRepository,
    TeamUserRepository,
    UserRepository,
    UserTagRepository,
)
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


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=get_db):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = await self.session_factory()

        self.user = UserRepository(self.session)
        self.team = TeamRepository(self.session)
        self.request = RequestRepository(self.session)
        self.user_tags = UserTagRepository(self.session)
        self.team_user = TeamUserRepository(self.session)

        return super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
