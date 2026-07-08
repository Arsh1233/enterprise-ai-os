from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    agent_name: str = Field(
        ..., description="The name of the agent to invoke (e.g. customer_support)"
    )
    prompt: str = Field(..., description="The user prompt or instruction to execute")


class AgentResponse(BaseModel):
    result: str = Field(..., description="The text response from the agent")
    execution_time_ms: float = Field(..., description="Execution time in milliseconds")
