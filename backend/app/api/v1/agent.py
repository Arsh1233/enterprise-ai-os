import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.dependencies import get_agent_service
from app.agents.exceptions import AgentExecutionError, AgentNotFoundError
from app.agents.schemas import AgentRequest, AgentResponse
from app.agents.service import AgentService

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post("/run", response_model=AgentResponse, status_code=status.HTTP_200_OK)
async def run_agent(
    request: AgentRequest, agent_service: AgentService = Depends(get_agent_service)
) -> AgentResponse:
    """
    Execute an AI agent using Google ADK.
    """
    try:
        return await agent_service.execute_agent(request)
    except AgentNotFoundError as e:
        logger.warning("Agent not found", error=str(e), agent_name=request.agent_name)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AgentExecutionError as e:
        logger.error(
            "Agent execution error", error=str(e), agent_name=request.agent_name
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent execution failed. Please try again later.",
        )
    except Exception as e:
        logger.exception("Unexpected error in agent execution", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
