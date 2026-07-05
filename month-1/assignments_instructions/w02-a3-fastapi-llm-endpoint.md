# Assignment 2.3: FastAPI LLM Endpoint

> **Week 2** | [Back to Week 2 Plan](../week-2.md)

## Title
**FastAPI LLM Endpoint** -- Your First AI Backend

## Objective
Build a production-ready FastAPI application that serves as a backend for an LLM-powered chat application. It includes a standard chat endpoint, a Server-Sent Events (SSE) streaming endpoint, Pydantic request/response models, CORS configured for a React frontend, basic rate limiting, and a health check. This is the Python equivalent of building an Express.js API -- but for AI.

## Difficulty
Intermediate

## Estimated Time
3-4 hours

## Prerequisites
- Python 3.10+ installed
- Completed Assignment 2.2 (Pydantic models)
- Basic REST API concepts (you know this from Node.js/Express)
- Install dependencies:
```bash
pip install fastapi uvicorn[standard] openai anthropic python-dotenv sse-starlette pydantic-settings slowapi
```
- **Required**: At least one LLM API key (OpenAI or Anthropic). If you have neither, you will implement a mock provider.

## Why This Matters
As a React developer, you have built many frontends that call APIs. Now you are building the AI-powered API itself. FastAPI is the dominant Python framework for AI backends because:
- It is async-native (handles many concurrent LLM API calls)
- It uses Pydantic for automatic request validation and OpenAPI docs
- It supports SSE streaming out of the box
- It auto-generates Swagger/OpenAPI docs (you get a free API playground)

This is the exact stack used at most AI startups.

---

## Detailed Instructions

### Step 1: Project Setup (10 min)

```
fastapi-llm-endpoint/
  app/
    __init__.py
    main.py
    config.py
    models/
      __init__.py
      requests.py
      responses.py
    routes/
      __init__.py
      chat.py
      health.py
    services/
      __init__.py
      llm_service.py
      rate_limiter.py
    middleware/
      __init__.py
      cors.py
      logging.py
  tests/
    __init__.py
    test_chat.py
    test_health.py
  .env.example
  pyproject.toml
```

Create `.env.example`:
```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_PROVIDER=openai
MAX_REQUESTS_PER_MINUTE=20
LOG_LEVEL=INFO
```

### Step 2: Configuration with Pydantic Settings (10 min)

