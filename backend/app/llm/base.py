"""Base abstractions for LLM integrations."""

import abc


class BaseLLM(abc.ABC):
    """Abstract base class for LLM providers."""

    @abc.abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM based on the given prompt.

        Args:
            prompt (str): The user input prompt.

        Returns:
            str: The LLM's text response.

        Raises:
            LLMGenerationError: If the generation fails.
        """
        pass
