from abc import ABC, abstractmethod
from json import dumps, loads

from redis.asyncio import Redis


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: any, ttl: int = 3600):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError


class RedisCache(AbstractCache):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str):
        json_value = await self.redis.get(key)

        if json_value is None:
            return None

        return loads(json_value)

    async def set(self, key: str, value: any, ttl: int = 3600):
        await self.redis.set(key, dumps(value), ex=ttl)

    async def delete(self, key: str):
        await self.redis.delete(key)
