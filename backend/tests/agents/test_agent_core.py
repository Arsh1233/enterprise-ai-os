from unittest.mock import patch

import pytest

from app.agents.base import BaseAgent
from app.agents.customer_support import CustomerSupportAgent
from app.agents.exceptions import AgentExecutionError, AgentNotFoundError
from app.agents.registry import AgentRegistry
from app.agents.schemas import AgentRequest
from app.agents.service import AgentService


@pytest.mark.asyncio
async def test_customer_support_agent_execute() -> None:
    agent = CustomerSupportAgent()
    assert agent.name == "customer_support"

    with patch("app.agents.customer_support.settings.GOOGLE_API_KEY", ""):
        result = await agent.execute("Hello")
        assert "[Customer Support]" in result

    with patch("app.agents.customer_support.settings.GOOGLE_API_KEY", "dummy_key"):
        result = await agent.execute("Hello")
        assert "Processed by ADK Agent" in result


@pytest.mark.asyncio
async def test_customer_support_agent_error() -> None:
    agent = CustomerSupportAgent()
    with (
        patch("app.agents.customer_support.settings.GOOGLE_API_KEY", ""),
        patch(
            "app.agents.customer_support.logger.warning",
            side_effect=Exception("mock error"),
        ),
    ):
        with pytest.raises(AgentExecutionError):
            await agent.execute("Test")


def test_agent_registry() -> None:
    registry = AgentRegistry()
    agent = registry.get_agent("customer_support")
    assert isinstance(agent, CustomerSupportAgent)

    with pytest.raises(AgentNotFoundError):
        registry.get_agent("unknown_agent")

    # test registration
    class DummyAgent(BaseAgent):
        def __init__(self) -> None:
            super().__init__(name="dummy", instruction="dummy")

        async def execute(self, prompt: str) -> str:
            return "dummy"

    registry.register(DummyAgent())
    assert registry.get_agent("dummy").name == "dummy"


@pytest.mark.asyncio
async def test_agent_service() -> None:
    registry = AgentRegistry()
    service = AgentService(registry)

    request = AgentRequest(agent_name="customer_support", prompt="Help me")
    response = await service.execute_agent(request)
    assert response.result is not None
    assert response.execution_time_ms > 0

    request_unknown = AgentRequest(agent_name="unknown", prompt="Help")
    with pytest.raises(AgentNotFoundError):
        await service.execute_agent(request_unknown)


@pytest.mark.asyncio
async def test_agent_service_execution_error() -> None:
    registry = AgentRegistry()

    class FailingAgent(BaseAgent):
        def __init__(self) -> None:
            super().__init__(name="failing", instruction="fail")

        async def execute(self, prompt: str) -> str:
            raise ValueError("Test value error")

    registry.register(FailingAgent())
    service = AgentService(registry)

    request = AgentRequest(agent_name="failing", prompt="Fail")
    with pytest.raises(AgentExecutionError) as exc_info:
        await service.execute_agent(request)
    assert "Internal error executing failing" in str(exc_info.value)

    # Test when AgentExecutionError is raised directly
    class AgentExecutionFailingAgent(BaseAgent):
        def __init__(self) -> None:
            super().__init__(name="failing2", instruction="fail")

        async def execute(self, prompt: str) -> str:
            raise AgentExecutionError("Direct error")

    registry.register(AgentExecutionFailingAgent())
    with pytest.raises(AgentExecutionError) as exc_info:
        await service.execute_agent(AgentRequest(agent_name="failing2", prompt="Fail"))
    assert str(exc_info.value) == "Direct error"
