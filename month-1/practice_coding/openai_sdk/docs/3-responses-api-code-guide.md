# Topic 2: Responses API — OpenAI's New Stateful Engine

---

## ⚠️ Topic 1 Code Corrections First

Before anything new, here are the fixes I owe you from Topic 1. These apply to every file we built:

**`config.py` — Inner `class Config` is Pydantic v1 legacy. Modern Pydantic v2 uses `model_config`:**
```python
# ❌ Old (Pydantic v1 style — still works but deprecated in v2)
class Config:
    env_file = ".env"

# ✅ Modern (Pydantic v2)
from pydantic import ConfigDict
model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")
```

**`schemas/chat.py` — Remove `ChatResponse.model_rebuild()` and modernize types:**
```python
# ❌ Old — workaround for forward references
ChatResponse.model_rebuild()

# ✅ Modern — add this at the top of the file instead
from __future__ import annotations
# Forward references now resolve lazily — model_rebuild() not needed
```
Also replace `Optional[str]` → `str | None` and `Optional[list[Message]]` → `list[Message] | None` throughout.

I'll show complete corrected files at the end of this topic in the project summary. For now, let's go deep on Topic 2.

---

## Prerequisites / Required Packages

```bash
# Everything from Topic 1 is already installed.
# No new packages needed for the Responses API itself.
# The openai SDK already includes Responses API support.

# Verify your SDK version is recent enough (>= 1.66.0 for full Responses API support)
uv add "openai>=1.66.0"
```

---

## The Big Picture — Why Did OpenAI Build This?

To understand the Responses API, you first need to understand the **problem it solves** — because that problem is directly tied to money, developer pain, and the shift toward agentic AI.

Think about your experience from Topic 1. Every time a user sends a message, you:
1. Collect the entire conversation history from wherever you stored it
2. Serialize it into a `messages[]` array
3. Send **the entire thing** to OpenAI on every single call
4. Pay for **all of those tokens** every single time

In a short conversation that's fine. But imagine a support agent that's been talking for 30 messages, or an AI coding assistant with a 50-file codebase in context. That full history payload grows linearly. Your token costs grow linearly. Your latency grows. Your complexity of managing and truncating history grows.

**The Assistants API (2023) was OpenAI's first attempt to solve this.** OpenAI would store the thread server-side. You'd just say "continue thread `thread_abc123`." But the Assistants API was overly complex — Assistants, Threads, Runs, Steps, Polling — it took 5–10 API calls to do what Chat Completions does in 1. Developers hated it. It got deprecated.

**The Responses API (2025) is the mature second attempt.** It takes the simplicity of Chat Completions but adds server-side state through one elegant mechanism: `previous_response_id`. That's it. One field. OpenAI stores the conversation on their end. You just pass the ID of the last response and they know exactly where the conversation is.

---

## The Core Architectural Shift: Stateless vs Stateful

This is the most important concept in this entire topic. Let me map it to something you already know from your web background.

**Topic 1 (Chat Completions) is like JWT auth:**
- Stateless by design
- *You* store everything (the conversation history) on your side
- Every request is self-contained — it carries all the information needed
- Full control, full responsibility

**Topic 2 (Responses API) is like session-based auth:**
- Stateful by design
- *The server* (OpenAI) stores the conversation state
- Your request just carries a session ID (`previous_response_id`)
- Less control, less responsibility, potential vendor lock-in

Neither is universally better. This is an engineering tradeoff decision you'll make per feature. Here's the decision matrix you'll use in the real world:

| Situation | Use |
|---|---|
| Simple Q&A, single-turn queries | Chat Completions |
| Full control over context window management | Chat Completions |
| Multi-provider (switching between OpenAI/Anthropic) | Chat Completions |
| Multi-turn stateful conversations, reduced complexity | Responses API |
| Agentic workflows with built-in tools (web search, file search) | Responses API |
| MCP server integrations | Responses API |
| You want OpenAI to handle token management | Responses API |

---

## Concept Mapping: Assistants API → Responses API

Since the Assistants API sunsets **August 26, 2026**, you need to understand the migration mentally. You'll see legacy codebases using Assistants. Here's the direct mapping:

```
Assistants API                     Responses API
─────────────────────────────────────────────────────────────
Assistant (instructions, model)  → instructions + model param
Thread (conversation container)  → previous_response_id chain
Run (execution of the thread)    → client.responses.create()
Run Steps (tool call loop)       → output items in response
Polling (wait for completion)    → Gone — synchronous by default
5-10 API calls per turn          → 1 API call per turn
```

The Assistants API required you to create an Assistant object, create a Thread, add a Message to the Thread, create a Run, then poll the Run until it completed. The Responses API collapses all of that into a single call.

---

## The Responses API in Detail

