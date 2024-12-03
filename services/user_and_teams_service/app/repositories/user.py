from app.core.redis_client import RedisClient
from app.core.utils.repository import SQLAlchemyRepository
from app.database.models.user import User


class UserRepository(SQLAlchemyRepository):
    model = User

    def __init__(self):
        super().__init__()
        self.redis_client = RedisClient()

    # async def create_user(self, user_dict: dict):
    # user = await super().add_one(user_dict)
    # return user

    # async def get_users(self):
    # users = await super().find_all()
    # return users

    async def get_user_by_id(self, user_id: int):
        cache_key = f"user:{user_id}"
        cached_user = self.redis_client.get(cache_key)

        if cached_user:
            return cached_user

        user = await super().find_one({"id": user_id})

        if user:
            self.redis_client.set(cache_key, user, expire=120)

        return user

    # async def get_user_by_email(self, email: str):
    # user = await super().find_one({"email": email})
    # return user

    async def update_user(self, user_id: int, update_dict: dict):
        user = await super().update({"id": user_id}, update_dict)

        if user:
            cache_key = f"user:{user_id}"
            self.redis_client.delete(cache_key)

        return user

    async def delete_user(self, user_id: int):
        user = await super().delete({"id": user_id})

        if user:
            cache_key = f"user:{user_id}"
            self.redis_client.delete(cache_key)

        return user
