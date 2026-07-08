from typing import Dict

import structlog

from app.agents.base import BaseAgent
from app.agents.customer_support import CustomerSupportAgent
from app.agents.exceptions import AgentNotFoundError

logger = structlog.get_logger(__name__)


class AgentRegistry:
    """Registry to manage and retrieve AI agents."""

    def __init__(self) -> None:
        self._agents: Dict[str, BaseAgent] = {}
        # Pre-register default agents
        self.register(CustomerSupportAgent())
        logger.info("AgentRegistry initialized")

    def register(self, agent: BaseAgent) -> None:
        """Register a new agent instance."""
        if agent.name in self._agents:
            logger.warning("Overwriting existing agent", agent_name=agent.name)
        self._agents[agent.name] = agent
        logger.info("Agent registered", agent_name=agent.name)

    def get_agent(self, name: str) -> BaseAgent:
        """Retrieve an agent by name. Raises AgentNotFoundError if not found."""
        agent = self._agents.get(name)
        if not agent:
            logger.error("Agent not found", requested_agent=name)
            raise AgentNotFoundError(f"Agent '{name}' is not registered.")
        return agent
