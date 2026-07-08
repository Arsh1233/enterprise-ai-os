from typing import Optional

import redis.asyncio as redis

from app.config.settings import settings
from app.logging.logger import get_logger

logger = get_logger("redis")


class RedisClient:
    def __init__(self) -> None:
        self.redis: Optional[redis.Redis] = None

    async def connect(self) -> None:
        self.redis = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        await self.ping()
        logger.info("redis_connected", url=settings.redis_url)

    async def ping(self) -> bool:
        if not self.redis:
            return False
        return await self.redis.ping()

    async def disconnect(self) -> None:
        if self.redis:
            await self.redis.close()
            logger.info("redis_disconnected")


redis_client = RedisClient()
