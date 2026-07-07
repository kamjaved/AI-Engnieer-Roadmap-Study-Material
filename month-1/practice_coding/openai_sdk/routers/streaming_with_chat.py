# routers/streaming.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

from dependencies import get_async_openai_client
from schemas.streaming_with_chat import StreamChatRequest
from services.streaming_with_chat_service import (
    stream_chat_completion,
    stream_chat_completion_plain_text,
)

router = APIRouter(prefix="/api/v1", tags=["Stream From Chat Completion"])


@router.post(
    "/chat/stream",
    summary="Streaming chat via Server-Sent Events",
    description="Streams the assistant's reply token-by-token using SSE.",
)
async def stream_chat_endpoint(
    request: StreamChatRequest, client: AsyncOpenAI = Depends(get_async_openai_client)
) -> StreamingResponse:
    return StreamingResponse(
        stream_chat_completion(request, client),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # Disables buffering on nginx reverse proxies — CRITICAL in production.
            # Without this header, nginx buffers the whole response before sending
            # it to the client, completely defeating the purpose of streaming.
            "X-Accel-Buffering": "no",
        },
    )


@router.post(
    "/chat/stream/plain",
    summary="Streaming chat as plain text",
    description="Streams token chunks as text/plain for API clients like Postman.",
)
async def stream_chat_plain_endpoint(
    request: StreamChatRequest, client: AsyncOpenAI = Depends(get_async_openai_client)
) -> StreamingResponse:
    return StreamingResponse(
        stream_chat_completion_plain_text(request, client),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
