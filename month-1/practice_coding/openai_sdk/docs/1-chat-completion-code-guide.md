# Great Call — This Changes Everything (For the Better)

This is exactly the right instinct. In a real job, you never build SDK calls in isolation — they always live inside an API. By integrating FastAPI from the start, we'll be building a **real, deployable GenAI backend** that grows with every topic. By Lesson 3.1's end, you'll have a complete, structured FastAPI project that an interviewer or client could actually use.

---

## The Project We're Building Throughout Lesson 3.1

Before rewriting Topic 1, let me show you the **full project structure** we'll assemble topic by topic. Think of this as the architecture diagram of what we're building:

```
openai_service/
├── main.py                    # FastAPI app entry + router registration
├── config.py                  # Pydantic Settings (API keys, model config)
├── dependencies.py            # Shared FastAPI dependencies (OpenAI client)
│
├── routers/
│   ├── chat.py               # Topic 1: Chat Completions endpoint
│   ├── responses.py          # Topic 2: Responses API endpoint
│   ├── streaming.py          # Topic 3: SSE Streaming endpoint
│   ├── tools.py              # Topic 4: Tool Calling endpoint
│   ├── structured.py         # Topic 5: Structured Outputs endpoint
│   └── tokens.py             # Topic 7: Token Counting endpoint
│
├── schemas/
│   ├── chat.py               # Pydantic request/response models (Topic 1)
│   ├── tools.py              # Tool schemas (Topic 4)
│   └── structured.py         # Structured output schemas (Topic 5)
│
└── services/
    ├── chat_service.py       # Core OpenAI logic for chat
    ├── tool_service.py       # Tool execution logic
    └── token_service.py      # Token counting logic
```

**Why this structure?** This is the **separation of concerns** pattern used in production FastAPI apps:
- `routers/` → HTTP layer (handles requests, calls services, returns responses)
- `services/` → Business logic layer (pure Python, no HTTP concerns)
- `schemas/` → Data contracts (Pydantic in/out models)
- `dependencies.py` → Shared resources (DB connections, API clients)

This means your services are **testable without HTTP**, and your routers are thin. This is what separates real engineering from ticket-level coding.

---

# Topic 1 (Rebuilt): Chat Completions API + FastAPI

---

## Step 1 — Project Foundation Files

These files are created **once** and used by every topic going forward.

**`config.py` — Centralized settings with Pydantic:**

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    default_model: str = "gpt-4o"
    default_max_tokens: int = 1000
    default_temperature: float = 0.7

    class Config:
        env_file = ".env"         # reads from .env automatically
        env_file_encoding = "utf-8"

# Singleton — imported everywhere
settings = Settings()
```

**Why `pydantic_settings`?** You already know Pydantic validates data shapes. `BaseSettings` does the same but for *configuration* — it reads from environment variables or `.env` files and validates them. If `OPENAI_API_KEY` is missing, it raises a clear error at startup, not at runtime inside a request. This is production best practice — **fail fast at boot, not during a user request.**

Your `.env` file:
```env
OPENAI_API_KEY=sk-...
DEFAULT_MODEL=gpt-4o
```

---

**`dependencies.py` — The shared OpenAI client:**

```python
# dependencies.py
from openai import OpenAI
from config import settings

# Module-level singleton — created once when the app starts
# FastAPI will inject this into any route that needs it
_openai_client = OpenAI(api_key=settings.openai_api_key)

def get_openai_client() -> OpenAI:
    """
    FastAPI dependency that provides the shared OpenAI client.
    Using a singleton avoids creating a new HTTP client per request.
    """
    return _openai_client
```

**Why a dependency instead of a global import?**

You know FastAPI's `Depends()` system. The benefit here is **testability**. In tests, you can override `get_openai_client` to return a mock client — without touching any business logic. This is the dependency injection pattern — identical to what you've seen in Angular (if you've used it) or NestJS.

```python
# In tests — you can do this:
app.dependency_overrides[get_openai_client] = lambda: MockOpenAIClient()
```

---

**`main.py` — The app entry point (we'll add routers as we go):**

```python
# main.py
from fastapi import FastAPI
from routers import chat  # We'll add more imports as we build more topics

app = FastAPI(
    title="OpenAI Service API",
    description="Production-ready GenAI backend built on OpenAI SDK",
    version="1.0.0"
)