Let me walk you through what changes at the API level compared to Chat Completions:

**Key parameter differences:**

| Chat Completions | Responses API | Note |
|---|---|---|
| `messages=[...]` | `input="..."` | Input is simpler — string or list |
| `messages[0].role == "system"` | `instructions="..."` | System prompt is a top-level param |
| N/A | `previous_response_id` | The stateful chaining mechanism |
| `max_tokens` | `max_output_tokens` | **Renamed — easy to miss** |
| N/A | `store=True/False` | Controls whether OpenAI stores the response |

**Key response object differences:**

| Chat Completions | Responses API | Note |
|---|---|---|
| `response.choices[0].message.content` | `response.output_text` | Much cleaner extraction |
| `response.choices[0].finish_reason` | `response.status` | "completed", "incomplete", "failed" |
| `usage.prompt_tokens` | `usage.input_tokens` | **Renamed** |
| `usage.completion_tokens` | `usage.output_tokens` | **Renamed** |
| No ID for chaining | `response.id` | This is your "session token" |

These renames are subtle but will cause production bugs if you mix them up. The test is simple: if you try to access `.prompt_tokens` on a Responses API response, you get `None` — no error, just silent wrong data.

---

## How the Stateful Chain Works

Here's the flow of a multi-turn conversation visually:

```
Turn 1:
  Client → POST /api/v1/responses
           { message: "What is async/await?", previous_response_id: null }
  
  OpenAI → Creates response, stores [user: "What is async/await?"] internally
  
  Server → Returns { response_id: "resp_abc123", reply: "Async/await is..." }

Turn 2:
  Client → POST /api/v1/responses
           { message: "Show me an example", previous_response_id: "resp_abc123" }
  
  OpenAI → Looks up "resp_abc123", retrieves full history internally,
            appends new user message, generates reply
  
  Server → Returns { response_id: "resp_def456", reply: "Here's an example..." }

Turn 3:
  Client → POST /api/v1/responses
           { message: "What about error handling?", previous_response_id: "resp_def456" }
  ...
```

The client only stores one string — the latest `response_id`. OpenAI handles everything else. Each response ID points to a node in a linked list that OpenAI maintains internally.

**The production implication you need to internalize:** If OpenAI's storage has an outage or they delete old responses (they have a retention policy), your conversation chain breaks. This is the vendor lock-in risk. For critical applications, you might still want to store conversation history on your side *in addition to* using the Responses API — using it for convenience but keeping your own record for resilience.

---

## Building the Code

**Step 1 — `schemas/responses.py`:**

```python
# schemas/responses.py
from __future__ import annotations

from pydantic import BaseModel, Field


class ResponseRequest(BaseModel):
    """
    Request body for the Responses API endpoint.

    The key difference from ChatRequest: instead of sending full conversation
    history, the client only needs to send the previous_response_id.
    OpenAI manages the rest server-side.
    """
    message: str = Field(..., min_length=1, description="The user's new message")
    instructions: str | None = Field(
        default="You are a helpful assistant.",
        description="System-level instructions. Only needed on the first turn — "
                    "OpenAI carries it forward automatically via previous_response_id."
    )
    previous_response_id: str | None = Field(
        default=None,
        description="Pass the response_id from the previous turn to continue a conversation. "
                    "Omit or set to null to start a new conversation."
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
```

---

**Step 2 — `services/responses_service.py`:**

```python
# services/responses_service.py
from __future__ import annotations

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

    # Only inject instructions at the start of a new conversation
    if not request.previous_response_id:
        kwargs["instructions"] = request.instructions

    # This is the entire stateful mechanism — one field
    if request.previous_response_id:
        kwargs["previous_response_id"] = request.previous_response_id

    response = client.responses.create(**kwargs)

    # Extract cached token count safely — field may not exist on all response types
    cached = getattr(response.usage, "input_tokens_details", None)
    cached_tokens = getattr(cached, "cached_tokens", 0) if cached else 0

    return ResponseResult(
        response_id=response.id,
        reply=response.output_text,   # Convenience property — extracts all text output
        status=response.status,
        is_truncated=response.status == "incomplete",
        usage=ResponseUsage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
            cached_tokens=cached_tokens,
        ),
    )
```

**Why the `kwargs: dict` pattern instead of hardcoding all params?**

In production, optional parameters that you conditionally include are best handled by building the dict first, then unpacking. The alternative — passing `None` values to every optional param — can cause unexpected behavior in some SDK versions (they treat `None` differently from "not provided"). Explicit is better than implicit.

---

**Step 3 — `routers/responses.py`:**

```python
# routers/responses.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from openai import BadRequestError, NotFoundError, OpenAI, RateLimitError

from dependencies import get_openai_client
from schemas.responses import ResponseRequest, ResponseResult
from services.responses_service import run_response

router = APIRouter()


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
```

