from abc import ABC, abstractmethod

import structlog
from google.adk import Agent

from app.config.settings import settings

logger = structlog.get_logger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all AI agents using Google ADK."""

    def __init__(self, name: str, instruction: str):
        self.name = name
        self.instruction = instruction

        # Initialize Google ADK Agent
        self._adk_agent = Agent(
            name=self.name,
            model=settings.GEMINI_MODEL,
            instruction=self.instruction,
        )
        logger.info(f"Initialized agent: {self.name}", model=settings.GEMINI_MODEL)

    @abstractmethod
    async def execute(self, prompt: str) -> str:
        """
        Execute the agent with a given prompt.
        Subclasses must implement this method.
        """
        pass
