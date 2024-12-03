from app.core.redis_client import RedisClient
from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.request import Request


class RequestRepository(SQLAlchemyRepository):
    model = Request

    def __init__(self):
        super().__init__()
        self.redis_client = RedisClient()

    async def get_request_by_id(self, request_id: int):
        cache_key = f"request:{request_id}"
        cached_request = self.redis_client.get(cache_key)

        if cached_request:
            return cached_request

        request = await super().find_one({"id": request_id})

        if request:
            self.redis_client.set(cache_key, request, expire=120)

        return request

    async def delete_request(self, request_id: int):
        request = await super().delete({"id": request_id})

        if request:
            cache_key = f"request:{request_id}"
            self.redis_client.delete(cache_key)

        return request
