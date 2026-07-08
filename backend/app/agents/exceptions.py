class AgentError(Exception):
    """Base exception for all agent-related errors."""

    pass


class AgentNotFoundError(AgentError):
    """Raised when an unknown agent is requested."""

    pass


class AgentExecutionError(AgentError):
    """Raised when an agent encounters an error during execution."""

    pass
