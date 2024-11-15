from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update(self, row_id: int, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, row_id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        response = self.model(**data)
        self.session.add(response)

        return response.id

    async def find_all(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        result = [row[0].to_read_model() for row in result]

        return result


    async def find_one(self, data: dict):
        stmt = select(self.model).filter_by(**data)
        result = await self.session.execute(stmt)

        return result.scalar_one().to_read_model()


    async def update(self, row_id: int, data: dict) -> int:
        model_object = await self.find_one({"id": row_id})

        for key, value in data.items():
            setattr(model_object, key, value)

        self.session.add(model_object)

        return model_object.id


    async def delete(self, row_id: int):
        model_object = await self.find_one({"id": row_id})

        await self.session.delete(model_object)

        return model_object.scalar_one().to_read_model()
