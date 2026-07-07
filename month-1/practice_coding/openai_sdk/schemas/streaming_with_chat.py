# schemas/streaming.py
from __future__ import annotations

from pydantic import BaseModel, Field

from schemas.chat import Message


class StreamChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    system_prompt: str | None = Field(default="You are a helpful assistant.")
    conversation_history: list[Message] = Field(default_factory=list)
