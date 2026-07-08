from unittest.mock import patch

from fastapi.testclient import TestClient


def test_agent_run_endpoint(client: TestClient) -> None:
    payload = {
        "agent_name": "customer_support",
        "prompt": "How do I reset my password?",
    }
    response = client.post("/api/v1/agent/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "execution_time_ms" in data


def test_agent_run_endpoint_not_found(client: TestClient) -> None:
    payload = {"agent_name": "invalid_agent", "prompt": "Hello"}
    response = client.post("/api/v1/agent/run", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Agent 'invalid_agent' is not registered."


def test_agent_run_endpoint_execution_error(client: TestClient) -> None:
    payload = {"agent_name": "customer_support", "prompt": "Hello"}

    with patch(
        "app.agents.service.AgentService.execute_agent",
        side_effect=Exception("Unexpected"),
    ):
        response = client.post("/api/v1/agent/run", json=payload)
        assert response.status_code == 500
        assert "unexpected error" in response.json()["detail"].lower()

    from app.agents.exceptions import AgentExecutionError

    with patch(
        "app.agents.service.AgentService.execute_agent",
        side_effect=AgentExecutionError("Failed"),
    ):
        response = client.post("/api/v1/agent/run", json=payload)
        assert response.status_code == 500
        assert "agent execution failed" in response.json()["detail"].lower()
