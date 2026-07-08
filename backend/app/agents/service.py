import time

import structlog

from app.agents.exceptions import AgentExecutionError
from app.agents.registry import AgentRegistry
from app.agents.schemas import AgentRequest, AgentResponse

logger = structlog.get_logger(__name__)


class AgentService:
    """Service layer to manage AI agent execution."""

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    async def execute_agent(self, request: AgentRequest) -> AgentResponse:
        """Execute the requested agent and return the formatted response."""
        start_time = time.perf_counter()

        # This will raise AgentNotFoundError if the agent does not exist
        agent = self.registry.get_agent(request.agent_name)

        logger.info(
            "Executing agent",
            agent_name=request.agent_name,
            prompt_preview=request.prompt[:50],
        )

        try:
            # Execute the agent logic
            result = await agent.execute(request.prompt)
        except Exception as e:
            logger.error(
                "Agent execution encountered an error",
                agent_name=request.agent_name,
                error=str(e),
            )
            # Re-raise as Domain exception if it isn't already one
            if isinstance(e, AgentExecutionError):
                raise
            raise AgentExecutionError(
                f"Internal error executing {request.agent_name}: {e}"
            )

        execution_time_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Agent executed successfully",
            agent_name=request.agent_name,
            execution_time_ms=execution_time_ms,
        )

        return AgentResponse(result=result, execution_time_ms=execution_time_ms)