# Register routers — each topic adds one
app.include_router(chat.router, prefix="/api/v1", tags=["Chat Completions"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

## Step 2 — Pydantic Schemas for Topic 1

```python
# schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional, Literal

class Message(BaseModel):
    """
    Represents a single message in a conversation.
    Maps directly to OpenAI's message format.
    """
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    """
    Request body for the chat endpoint.
    This is what the client (React app, Postman, etc.) sends us.
    """
    message: str = Field(..., description="The user's new message", min_length=1)
    system_prompt: Optional[str] = Field(
        default="You are a helpful assistant.",
        description="Instructions that shape the model's behavior"
    )
    conversation_history: Optional[list[Message]] = Field(
        default=[],
        description="Previous messages for multi-turn conversations"
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4096)

class ChatResponse(BaseModel):
    """
    Response body — what we send back to the client.
    Notice we return the updated history — client stores it and sends it next call.
    """
    reply: str
    finish_reason: str
    updated_history: list[Message]
    usage: "TokenUsage"

class TokenUsage(BaseModel):
    """
    Token usage info — critical for cost monitoring in production.
    """
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

# Needed because TokenUsage is referenced before definition
ChatResponse.model_rebuild()
```

**Key design decisions here:**

- `conversation_history` is `Optional[list[Message]]` — the client is responsible for sending it. Stateless API design — we don't store anything.
- `updated_history` in the response — we return the *full updated history* so the client can send it on the next request. This makes the contract explicit.
- `TokenUsage` in every response — in production, you log this and feed it to a cost dashboard. Never throw this data away.
- `Field(ge=0.0, le=2.0)` on temperature — Pydantic validates the range *before* the request reaches your logic. Bad inputs get a 422 automatically.

---

## Step 3 — The Service Layer (Pure Business Logic)

```python
# services/chat_service.py
from openai import OpenAI
from schemas.chat import ChatRequest, ChatResponse, Message, TokenUsage
from config import settings

def run_chat_completion(request: ChatRequest, client: OpenAI) -> ChatResponse:
    """
    Core logic for chat completion.
    No FastAPI here — pure Python. This makes it unit-testable.
    """
    # Build the messages array — exactly as we discussed in the concept section
    messages = [
        {"role": "system", "content": request.system_prompt}
    ]

    # Append conversation history (multi-turn support)
    if request.conversation_history:
        for msg in request.conversation_history:
            messages.append({"role": msg.role, "content": msg.content})

    # Append the new user message
    messages.append({"role": "user", "content": request.message})

    # Call OpenAI
    response = client.chat.completions.create(
        model=settings.default_model,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    assistant_reply = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason

    # Build updated history to return to client
    updated_history = list(request.conversation_history or [])
    updated_history.append(Message(role="user", content=request.message))
    updated_history.append(Message(role="assistant", content=assistant_reply))

    return ChatResponse(
        reply=assistant_reply,
        finish_reason=finish_reason,
        updated_history=updated_history,
        usage=TokenUsage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )
    )
```

**Notice:** No `Request`, no `Response`, no HTTP concepts. This function takes a `ChatRequest` and an `OpenAI` client, and returns a `ChatResponse`. That's it. A junior dev can read this without knowing anything about FastAPI.

---

## Step 4 — The Router (HTTP Layer)

```python
# routers/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAI, BadRequestError, RateLimitError

from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import run_chat_completion
from dependencies import get_openai_client

router = APIRouter()

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the AI",
    description="Stateless chat endpoint. Client manages conversation history."
)
async def chat_endpoint(
    request: ChatRequest,
    client: OpenAI = Depends(get_openai_client)  # Injected — not hardcoded
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
            # In production, you might log this or add a warning header
            # For now, we include it in the response and the client can handle it
            pass

        return result

    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="OpenAI rate limit reached. Please retry after a moment."
        )
    except BadRequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request to OpenAI: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
```

**Why `Depends(get_openai_client)` in the router instead of importing directly?**

The router doesn't *own* the client. It *receives* it. This is the Hollywood Principle — "Don't call us, we'll call you." FastAPI calls your endpoint and *injects* what it needs. In tests, you swap the injection. In production, it's the real client. Zero code changes needed between environments.

---

## Step 5 — What the Full Request/Response Looks Like

**Request (what your React frontend would POST to `/api/v1/chat`):**

```json
{
  "message": "Can you show me a real-world example?",
  "system_prompt": "You are a Python tutor.",
  "conversation_history": [
    {"role": "user", "content": "What is a closure?"},
    {"role": "assistant", "content": "A closure is a function that captures variables from its enclosing scope..."}
  ],
  "temperature": 0.7,
  "max_tokens": 800
}
```

**Response (what goes back to the client):**

```json
{
  "reply": "Here's a real-world closure example — a counter factory...",
  "finish_reason": "stop",
  "updated_history": [
    {"role": "user", "content": "What is a closure?"},
    {"role": "assistant", "content": "A closure is a function that captures variables..."},
    {"role": "user", "content": "Can you show me a real-world example?"},
    {"role": "assistant", "content": "Here's a real-world closure example..."}
  ],
  "usage": {
    "prompt_tokens": 142,
    "completion_tokens": 213,
    "total_tokens": 355
  }
}
```

**The client stores `updated_history` in React state or localStorage and sends it with the next message.** This is how ChatGPT-like multi-turn conversations work under the hood.

---

## Current Project State After Topic 1

```
openai_service/
├── main.py                  ✅ Done
├── config.py                ✅ Done
├── dependencies.py          ✅ Done
├── routers/
│   └── chat.py              ✅ Done
├── schemas/
│   └── chat.py              ✅ Done
└── services/
    └── chat_service.py      ✅ Done
```

The remaining 7 topics will each add new files to this structure — the foundation never changes.

---

## Mini Exercise

Look at the `ChatRequest` schema. Right now, the client can send *any* string as `system_prompt`.

**Think about this:** In a real product where you're building a customer support bot, you wouldn't want clients to override the system prompt — it's set by you, not by them. How would you modify the architecture to handle this? (Hint: think about what should live in the config vs what should come from the client.)

No need to code it — just reason through it. This is the kind of product thinking that separates architects from developers.

---

Ready for **Topic 2: Responses API** whenever you are. Let me know if anything needs clarification first.