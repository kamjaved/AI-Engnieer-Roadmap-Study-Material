# services/streaming_service.py
from __future__ import annotations

import json
from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from config import settings
from schemas.streaming_with_chat import StreamChatRequest


def _build_messages(request: StreamChatRequest) -> list[dict[str, str | None]]:
    messages = [{"role": "system", "content": request.system_prompt}]
    if request.conversation_history:
        for item in request.conversation_history:
            messages.append({"role": item.role.value, "content": item.content})

    messages.append({"role": "user", "content": request.message})
    return messages


async def stream_chat_completion(
    request: StreamChatRequest, client: AsyncOpenAI
) -> AsyncGenerator[str]:
    """
    Yields Server-Sent Event formatted strings, one per token delta.

    SSE wire format is strict: each event MUST be:
        data: <payload>\n\n
    The double newline is what tells the browser "this event is complete."
    Missing it means the client will buffer forever waiting for more.
    """
    messages = _build_messages(request)

    stream = await client.chat.completions.create(
        model=settings.default_model,
        messages=messages,
        stream=True,
        # By default, streaming responses do not include token usage.
        # If you need cost tracking we have to use this  flag,
        stream_options={"include_usage": True},
    )

    async for chunk in stream:
        if not chunk.choices:
            # This is the special final usage-only chunk when include_usage=True.
            if chunk.usage:
                usage_payload = {
                    "type": "usage",
                    "input_tokens": chunk.usage.prompt_tokens,
                    "output_tokens": chunk.usage.completion_tokens,
                }
                yield f"data: {json.dumps(usage_payload)}\n\n"
            continue

        delta = chunk.choices[0].delta.content
        if delta:
            payload = {"type": "token", "content": delta}
            yield f"data: {json.dumps(payload)}\n\n"

        finish_reason = chunk.choices[0].finish_reason
        if finish_reason:
            payload = {"type": "done", "finish_reason": finish_reason}
            yield f"data: {json.dumps(payload)}\n\n"
    # SSE convention: signal true stream termination to the client
    yield "data: [DONE]\n\n"

    # Why JSON-wrap every event instead of sending raw text?
    # Because in a real app, you need to distinguish "this is a text token" from "this is usage info" from "this is a tool call event" (later).
    # A typed envelope ({"type": "token", ...}) is the production pattern — it lets your frontend switch on type instead of guessing from raw string shape.
    # This is the same reasoning behind match event.type above — typed messages over a stream, not ambiguous raw strings.


async def stream_chat_completion_plain_text(
    request: StreamChatRequest, client: AsyncOpenAI
) -> AsyncGenerator[str]:
    """
    Yields raw token text chunks for clients like Postman that do not render SSE nicely.
    """
    messages = _build_messages(request)

    stream = await client.chat.completions.create(
        model=settings.default_model,
        messages=messages,
        stream=True,
    )

    async for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
