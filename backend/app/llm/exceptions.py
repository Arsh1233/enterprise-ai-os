"""Exceptions for the LLM package."""


class LLMError(Exception):
    """Base exception for all LLM errors."""

    pass


class LLMGenerationError(LLMError):
    """Raised when the LLM fails to generate a response."""

    pass


class LLMConfigurationError(LLMError):
    """Raised when there is a configuration error with the LLM provider."""

    pass
