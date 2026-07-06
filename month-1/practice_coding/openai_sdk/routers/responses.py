# routers/responses.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from openai import BadRequestError, NotFoundError, OpenAI, RateLimitError

from dependencies import get_openai_client
from schemas.responses import ResponseRequest, ResponseResult
from services.responses_service import run_response

router = APIRouter(prefix="/api/v1", tags=["Responses API From OpenAI"])


@router.post(
    "/responses",
    response_model=ResponseResult,
    summary="Stateful AI conversation (Responses API)",
    description=(
        "Uses OpenAI's Responses API for server-side stateful conversations. "
        "On the first turn, omit previous_response_id. "
        "On subsequent turns, pass the response_id returned from the previous call. "
        "Client only needs to store a single ID — not the full message history."
    ),
)
async def responses_endpoint(
    request: ResponseRequest,
    client: OpenAI = Depends(get_openai_client),
) -> ResponseResult:
    try:
        return run_response(request, client)

    except NotFoundError:
        # This happens when previous_response_id is invalid or expired
        # Responses are retained by OpenAI for a limited period
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "The referenced previous_response_id was not found. "
                "It may have expired or been deleted. Start a new conversation."
            ),
        )
    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="OpenAI rate limit reached. Retry after a moment.",
        )
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {e}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
