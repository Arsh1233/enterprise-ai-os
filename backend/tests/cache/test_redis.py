from unittest.mock import AsyncMock, patch

import pytest

from app.cache.redis import RedisClient


@pytest.mark.asyncio
async def test_redis_ping() -> None:
    client = RedisClient()
    client.redis = AsyncMock()
    client.redis.ping.return_value = True

    result = await client.ping()
    assert result is True


@pytest.mark.asyncio
async def test_redis_connect_disconnect() -> None:
    client = RedisClient()
    with patch("redis.asyncio.from_url") as mock_from_url:
        mock_redis = AsyncMock()
        mock_from_url.return_value = mock_redis

        await client.connect()
        assert client.redis == mock_redis
        mock_redis.ping.assert_called_once()

        await client.disconnect()
        mock_redis.close.assert_called_once()
