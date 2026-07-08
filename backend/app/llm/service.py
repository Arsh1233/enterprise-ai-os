"""LLM service definitions and orchestration."""

from app.llm.base import BaseLLM


class LLMService:
    """Service for interacting with Large Language Models."""

    def __init__(self, provider: BaseLLM) -> None:
        """Initialize the LLM Service.

        Args:
            provider (BaseLLM): The LLM provider to use.
        """
        self._provider = provider

    async def generate(self, prompt: str) -> str:
        """Generate a response from the underlying LLM provider.

        Args:
            prompt (str): The prompt to send to the LLM.

        Returns:
            str: The generated response.
        """
        return await self._provider.generate(prompt)
