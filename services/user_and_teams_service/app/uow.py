from redis_client import RedisClient
from fastapi import HTTPException


class RedisUnitOfWork:
    def __init__(self):
        try:
            self.redis = RedisClient()
        except Exception:
            raise HTTPException(
                status_code=500, detail="не удалось подключиться к redis"
            )

    def __enter__(self):
        print("запуск uow")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise HTTPException(status_code=500, detail="ошибка работы с redis")
        print("завершение uow")

    def cache_data(self, key, value, expire=None):
        try:
            self.redis.set(key, value, expire)
        except Exception:
            raise HTTPException(
                status_code=500, detail="не удалось записать данные в redis"
            )

    def fetch_data(self, key):
        try:
            data = self.redis.get(key)
            if data is None:
                raise HTTPException(status_code=404, detail="ключ не найден в redis")
            return data
        except Exception:
            raise HTTPException(
                status_code=500, detail="не удалось получить данные из redis"
            )

    def clear_cache(self, key):
        try:
            result = self.redis.delete(key)
            if not result:
                raise HTTPException(status_code=404, detail="ключ не найден в redis")
        except Exception:
            raise HTTPException(
                status_code=500, detail="не удалось удалить данные из redis"
            )
