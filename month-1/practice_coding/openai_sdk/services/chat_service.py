from openai import OpenAI

from config import settings
from schemas.chat import ChatRequest, ChatResponse, Message, Role, TokenUsage


def run_chat_completion(request: ChatRequest, client: OpenAI) -> ChatResponse:
    """
    Core logic for chat completion.
    No FastAPI here — pure Python. This makes it unit-testable.
    """

    # Build the messages array
    messages = [{"role": Role.SYSTEM, "content": request.system_prompt}]

    # Append conversation history (multi-turn support)
    if request.conversation_history:
        for msg in request.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": Role.USER, "content": request.message})

    response = client.chat.completions.create(
        model=settings.default_model,
        messages=messages,
        temperature=settings.default_temprature,
        max_tokens=settings.default_max_tokens,
    )

    assistant_reply = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    # Build updated history to return to client
    updated_history = list(request.conversation_history or [])
    updated_history.append(Message(role=Role.USER, content=request.message))
    updated_history.append(Message(role=Role.ASSISTANT, content=assistant_reply))

    return ChatResponse(
        reply=assistant_reply,
        finish_reason=finish_reason,
        updated_history=updated_history,
        usage=TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        ),
    )
