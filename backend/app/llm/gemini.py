"""Gemini LLM implementation."""

import structlog
from google import genai
from google.genai.errors import APIError

from app.config.settings import settings
from app.llm.base import BaseLLM
from app.llm.exceptions import LLMConfigurationError, LLMGenerationError

logger = structlog.get_logger(__name__)


class GeminiLLM(BaseLLM):
    """LLM provider implementation for Google Gemini."""

    def __init__(self) -> None:
        """Initialize the Gemini Provider."""
        super().__init__()
        if not settings.GEMINI_API_KEY:
            raise LLMConfigurationError(
                "GEMINI_API_KEY environment variable is not configured."
            )

        try:
            self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self._model = settings.GEMINI_MODEL
            logger.info("GeminiLLM initialized", model=self._model)
        except Exception as e:
            raise LLMConfigurationError(f"Failed to initialize Gemini Client: {e}")

    async def generate(self, prompt: str) -> str:
        """Generate a response using Gemini.

        Args:
            prompt (str): The user input prompt.

        Returns:
            str: The LLM's text response.

        Raises:
            LLMGenerationError: If generation fails or returns an empty response.
        """
        logger.debug("Generating response from Gemini", prompt_length=len(prompt))
        try:
            response = await self._client.aio.models.generate_content(
                model=self._model, contents=prompt
            )
            text = response.text
            if not text:
                raise LLMGenerationError("Gemini returned an empty response.")
            return text
        except APIError as e:
            logger.error("Gemini API Error", error=str(e))
            raise LLMGenerationError(f"API Error from Gemini: {e}")
        except Exception as e:
            if isinstance(e, LLMGenerationError):
                raise
            logger.error("Unexpected error during Gemini generation", error=str(e))
            raise LLMGenerationError(f"Unexpected error: {e}")