In `app/config.py`:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Defaults
    default_model: str = "gpt-4o-mini"
    default_provider: str = "openai"
    max_tokens_default: int = 1024
    temperature_default: float = 0.7

    # Rate Limiting
    max_requests_per_minute: int = 20

    # App
    app_name: str = "LLM Chat API"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    allowed_origins: list[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def has_openai(self) -> bool:
        return self.openai_api_key is not None

    @property
    def has_anthropic(self) -> bool:
        return self.anthropic_api_key is not None


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Step 3: Request/Response Models (20 min)

In `app/models/requests.py`:

```python
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    role: Role
    content: str = Field(..., min_length=1, max_length=100_000)


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""
    messages: list[Message] = Field(
        ..., min_length=1, max_length=50,
        description="Conversation history"
    )
    model: str | None = Field(
        None, description="Model to use (defaults to server config)"
    )
    provider: str | None = Field(
        None, description="Provider: 'openai' or 'anthropic'"
    )
    temperature: float = Field(
        0.7, ge=0.0, le=2.0,
        description="Sampling temperature"
    )
    max_tokens: int = Field(
        1024, ge=1, le=4096,
        description="Maximum tokens to generate"
    )
    stream: bool = Field(
        False, description="Whether to stream the response"
    )

    @field_validator("messages")
    @classmethod
    def must_have_user_message(cls, v: list[Message]) -> list[Message]:
        if not any(m.role == Role.USER for m in v):
            raise ValueError("At least one user message is required")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {"role": "user", "content": "Hello, how are you?"}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 256
                }
            ]
        }
    }
```

In `app/models/responses.py`:

```python
from pydantic import BaseModel, Field
from datetime import datetime


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @property
    def estimated_cost(self) -> float:
        """Rough cost estimate (update with real pricing)."""
        return (self.prompt_tokens * 0.15 + self.completion_tokens * 0.60) / 1_000_000


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""
    id: str = Field(..., description="Unique response ID")
    content: str = Field(..., description="Generated text")
    model: str = Field(..., description="Model used")
    provider: str = Field(..., description="Provider used")
    usage: Usage
    created_at: datetime = Field(default_factory=datetime.utcnow)
    finish_reason: str = Field("stop", description="Why generation stopped")


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    providers: dict[str, bool] = Field(
        description="Available providers and their status"
    )
    uptime_seconds: float


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: list[dict] | None = None
    request_id: str | None = None
```

### Step 4: LLM Service Layer (40 min)

In `app/services/llm_service.py`, build a provider-agnostic service:

```python
import uuid
from typing import AsyncIterator
from app.config import get_settings
from app.models.requests import ChatRequest, Message, Role
from app.models.responses import ChatResponse, Usage


class LLMService:
    """Unified interface for calling LLM providers."""

    def __init__(self):
        self.settings = get_settings()
        self._openai_client = None
        self._anthropic_client = None

    @property
    def openai_client(self):
        if self._openai_client is None and self.settings.has_openai:
            from openai import AsyncOpenAI
            self._openai_client = AsyncOpenAI(
                api_key=self.settings.openai_api_key
            )
        return self._openai_client

    @property
    def anthropic_client(self):
        if self._anthropic_client is None and self.settings.has_anthropic:
            import anthropic
            self._anthropic_client = anthropic.AsyncAnthropic(
                api_key=self.settings.anthropic_api_key
            )
        return self._anthropic_client

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a chat request to the appropriate provider."""
        provider = request.provider or self.settings.default_provider
        model = request.model or self.settings.default_model

        if provider == "openai":
            return await self._call_openai(request, model)
        elif provider == "anthropic":
            return await self._call_anthropic(request, model)
        elif provider == "mock":
            return await self._call_mock(request, model)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def chat_stream(
        self, request: ChatRequest
    ) -> AsyncIterator[str]:
        """Stream a chat response as SSE data."""
        provider = request.provider or self.settings.default_provider
        model = request.model or self.settings.default_model

        if provider == "openai":
            async for chunk in self._stream_openai(request, model):
                yield chunk
        elif provider == "anthropic":
            async for chunk in self._stream_anthropic(request, model):
                yield chunk
        elif provider == "mock":
            async for chunk in self._stream_mock(request, model):
                yield chunk
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def _call_openai(
        self, request: ChatRequest, model: str
    ) -> ChatResponse:
        messages = [
            {"role": m.role.value, "content": m.content}
            for m in request.messages
        ]
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        choice = response.choices[0]
        return ChatResponse(
            id=response.id,
            content=choice.message.content or "",
            model=model,
            provider="openai",
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            finish_reason=choice.finish_reason or "stop",
        )

    async def _call_anthropic(
        self, request: ChatRequest, model: str
    ) -> ChatResponse:
        # Anthropic separates system messages
        system_msg = ""
        messages = []
        for m in request.messages:
            if m.role == Role.SYSTEM:
                system_msg += m.content + "\n"
            else:
                messages.append(
                    {"role": m.role.value, "content": m.content}
                )

        response = await self.anthropic_client.messages.create(
            model=model or "claude-3-haiku-20240307",
            max_tokens=request.max_tokens,
            system=system_msg.strip() or None,
            messages=messages,
            temperature=request.temperature,
        )
        return ChatResponse(
            id=response.id,
            content=response.content[0].text,
            model=model,
            provider="anthropic",
            usage=Usage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=(
                    response.usage.input_tokens
                    + response.usage.output_tokens
                ),
            ),
            finish_reason=response.stop_reason or "stop",
        )

    async def _stream_openai(
        self, request: ChatRequest, model: str
    ) -> AsyncIterator[str]:
        import json
        messages = [
            {"role": m.role.value, "content": m.content}
            for m in request.messages
        ]
        stream = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                data = {
                    "content": chunk.choices[0].delta.content,
                    "finish_reason": chunk.choices[0].finish_reason,
                }
                yield f"data: {json.dumps(data)}\n\n"
        yield "data: [DONE]\n\n"

    async def _stream_anthropic(
        self, request: ChatRequest, model: str
    ) -> AsyncIterator[str]:
        import json
        system_msg = ""
        messages = []
        for m in request.messages:
            if m.role == Role.SYSTEM:
                system_msg += m.content + "\n"
            else:
                messages.append(
                    {"role": m.role.value, "content": m.content}
                )

        async with self.anthropic_client.messages.stream(
            model=model or "claude-3-haiku-20240307",
            max_tokens=request.max_tokens,
            system=system_msg.strip() or None,
            messages=messages,
            temperature=request.temperature,
        ) as stream:
            async for text in stream.text_stream:
                data = {"content": text, "finish_reason": None}
                yield f"data: {json.dumps(data)}\n\n"
        yield "data: [DONE]\n\n"

    async def _call_mock(
        self, request: ChatRequest, model: str
    ) -> ChatResponse:
        """Mock provider for testing without API keys."""
        import asyncio
        await asyncio.sleep(0.5)  # Simulate latency
        user_msg = next(
            m.content for m in reversed(request.messages)
            if m.role == Role.USER
        )
        return ChatResponse(
            id=f"mock-{uuid.uuid4().hex[:8]}",
            content=f"This is a mock response to: '{user_msg[:50]}'. "
                    f"Configure a real provider (openai/anthropic) "
                    f"in your .env file for real responses.",
            model="mock-model",
            provider="mock",
            usage=Usage(
                prompt_tokens=len(user_msg.split()) * 2,
                completion_tokens=30,
                total_tokens=len(user_msg.split()) * 2 + 30,
            ),
        )

    async def _stream_mock(
        self, request: ChatRequest, model: str
    ) -> AsyncIterator[str]:
        """Mock streaming for testing."""
        import asyncio
        import json
        words = (
            "This is a mock streaming response. "
            "Each word arrives with a small delay to simulate real streaming. "
            "Configure a real provider for actual LLM responses."
        ).split()
        for i, word in enumerate(words):
            await asyncio.sleep(0.05)
            content = word + (" " if i < len(words) - 1 else "")
            data = {
                "content": content,
                "finish_reason": "stop" if i == len(words) - 1 else None,
            }
            yield f"data: {json.dumps(data)}\n\n"
        yield "data: [DONE]\n\n"


# Singleton
_llm_service: LLMService | None = None

def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
```

### Step 5: Route Handlers (30 min)

In `app/routes/chat.py`:

```python
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse, ErrorResponse
from app.services.llm_service import LLMService, get_llm_service

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Send a chat message",
    description="Send a conversation to the LLM and get a response. "
                "Set stream=true to receive Server-Sent Events instead.",
)
async def chat(
    request: ChatRequest,
    llm: LLMService = Depends(get_llm_service),
):
    if request.stream:
        return EventSourceResponse(
            llm.chat_stream(request),
            media_type="text/event-stream",
        )

    try:
        response = await llm.chat(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM provider error: {str(e)}"
        )


@router.post(
    "/chat/stream",
    summary="Stream a chat response",
    description="Dedicated streaming endpoint. "
                "Returns Server-Sent Events (SSE).",
)
async def chat_stream(
    request: ChatRequest,
    llm: LLMService = Depends(get_llm_service),
):
    # Force streaming regardless of the stream field
    return EventSourceResponse(
        llm.chat_stream(request),
        media_type="text/event-stream",
    )
```

In `app/routes/health.py`:

```python
import time
from fastapi import APIRouter
from app.models.responses import HealthResponse
from app.config import get_settings

router = APIRouter(tags=["health"])

_start_time = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
)
async def health_check():
    settings = get_settings()
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        providers={
            "openai": settings.has_openai,
            "anthropic": settings.has_anthropic,
            "mock": True,
        },
        uptime_seconds=round(time.time() - _start_time, 2),
    )
```

### Step 6: Main Application with Middleware (20 min)

In `app/main.py`:

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import time
import structlog

from app.config import get_settings
from app.routes import chat, health

settings = get_settings()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A production-ready LLM chat API with streaming support.",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS -- configured for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=round(duration * 1000, 2),
    )
    return response

