from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "project_name" in data
    assert "description" in data
    assert "docs_url" in data
    assert "redoc_url" in data
    assert "version" in data


def test_health_endpoint(client: TestClient) -> None:
    # Mocking DB and Redis checks for CI
    with patch(
        "app.api.v1.health.AsyncSession.execute", new_callable=AsyncMock
    ) as mock_db:
        with patch(
            "app.api.v1.health.redis.Redis.ping", new_callable=AsyncMock
        ) as mock_redis:
            mock_db.return_value = True
            mock_redis.return_value = True

            response = client.get("/api/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["database"] == "up"
            assert data["redis"] == "up"
            assert "service" in data
            assert "uptime" in data
            assert "timestamp" in data
            assert "version" in data
            assert "environment" in data


def test_health_endpoint_unhealthy(client: TestClient) -> None:
    from app.cache.redis import redis_client

    with patch(
        "app.api.v1.health.AsyncSession.execute", new_callable=AsyncMock
    ) as mock_db:
        # redis_client.redis is already an AsyncMock from conftest
        redis_client.redis.ping.side_effect = Exception("Redis Down")  # type: ignore
        mock_db.side_effect = Exception("DB Down")

        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "down"
        assert data["redis"] == "down"

        # Reset side_effect for other tests if necessary
        redis_client.redis.ping.side_effect = None  # type: ignore


def test_version_endpoint(client: TestClient) -> None:
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    data = response.json()
    assert "application_version" in data
    assert "python_version" in data
    assert "api_version" in data
    assert "environment" in data
