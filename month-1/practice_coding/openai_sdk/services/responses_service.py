from openai import OpenAI

from config import settings
from schemas.responses import ResponseRequest, ResponseResult, ResponseUsage


def run_response(request: ResponseRequest, client: OpenAI) -> ResponseResult:
    """
    Core logic for the Responses API.

    Design decision: we only pass `instructions` when starting a new conversation
    (no previous_response_id). When continuing, OpenAI already has the instructions
    from the first turn stored internally — re-sending is redundant but harmless.
    We skip it to keep payloads clean and make the stateful nature explicit.
    """
    kwargs: dict = {
        "model": settings.default_model,
        "input": request.message,
        "temperature": request.temperature,
        "max_output_tokens": request.max_output_tokens,
        # store=True is the default — OpenAI retains this response for chaining.
        # Set store=False for one-shot queries where you never need to continue.
        "store": True,
    }

    # if prev_response_id is null whihc thats means this is the new conversation
    # so we will inject instrcution only at the start of the new converstation
    if not request.previous_response_id:
        kwargs["instructions"] = request.instructions

    # This is the entire stateful mechanism and will contain all the previous message as context
    if request.previous_response_id:
        kwargs["previous_response_id"] = request.previous_response_id

    # Why the kwargs: dict pattern instead of hardcoding all params?
    # In production, optional parameters that you conditionally include are best handled by building the dict first, then unpacking by **kwargs.
    # The alternative — passing None values to every optional param — can cause unexpected behavior in some SDK versions (they treat None differently from "not provided").
    response = client.responses.create(**kwargs)

    # we are Extracting cached token count safely by using "getattr()" field may exists or may not exist on all response types
    cached = getattr(response.usage, "input_tokens_details", None)
    cached_tokens = getattr(cached, "cached_tokens", 0) if cached else 0

    return ResponseResult(
        response_id=response.id,
        reply=response.output_text,  # Convenience property — extracts all text output
        status=response.status,
        is_truncated=response.status == "incomplete",
        usage=ResponseUsage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
            cached_tokens=cached_tokens,
        ),
    )
