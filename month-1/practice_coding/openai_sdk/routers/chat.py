from fastapi import APIRouter, Depends, HTTPException, status
from openai import BadRequestError, OpenAI, RateLimitError

from dependencies import get_openai_client
from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import run_chat_completion

router = APIRouter(prefix="/api/v1", tags=["Chat Completions"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the AI",
    description="Stateless chat endpoint. Client manages conversation history.",
)
async def chat_endpoint(
    request: ChatRequest,
    client: OpenAI = Depends(get_openai_client),  ## Injected — not hardcoded
):
    """
    Chat Completions endpoint.

    The client sends the full conversation history with each request.
    We process it, call OpenAI, and return the updated history.
    The client stores the updated history and sends it next time.
    """
    try:
        result = run_chat_completion(request, client)
        # Production guard: warn if response was truncated

        if result.finish_reason == "length":
            # In production, we might log this or add a warning header
            # For now, we include it in the response and the client can handle it
            pass
        return result

    except RateLimitError:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="OpenAI rate limit reached. Please retry after a moment.",
        )
    except BadRequestError as e:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request to OpenAI: {str(e)}"
        )
    except Exception:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
