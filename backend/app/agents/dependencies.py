from fastapi import Depends

from app.agents.registry import AgentRegistry
from app.agents.service import AgentService

# Create a singleton registry instance to hold all agents
_registry = AgentRegistry()


def get_agent_registry() -> AgentRegistry:
    """Dependency to retrieve the singleton AgentRegistry."""
    return _registry


def get_agent_service(
    registry: AgentRegistry = Depends(get_agent_registry),
) -> AgentService:
    """Dependency to retrieve the AgentService."""
    return AgentService(registry=registry)
