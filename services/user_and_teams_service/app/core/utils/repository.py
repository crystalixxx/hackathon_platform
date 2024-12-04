from abc import ABC, abstractmethod
from hashlib import sha256
from json import dumps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .cache import AbstractCache, RedisCache


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, filter_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_some(self, filter_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update(self, filter_data: dict, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, filter_data: dict):
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

    async def find_one(self, filter_data: dict):
        stmt = select(self.model).filter_by(**filter_data)
        result = await self.session.execute(stmt)

        return result.scalar_one().to_read_model()

    async def find_some(self, filter_data: dict):
        stmt = select(self.model).filter_by(**filter_data)
        result = await self.session.execute(stmt)
        result = [row[0].to_read_model() for row in result]

        return result

    async def update(self, filter_data: dict, data: dict) -> int:
        model_object = await self.find_one(**filter_data)

        for key, value in data.items():
            setattr(model_object, key, value)

        self.session.add(model_object)

        return model_object.id

    async def delete(self, filter_data: dict):
        model_object = await self.find_one(**filter_data)

        await self.session.delete(model_object)

        return model_object.scalar_one().to_read_model()


class CachedRepository(AbstractRepository):
    model = None

    def __init__(self, repository: AbstractRepository, cache: AbstractCache):
        self.repository = repository
        self.repository.model = self.model

        self.cache = cache

    async def __generate_hash(self, method_name: str, params: dict) -> str:
        key = f"{self.repository.__class__.__name__}:{method_name}:{dumps(params, sort_keys=True)}"
        return sha256(key.encode()).hexdigest()

    async def add_one(self, data: dict) -> int:
        result = await self.repository.add_one(data)

        key = await self.__generate_hash("find_all", {})
        await self.cache.delete(key)

        return result

    async def find_all(self):
        key = await self.__generate_hash("find_all", {})
        expected_result = await self.cache.get(key)

        if expected_result is not None:
            return expected_result

        result = await self.repository.find_all()
        if result is not None:
            await self.cache.set(key, result)

        return result

    async def find_one(self, filter_data: dict):
        key = await self.__generate_hash("find_one", filter_data)
        expected_result = await self.cache.get(key)

        if expected_result is not None:
            return expected_result

        result = await self.repository.find_one(filter_data)
        if result is not None:
            await self.cache.set(key, result)

        return result

    async def find_some(self, filter_data: dict):
        key = await self.__generate_hash("find_some", filter_data)
        expected_result = await self.cache.get(key)

        if expected_result is not None:
            return expected_result

        result = await self.repository.find_some(filter_data)
        if result is not None:
            await self.cache.set(key, result)

        return result

    async def update(self, filter_data: dict, data: dict) -> int:
        result = await self.repository.update(filter_data, data)

        key_one = await self.__generate_hash("find_one", filter_data)
        key_many = await self.__generate_hash("find_all", {})

        await self.cache.delete(key_one)
        await self.cache.delete(key_many)

        return result

    async def delete(self, filter_data: dict):
        result = await self.repository.delete(filter_data)

        key_one = await self.__generate_hash("find_one", filter_data)
        key_many = await self.__generate_hash("find_all", {})

        await self.cache.delete(key_one)
        await self.cache.delete(key_many)

        return result
