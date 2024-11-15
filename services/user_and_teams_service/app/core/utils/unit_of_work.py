from abc import ABC, abstractmethod

from app.core.utils.repositories import AbstractRepository, SQLAlchemyRepository
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractUnitOfWork(ABC):
    batches: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=get_db):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: AsyncSession = self.session_factory()
        self.batches = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
