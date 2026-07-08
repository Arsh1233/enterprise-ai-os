from typing import AsyncGenerator

import redis.asyncio as redis

from app.cache.redis import redis_client


async def get_redis() -> AsyncGenerator[redis.Redis, None]:  # type: ignore[type-arg]
    if not redis_client.redis:
        raise RuntimeError("Redis is not initialized")
    yield redis_client.redis
