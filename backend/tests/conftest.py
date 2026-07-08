from typing import Generator

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app


@pytest.fixture(scope="module", autouse=True)
def mock_connections() -> Generator[None, None, None]:
    from app.cache.redis import redis_client
    redis_client.redis = AsyncMock() # type: ignore[assignment]
    with patch("app.core.factory.redis_client.connect", new_callable=AsyncMock), \
         patch("app.core.factory.redis_client.disconnect", new_callable=AsyncMock), \
         patch("sqlalchemy.ext.asyncio.AsyncEngine.dispose", new_callable=AsyncMock):
        yield


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
