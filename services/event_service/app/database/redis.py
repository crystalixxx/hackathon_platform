from redis.asyncio import Redis


class RedisSingleton:
    __instance: Redis | None = None

    @classmethod
    def get_instance(cls, redis_url: str) -> Redis:
        if cls.__instance is None:
            cls.__instance = Redis.from_url(redis_url)

        return cls.__instance

    @classmethod
    async def delete_instance(cls):
        if cls.__instance is not None:
            await cls.__instance.close()
            cls.__instance = None