# Register routes
app.include_router(health.router)
app.include_router(chat.router)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "docs": "/docs",
        "health": "/health",
    }
```

### Step 7: Run and Test (20 min)

Start the server:
```bash
# Create .env from .env.example and add your keys
cp .env.example .env

# Run with auto-reload for development
uvicorn app.main:app --reload --port 8000
```

Test manually:

1. **Open Swagger UI**: Go to `http://localhost:8000/docs` in your browser. You get a free interactive API playground.

2. **Health check**:
```bash
curl http://localhost:8000/health
```

3. **Chat (non-streaming)**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What is Python?"}],
    "provider": "mock"
  }'
```

4. **Chat (streaming)**:
```bash
curl -N -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Tell me a joke"}],
    "provider": "mock"
  }'
```

5. **Test from React** (if you want to quickly verify CORS):
```javascript
// In your browser console or a React app
const response = await fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{ role: 'user', content: 'Hello!' }],
    provider: 'mock'
  })
});
const data = await response.json();
console.log(data);
```

### Step 8: Write Tests (30 min)

In `tests/test_chat.py`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "providers" in data


def test_chat_with_mock():
    response = client.post("/api/v1/chat", json={
        "messages": [{"role": "user", "content": "Hello"}],
        "provider": "mock",
    })
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert data["provider"] == "mock"


def test_chat_missing_user_message():
    response = client.post("/api/v1/chat", json={
        "messages": [{"role": "system", "content": "You are helpful"}],
    })
    assert response.status_code == 422  # Validation error


def test_chat_empty_messages():
    response = client.post("/api/v1/chat", json={
        "messages": [],
    })
    assert response.status_code == 422


def test_chat_invalid_temperature():
    response = client.post("/api/v1/chat", json={
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 5.0,
    })
    assert response.status_code == 422


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert "docs" in response.json()
```