**Notice the `NotFoundError` handler** — this is unique to the Responses API and doesn't exist in Chat Completions. If a client stores a `response_id` and comes back days later (after OpenAI's retention window expires), you get a 404. Your frontend needs to handle this by starting a fresh conversation. This is a real edge case you'll hit in production.

---

**Step 4 — Update `main.py`:**

```python
# main.py
from __future__ import annotations

from fastapi import FastAPI

from routers import chat, responses  # ← add responses

app = FastAPI(
    title="OpenAI Service API",
    description="Production-ready GenAI backend built on OpenAI SDK",
    version="1.0.0",
)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat Completions"])
app.include_router(responses.router, prefix="/api/v1", tags=["Responses API"])  # ← new


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "ok"}
```

---

**Step 5 — Corrected `config.py` (fixing Topic 1 issue):**

```python
# config.py
from __future__ import annotations

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(          # ← Pydantic v2 — not inner class Config
        env_file=".env",
        env_file_encoding="utf-8",
    )

    openai_api_key: str
    default_model: str = "gpt-4o"
    default_max_tokens: int = 1000
    default_temperature: float = 0.7


settings = Settings()
```

---

**Step 6 — Corrected `schemas/chat.py` (fixing Topic 1 issues):**

```python
# schemas/chat.py
from __future__ import annotations   # ← replaces the need for model_rebuild()

from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The user's new message")
    system_prompt: str | None = Field(   # ← str | None instead of Optional[str]
        default="You are a helpful assistant.",
    )
    conversation_history: list[Message] | None = Field(default=None)  # ← modernized
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4096)


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    reply: str
    finish_reason: str
    updated_history: list[Message]
    usage: TokenUsage
    # ← No model_rebuild() needed — from __future__ import annotations handles it
```

---

## What the API Looks Like End to End

**Turn 1 — Starting a conversation:**

```json
// POST /api/v1/responses
{
  "message": "What is dependency injection and why does it matter?",
  "instructions": "You are a senior software architect. Be concise and use real-world examples.",
  "previous_response_id": null
}

// Response
{
  "response_id": "resp_68a1b2c3d4e5f6",
  "reply": "Dependency injection is a pattern where...",
  "status": "completed",
  "is_truncated": false,
  "usage": {
    "input_tokens": 42,
    "output_tokens": 186,
    "total_tokens": 228,
    "cached_tokens": 0
  }
}
```

**Turn 2 — Continuing without sending history:**

```json
// POST /api/v1/responses
{
  "message": "How does FastAPI implement it?",
  "previous_response_id": "resp_68a1b2c3d4e5f6"
}
// No instructions needed — OpenAI already has them from Turn 1

// Response
{
  "response_id": "resp_79b2c3d4e5f6a7",
  "reply": "FastAPI uses the Depends() decorator...",
  "status": "completed",
  "is_truncated": false,
  "usage": {
    "input_tokens": 248,
    "output_tokens": 203,
    "total_tokens": 451,
    "cached_tokens": 186
  }
}
```

Notice `cached_tokens: 186` in Turn 2 — OpenAI is already caching the previous response content. This previews Topic 8 (Prompt Caching) — you're getting cost savings automatically just by using the Responses API.

---

## Updated Project State After Topic 2

```
openai_service/
├── main.py                    ✅ Updated (responses router added)
├── config.py                  ✅ Fixed (Pydantic v2 model_config)
├── dependencies.py            ✅ No changes needed
│
├── routers/
│   ├── chat.py                ✅ No changes needed
│   └── responses.py           ✅ New
│
├── schemas/
│   ├── chat.py                ✅ Fixed (from __future__, str | None)
│   └── responses.py           ✅ New
│
└── services/
    ├── chat_service.py        ✅ No changes needed
    └── responses_service.py   ✅ New
```

---

## The Architectural Question Worth Sitting With

Here's a real product decision you'd face as a GenAI architect — not a coding question, a system design question:

You're building a customer support AI for a SaaS product. Users can come back days later to continue a conversation. You're choosing between:

**Option A:** Chat Completions + store history in your PostgreSQL DB  
**Option B:** Responses API + store only `response_id` in your DB

Think about: resilience, cost, vendor lock-in, data sovereignty (what if your enterprise client requires all data on-premises?), and what happens when OpenAI expires a response after 30 days.

There's no single right answer — but the fact that you can reason through these tradeoffs is what makes you an architect vs a developer who just ships tickets. What's your instinct?

---

Ready for **Topic 3: Streaming via Server-Sent Events** when you are. That one's where things get genuinely exciting from a frontend perspective — you'll finally understand how ChatGPT's typewriter effect works and how to pipe it through your FastAPI backend to a React client.