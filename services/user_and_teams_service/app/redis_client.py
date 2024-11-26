import redis
import os


class RedisClient:
    def __init__(self):
        self.client = redis.StrictRedis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
        )

    def set(self, key, value, expire=None):
        self.client.set(key, value, ex=expire)

    def get(self, key):
        return self.client.get(key)

    def delete(self, key):
        self.client.delete(key)