Run tests:
```bash
pytest tests/ -v
```

---

## Expected Output

After completing all steps:

1. `http://localhost:8000/docs` -- A full Swagger UI with all your endpoints documented
2. `http://localhost:8000/health` -- Returns provider availability status
3. POST `/api/v1/chat` -- Returns structured chat responses
4. POST `/api/v1/chat/stream` -- Returns SSE streaming responses
5. All tests pass with `pytest`

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **API Design** | 25% | RESTful routes, proper HTTP status codes, clear request/response models |
| **Streaming** | 20% | SSE endpoint works correctly, tokens arrive incrementally |
| **Error Handling** | 20% | Validation errors return 422, provider errors return 500, clear messages |
| **CORS + Config** | 15% | Environment-based config, CORS allows React frontend |
| **Tests** | 20% | At least 6 tests covering happy path and error cases |

---

## Bonus Challenges

1. **WebSocket Endpoint**: Add a WebSocket endpoint (`/ws/chat`) alongside the SSE endpoint. Compare the two approaches and document trade-offs.
2. **Request Caching**: Add Redis-based caching for identical requests (same messages + model + temperature). Use a TTL of 1 hour. Measure the latency improvement.
3. **API Key Authentication**: Add header-based API key auth (`X-API-Key`). Store valid keys in a config file or environment variable. This mirrors how you would secure your API in production.
4. **Conversation Memory**: Add a `conversation_id` field that persists conversations server-side (in-memory dict or SQLite). Clients can continue conversations without resending the full history.
5. **React Frontend**: Since you know React, build a simple chat UI that connects to your API. Use the `EventSource` API for streaming. This completes the full stack.

---

## Key Concepts You Will Learn

- **FastAPI**: The dominant Python web framework for AI applications
- **Dependency injection**: FastAPI's `Depends()` pattern (similar to React context/providers)
- **Server-Sent Events (SSE)**: How ChatGPT-style streaming works
- **Pydantic integration**: Auto-validation, auto-documentation from type hints
- **CORS**: Cross-origin config for frontend-backend communication
- **Async Python web servers**: uvicorn, ASGI, and why they matter for AI backends
