from __future__ import annotations  # see Readme file to see what is forward references

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """
    Represents a single message in a conversation.
    Maps directly to OpenAI's message format.
    """

    role: Role
    content: str


class ChatRequest(BaseModel):
    """
    Request body for the chat endpoint.
    This is what the client (React app, Postman, etc.) sends us.
    """

    message: str = Field(description="The user's new message", min_length=1)
    system_prompt: str | None = Field(
        default="You are a helpful assistant.",
        description="Instructions that shape the model's behavior",
    )
    conversation_history: list[Message] = Field(
        default=list, description="Previous messages for multi-turn conversations"
    )
    temperature: float = Field(default=0.6, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4096)


class ChatResponse(BaseModel):
    """
    Response body — what we send back to the client.
    Notice we return the updated history — client stores it and sends it next call.
    """

    reply: str
    finish_reason: str
    updated_history: list[Message]
    usage: TokenUsage


class TokenUsage(BaseModel):
    """
    Token usage info — critical for cost monitoring in production.
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
