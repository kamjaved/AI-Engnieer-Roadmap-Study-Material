from __future__ import annotations

from pydantic import BaseModel, Field


class ResponseRequest(BaseModel):
    """
    Request body for the Responses API endpoint.

    The key difference from ChatRequest: instead of sending full conversation
    history, the client only needs to send the previous_response_id.
    OpenAI manages the rest server-side.
    """

    message: str = Field(min_length=2, description="The User's new Message")
    instructions: str | None = Field(
        default="You're a helpful assistant and you have to asnwer users question in Natural Form",
        description="System-level instructions. Only needed on the first turn — "
        "OpenAI carries it forward automatically via previous_response_id.",
    )
    previous_response_id: str | None = Field(
        default=None,
        description="Pass the response_id from the previous turn to continue a conversation. "
        "Omit or set to null to start a new conversation.",
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_output_tokens: int = Field(default=1000, ge=1, le=4096)


class ResponseUsage(BaseModel):
    """
    Note the naming: input_tokens / output_tokens — NOT prompt_tokens / completion_tokens.
    Responses API uses different field names than Chat Completions API.
    Mixing these up causes silent None values in production — a common bug.
    """

    input_tokens: int
    output_tokens: int
    total_tokens: int
    # Prompt caching fields — available when cache is hit (covered in Topic 8)
    cached_tokens: int = 0


class ResponseResult(BaseModel):
    """
    The response returned to the client.
    response_id is the critical field — the client stores this and sends it
    as previous_response_id in the next request to continue the conversation.
    Think of it as a lightweight session token.
    """

    response_id: str
    reply: str
    status: str  # "completed" | "incomplete" | "failed"
    is_truncated: bool  # True when status == "incomplete" (hit max_output_tokens)
    usage: ResponseUsage
