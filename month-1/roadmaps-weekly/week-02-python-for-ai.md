# Week 2 — Python for AI Engineering

[Back to Roadmap](../ROADMAP.md)

**Estimated Time:** ~6-7 hours (lessons + review)
**Goal:** Level up your Python skills specifically for AI engineering — async patterns for API calls, Pydantic for structured outputs, FastAPI for serving, and just enough NumPy to reason about embeddings. You already know Python; this week sharpens the tools you will use daily.

---

## Lesson 2.1 — Python Core for AI Engineers

### Sub-topics
- Type Hints Deep Dive
- Async/Await for Concurrent API Calls
- Generators & Iterators (for Streaming)
- Decorators
- Context Managers
- f-strings & Logging

### Key Concepts

**Type Hints Deep Dive.** As a frontend dev, you know TypeScript — Python type hints serve the same purpose but are not enforced at runtime (unless you use a tool like Pydantic or beartype). Modern AI Python code is heavily typed because: (1) LLM structured outputs map directly to typed models; (2) tools like mypy and pyright catch bugs before runtime; (3) IDEs provide dramatically better autocomplete. Key patterns you will use constantly: `Optional[str]` for nullable fields, `list[dict[str, Any]]` for LLM message formats, `Literal["gpt-4", "claude-3"]` for model name enums, `TypedDict` for dictionary shapes, and `Generic[T]` for reusable typed containers. Python 3.10+ lets you write `str | None` instead of `Optional[str]` and `list[str]` instead of `List[str]`. Use the modern syntax — it is cleaner and matches what you will see in current AI libraries.

**Async/Await for Concurrent API Calls.** LLM API calls are IO-bound — you spend most of the time waiting for the network response. Without async, calling 10 different LLMs sequentially takes the sum of all response times. With async, you fire all 10 requests concurrently and wait for the total time of the slowest one. Python's `asyncio` is essential for: batch processing (embed 1000 documents by making 50 concurrent API calls), agent orchestration (run multiple tool calls in parallel), and real-time applications (handle many users simultaneously). Key patterns: `async def`, `await`, `asyncio.gather()` for concurrent execution, `asyncio.Semaphore` for rate limiting, and `aiohttp` or `httpx.AsyncClient` for async HTTP. If you are coming from JavaScript, the mental model is nearly identical to `Promise.all()`.

```python
import asyncio
import httpx

async def call_llm(client: httpx.AsyncClient, prompt: str) -> str:
    response = await client.post("/v1/chat/completions", json={"prompt": prompt})
    return response.json()["choices"][0]["message"]["content"]

async def batch_process(prompts: list[str]) -> list[str]:
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent requests
    async with httpx.AsyncClient() as client:
        async def limited_call(prompt: str) -> str:
            async with semaphore:
                return await call_llm(client, prompt)
        return await asyncio.gather(*[limited_call(p) for p in prompts])
```

**Generators & Iterators for Streaming.** LLM APIs stream responses token-by-token using Server-Sent Events (SSE). Python generators (`yield`) are the natural way to handle streaming data — they produce values lazily without loading the entire response into memory. You will write generators that consume SSE streams and yield parsed tokens, and async generators (`async for`) for streaming in async contexts. This pattern is critical for: real-time chat UIs (send tokens to the frontend as they arrive), long-running generation (avoid timeouts by streaming), and memory efficiency (process large outputs without buffering).

```python
async def stream_response(client, prompt: str):
    async with client.stream("POST", "/v1/chat/completions",
                              json={"prompt": prompt, "stream": True}) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: ") and line != "data: [DONE]":
                chunk = json.loads(line[6:])
                token = chunk["choices"][0]["delta"].get("content", "")
                if token:
                    yield token
```

**Decorators.** Decorators wrap functions to add behavior — logging, retrying, caching, timing. In AI engineering, you will use decorators for: retry logic on flaky API calls (`@retry(max_attempts=3, backoff=exponential)`), caching expensive LLM responses (`@lru_cache` or custom disk cache), rate limiting, and observability (logging inputs/outputs for debugging). Understanding decorators also helps when working with frameworks like LangChain and FastAPI, which use them extensively.

**Context Managers.** The `with` statement ensures resources are properly cleaned up. You will use context managers for: HTTP client sessions (`async with httpx.AsyncClient() as client:`), database connections, file handling, and temporary resource management. Custom context managers using `@contextmanager` are useful for patterns like "set up a tracing span, yield, then close the span." In AI applications, context managers are essential for managing API client lifecycles and ensuring connections are properly closed even when exceptions occur.

**f-strings & Logging.** Prompt construction often involves complex string formatting. f-strings are the standard, but for production systems, use proper logging (`import logging`) instead of print statements. Structured logging with libraries like `structlog` gives you searchable, parseable logs — critical when debugging LLM behavior in production. Log the prompt, model parameters, response, latency, and token counts for every LLM call. This observability is what separates hobby projects from production systems.

### Interview Questions

**Q1: How would you make 100 LLM API calls efficiently in Python?**
**A:** Use `asyncio` with `httpx.AsyncClient` and `asyncio.gather()` to make concurrent requests. Add a `Semaphore` to respect rate limits (e.g., max 20 concurrent requests). Use exponential backoff retry logic for transient failures. This pattern turns 100 sequential 2-second calls (200s total) into roughly 10 batches of 10 concurrent calls (~20s total). Key considerations: rate limiting, error handling per request (don't let one failure cancel all), and timeout configuration.

**Q2: Explain Python generators and why they matter for LLM streaming.**
**A:** Generators (`yield`) produce values lazily — they compute and return one value at a time without holding the entire sequence in memory. LLM APIs stream responses as SSE (Server-Sent Events), delivering tokens incrementally. Generators naturally model this: you write a generator that yields each token as it arrives, and the consumer processes tokens one-by-one. This enables real-time UI updates, avoids timeout issues on long generations, and keeps memory usage constant regardless of response length. Async generators (`async for`) extend this to async contexts.

**Q3: Why are type hints important in AI engineering, and how do they relate to Pydantic?**
**A:** Type hints document expected data shapes, enable IDE autocompletion, and catch type errors via static analysis (mypy/pyright). In AI engineering, they are doubly important because Pydantic uses type hints to validate data at runtime — when you define a Pydantic model with typed fields, those hints become actual runtime validators. This means the same type annotation both documents the expected LLM output schema and enforces it when parsing responses. LLM structured output features (OpenAI's function calling, Anthropic's tool use) generate JSON that maps directly to Pydantic models.

### Hands-on
- [Assignment: Python AI Toolkit](./assignments/w02-a1-python-ai-toolkit.md)

---

## Lesson 2.2 — Pydantic v2 for Structured AI

### Sub-topics
- BaseModel
- Field Validators
- JSON Schema Generation
- model_validate
- Discriminated Unions
- Why Pydantic Matters for LLM Structured Outputs

### Key Concepts

**BaseModel.** Pydantic's `BaseModel` is the foundation of structured data handling in Python AI applications. You define a class with typed fields, and Pydantic automatically validates, coerces, and serializes data. This replaces the fragile pattern of passing raw dictionaries everywhere. When an LLM returns JSON, you parse it into a Pydantic model and get immediate validation — if the LLM hallucinated an integer where a string was expected, you catch it immediately rather than discovering it three function calls later.

```python
from pydantic import BaseModel, Field

class LLMResponse(BaseModel):
    answer: str = Field(description="The main answer to the user's question")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    sources: list[str] = Field(default_factory=list, description="Source references")
    reasoning: str | None = Field(default=None, description="Chain of thought reasoning")
```

**Field Validators.** Pydantic v2 provides two validator types: `@field_validator` for single-field validation and `@model_validator` for cross-field validation. These are essential for constraining LLM outputs beyond basic type checking. For example, you might validate that a generated SQL query does not contain DROP statements, that a list of extracted entities has no duplicates, or that a generated date is in the future. Validators run automatically on model construction, giving you a safety net between the LLM's raw output and your application logic.

```python
from pydantic import BaseModel, field_validator, model_validator

class ExtractedEntity(BaseModel):
    name: str
    entity_type: Literal["person", "org", "location"]
    confidence: float

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Entity name cannot be empty")
        return v.strip()

    @field_validator("confidence")
    @classmethod
    def valid_confidence(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")
        return round(v, 3)
```

**JSON Schema Generation.** `MyModel.model_json_schema()` generates a JSON Schema from your Pydantic model. This is the bridge between your Python types and LLM structured output: you pass the JSON Schema to the LLM API (as a function schema, tool definition, or response format), and the LLM constrains its output to match that schema. OpenAI's structured outputs, Anthropic's tool use, and most LLM frameworks use JSON Schema as the interchange format. Your Pydantic model is the single source of truth — it defines the schema sent to the LLM and validates the response.

**model_validate.** `MyModel.model_validate(data)` validates a dictionary (or JSON string via `model_validate_json`) against the model. This is how you parse LLM responses: get the JSON string from the API, call `model_validate_json(response_text)`, and either get a validated Python object or a clear `ValidationError` telling you exactly what went wrong. This replaces error-prone manual dictionary access with typed, validated data.

**Discriminated Unions.** When an LLM might return different response types (e.g., a text answer, a code block, or an error), discriminated unions let you model this cleanly. You define a base type field (the discriminator) and Pydantic automatically selects the right model variant. This is powerful for agent architectures where the LLM decides which tool to call — each tool has a different parameter schema, and the discriminated union validates the correct one based on the tool name.

```python
from pydantic import BaseModel
from typing import Literal, Union

class SearchAction(BaseModel):
    action: Literal["search"] = "search"
    query: str

class CalculateAction(BaseModel):
    action: Literal["calculate"] = "calculate"
    expression: str

class AnswerAction(BaseModel):
    action: Literal["answer"] = "answer"
    text: str

AgentAction = Union[SearchAction, CalculateAction, AnswerAction]
# Pydantic automatically discriminates based on the "action" field
```

**Why Pydantic Matters for LLM Structured Outputs.** The LLM ecosystem has converged on Pydantic as the standard way to define and validate structured outputs. OpenAI's Python SDK uses Pydantic models directly in `client.beta.chat.completions.parse()`. LangChain, LlamaIndex, Instructor, and Marvin all build on Pydantic. The pattern is: (1) define a Pydantic model describing what you want; (2) generate JSON Schema from it; (3) pass the schema to the LLM; (4) validate the response against the model. This creates a type-safe pipeline from LLM output to application code. Pydantic is not optional in modern AI engineering — it is infrastructure.

### Interview Questions

**Q1: How does Pydantic bridge the gap between LLM outputs and typed Python code?**
**A:** Pydantic models define the expected output structure with type annotations and constraints. `model_json_schema()` generates a JSON Schema that is passed to the LLM API to constrain its output format. When the response arrives, `model_validate_json()` parses and validates it against the same model. If validation fails, you get a detailed error. This creates an end-to-end typed pipeline: Python types define the contract, JSON Schema communicates it to the LLM, and Pydantic enforces it on the response.

**Q2: What is a discriminated union in Pydantic, and when would you use it in an AI application?**
**A:** A discriminated union is a Union type where Pydantic uses a specific field (the discriminator) to determine which variant to validate against. In AI applications, this models scenarios where the LLM output varies by type — like an agent choosing between different tools (each with different parameters) or a classifier returning different response structures based on the detected category. The discriminator field (e.g., "action": "search" vs "action": "calculate") tells Pydantic which validation rules to apply.

**Q3: Why is `model_json_schema()` important for LLM integrations?**
**A:** It automatically generates the JSON Schema that LLM APIs require for structured outputs. Instead of manually writing and maintaining JSON Schemas (error-prone, out of sync with code), you define a Pydantic model once and derive the schema from it. This is the single source of truth pattern: the same model defines the API contract (schema) and validates the response (parsing). Any change to the model automatically updates both.

### Hands-on
- [Assignment: Pydantic Structured Outputs](./assignments/w02-a2-pydantic-structured-outputs.md)

---

## Lesson 2.3 — UV Package Manager & Project Structure

### Sub-topics
- Why UV over pip/poetry
- pyproject.toml
- Virtual Environments
- Dependency Management
- Project Layout for AI Apps

### Key Concepts

**Why UV over pip/poetry.** UV is a modern Python package manager written in Rust by the Astral team (who also make Ruff, the fast Python linter). It is 10-100x faster than pip for dependency resolution and installation. For AI projects, where you often install large packages (torch, transformers, numpy, scipy), the speed difference is dramatic — minutes vs. seconds. UV also provides a unified tool for virtual environments, dependency resolution, and lockfiles, replacing the fragmented pip + venv + pip-tools stack. It is compatible with pip's requirements format and pyproject.toml.

**pyproject.toml.** This is the standard Python project configuration file, replacing the older setup.py and setup.cfg. It centralizes project metadata, dependencies, build configuration, and tool settings in one file. For AI projects, your pyproject.toml typically includes: project dependencies (openai, anthropic, pydantic, fastapi), development dependencies (pytest, mypy, ruff), tool configurations (ruff rules, mypy strictness), and scripts (entry points for your application).

```toml
[project]
name = "my-ai-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "openai>=1.30",
    "anthropic>=0.25",
    "pydantic>=2.7",
    "fastapi>=0.111",
    "httpx>=0.27",
    "uvicorn>=0.30",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "mypy>=1.10", "ruff>=0.4"]

[tool.ruff]
target-version = "py311"
line-length = 100
```

**Virtual Environments.** Always use a virtual environment — never install AI packages globally. With UV: `uv venv` creates a venv, `uv pip install -r requirements.txt` installs into it. Virtual environments isolate your project dependencies, preventing version conflicts between projects. This is especially important for AI projects because different models and frameworks often require conflicting dependency versions (e.g., different projects needing different torch versions).

**Project Layout for AI Apps.** A well-structured AI project separates concerns clearly. A recommended layout for AI applications:

```
my-ai-app/
├── pyproject.toml
├── src/
│   └── my_ai_app/
│       ├── __init__.py
│       ├── api/           # FastAPI routes
│       ├── agents/        # Agent definitions
│       ├── prompts/       # Prompt templates
│       ├── models/        # Pydantic models
│       ├── services/      # LLM client wrappers
│       └── config.py      # Settings via pydantic-settings
├── tests/
├── scripts/               # One-off scripts, evaluations
└── .env                   # API keys (never commit)
```

The key principles: keep prompts separate from logic (they change frequently), wrap LLM clients in service classes (easy to swap providers), use Pydantic models as the interface between components, and store configuration in environment variables.

### Interview Questions

**Q1: Why would you choose UV over pip for an AI project?**
**A:** Speed is the primary reason — UV is 10-100x faster for dependency resolution and installation, which matters when installing heavy packages like torch or transformers. UV also provides a unified workflow (venv creation, dependency resolution, lockfiles) replacing the fragmented pip+venv+pip-tools stack. It uses the same pyproject.toml standard as modern Python tooling and produces deterministic lockfiles for reproducible environments.

**Q2: How would you structure a production AI application in Python?**
**A:** Separate concerns: `api/` for HTTP routes, `agents/` for agent logic, `prompts/` for prompt templates (they change independently from code), `models/` for Pydantic schemas, `services/` for LLM client wrappers. Use pydantic-settings for configuration, store API keys in environment variables (never committed), and keep evaluation scripts separate from application code. This structure makes it easy to swap LLM providers, A/B test prompts, and maintain clean separation between infrastructure and AI logic.

---

## Lesson 2.4 — NumPy Essentials for Embeddings

### Sub-topics
- Vectors & Matrices Basics
- Dot Product
- Cosine Similarity Implementation
- Broadcasting

### Key Concepts

**Vectors & Matrices Basics.** For AI engineering, you need just enough NumPy to work with embeddings. An embedding is a 1D NumPy array (vector) of floats, typically 768-3072 dimensions. A batch of embeddings is a 2D array (matrix) where each row is one embedding. Key operations: `np.array([1.0, 2.0, 3.0])` creates a vector, `.shape` tells you dimensions, `embeddings[0]` accesses the first embedding in a batch. You do not need to master NumPy's full API — focus on the operations used in similarity search and embedding manipulation.

```python
import numpy as np

# Single embedding (1536 dimensions, like OpenAI's text-embedding-3-small)
embedding = np.array([0.023, -0.041, 0.089, ...])  # shape: (1536,)

# Batch of 100 embeddings
batch = np.random.randn(100, 1536)  # shape: (100, 1536)
```

**Dot Product.** The dot product of two vectors is the sum of element-wise products: a · b = Σ(a_i * b_i). For normalized vectors (magnitude = 1), the dot product equals cosine similarity. NumPy: `np.dot(a, b)` or `a @ b`. For a batch: `batch @ query` computes the dot product of every embedding with the query vector simultaneously, returning a vector of 100 similarity scores in one operation. This vectorized operation is orders of magnitude faster than a Python loop.

**Cosine Similarity Implementation.** Cosine similarity = dot product / (magnitude_a * magnitude_b). In NumPy:

```python
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def batch_cosine_similarity(query: np.ndarray, embeddings: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between query and all embeddings."""
    query_norm = query / np.linalg.norm(query)
    emb_norms = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return emb_norms @ query_norm  # shape: (n_embeddings,)

# Find top-k most similar
similarities = batch_cosine_similarity(query_embedding, all_embeddings)
top_k_indices = np.argsort(similarities)[-5:][::-1]  # Top 5
```

Understanding this implementation helps you debug RAG retrieval issues. If your similarity scores are all near 0, your embeddings might not be normalized. If top results seem random, the embedding model might not be suitable for your domain.

**Broadcasting.** NumPy broadcasting automatically expands dimensions when operating on arrays of different shapes. When you subtract a (1536,) vector from a (100, 1536) matrix, NumPy broadcasts the vector across all 100 rows. This is useful for centering embeddings (subtract the mean) and normalization. You do not need deep broadcasting expertise — just know that it exists and that it is what makes operations like `embeddings - mean_embedding` work without explicit loops.

### Interview Questions

**Q1: Implement cosine similarity for two embedding vectors without using a library function.**
**A:** Cosine similarity is the dot product divided by the product of magnitudes: `cos_sim = sum(a[i]*b[i] for i in range(len(a))) / (sqrt(sum(x**2 for x in a)) * sqrt(sum(x**2 for x in b)))`. In NumPy: `np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))`. For pre-normalized vectors (common in production), this simplifies to just the dot product: `np.dot(a, b)`. Most embedding APIs return normalized vectors, so dot product is sufficient and faster.

**Q2: Why is vectorized NumPy computation important for embedding operations?**
**A:** Computing similarity between a query and 10,000 stored embeddings using a Python loop takes hundreds of milliseconds. The same operation vectorized as a matrix multiplication (`embeddings @ query`) takes under a millisecond because NumPy delegates to optimized C/Fortran BLAS libraries that use SIMD instructions and cache-efficient memory access patterns. For production RAG systems handling many queries, this difference is critical.

---

## Lesson 2.5 — FastAPI Fundamentals

### Sub-topics
- Why FastAPI for AI Backends
- Route Handlers
- Request/Response Models with Pydantic
- SSE Streaming
- Dependency Injection
- CORS for React Frontends

### Key Concepts

**Why FastAPI for AI Backends.** FastAPI is the dominant choice for AI backend services in Python because: (1) native async support — essential for handling concurrent LLM API calls without blocking; (2) built on Pydantic — request/response validation uses the same models you define for LLM outputs; (3) automatic OpenAPI documentation — your AI service gets Swagger UI for free; (4) performance — one of the fastest Python web frameworks (built on Starlette and Uvicorn); (5) SSE streaming support — critical for real-time LLM response streaming. For a frontend developer transitioning to AI, FastAPI is the closest Python analog to Express.js/Next.js API routes, but with superior type safety.

**Route Handlers.** FastAPI route handlers are async functions decorated with HTTP method decorators. The pattern will feel familiar from Express:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-4"
    temperature: float = 0.7

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int
    model: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # Call LLM API
    result = await llm_service.chat(request.message, request.model, request.temperature)
    return ChatResponse(
        reply=result.content,
        tokens_used=result.usage.total_tokens,
        model=request.model,
    )
```

FastAPI automatically validates the request body against `ChatRequest`, returns 422 with detailed errors for invalid input, and generates OpenAPI docs showing the exact request/response schema.

**Request/Response Models with Pydantic.** Every endpoint should have explicit Pydantic models for request and response bodies. This is where Week 2's Pydantic knowledge directly applies. Benefits: automatic request validation, clear API contracts, generated documentation, and type safety throughout your codebase. Anti-pattern: accepting raw `dict` bodies and manually extracting fields. Always define a model.

**SSE Streaming.** Streaming LLM responses to the frontend requires Server-Sent Events. FastAPI supports this via `StreamingResponse`:

```python
from fastapi.responses import StreamingResponse
import json

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        async for token in llm_service.stream_chat(request.message):
            data = json.dumps({"token": token})
            yield f"data: {data}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

On the frontend (React), you consume this with `EventSource` or the `fetch` API with a `ReadableStream` reader. This is the standard pattern for ChatGPT-style streaming interfaces. The `data:` prefix and double newlines follow the SSE protocol.

**Dependency Injection.** FastAPI's dependency injection system manages shared resources — database connections, LLM clients, authentication. Instead of global variables, you declare dependencies in function signatures:

```python
from fastapi import Depends

async def get_llm_client() -> AsyncOpenAI:
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    return client

@app.post("/chat")
async def chat(
    request: ChatRequest,
    client: AsyncOpenAI = Depends(get_llm_client),
):
    response = await client.chat.completions.create(...)
    return response
```

Dependencies can be overridden in tests — inject a mock LLM client to test your API without making real API calls. This is critical for testing AI applications where real LLM calls are slow and expensive.

**CORS for React Frontends.** As a frontend developer, you know the CORS pain. FastAPI makes it straightforward:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

In production, restrict `allow_origins` to your actual domain. For SSE streaming to work cross-origin, CORS headers must be properly configured. A common debugging issue: SSE streams failing silently in the browser due to CORS — check the Network tab.

### Interview Questions

**Q1: Why is FastAPI well-suited for AI backends compared to Flask or Django?**
**A:** FastAPI offers: (1) native async support essential for concurrent LLM API calls (Flask is synchronous by default); (2) built-in Pydantic integration for request/response validation using the same models as LLM structured outputs; (3) automatic OpenAPI documentation; (4) SSE streaming support for real-time LLM response delivery; (5) high performance via Starlette/Uvicorn. Flask can be made async with extensions but it is not native; Django's ORM-centric design adds unnecessary weight for stateless AI services.

**Q2: How would you implement streaming LLM responses to a React frontend?**
**A:** Backend: use FastAPI's `StreamingResponse` with an async generator that yields SSE-formatted data (`data: {json}\n\n`) from the LLM streaming API. Frontend: use the `fetch` API with `response.body.getReader()` to read the stream, parse each SSE chunk, and update the UI incrementally. This is the standard pattern for ChatGPT-style interfaces. Key considerations: proper CORS configuration, handling connection drops gracefully, and a `[DONE]` sentinel to signal stream end.

**Q3: Explain FastAPI's dependency injection and why it matters for AI applications.**
**A:** FastAPI's `Depends()` system lets you declare shared resources (LLM clients, database connections, auth context) as function parameters. Dependencies are resolved automatically per-request. For AI applications, this matters because: (1) LLM clients can be shared and properly managed (connection pooling); (2) dependencies can be overridden in tests — inject a mock LLM client to test your API without real API calls (which are slow and cost money); (3) configuration and secrets are injected rather than imported globally, improving testability and modularity.

### Hands-on
- [Assignment: FastAPI LLM Endpoint](./assignments/w02-a3-fastapi-llm-endpoint.md)

---

## Week 2 Summary Checklist

After completing this week, you should be able to:

- [ ] Use modern Python type hints including Union, Literal, TypedDict, and Generic
- [ ] Write async code for concurrent LLM API calls using asyncio.gather and Semaphore
- [ ] Implement streaming with async generators and understand the SSE protocol
- [ ] Define Pydantic v2 models with field validators and model validators
- [ ] Generate JSON Schema from Pydantic models for LLM structured output
- [ ] Use discriminated unions for multi-type LLM responses
- [ ] Set up a Python project with UV and pyproject.toml
- [ ] Structure an AI application with proper separation of concerns
- [ ] Compute cosine similarity using NumPy and understand vectorized operations
- [ ] Build a FastAPI endpoint that calls an LLM and streams the response
- [ ] Configure CORS for a React frontend consuming an AI backend
- [ ] Use FastAPI dependency injection for testable AI services

---

**Previous:** [Week 1 — LLM Fundamentals](./week-01-llm-fundamentals.md)
**Next:** [Week 3 — Prompt Engineering & API Mastery](./week-03-prompt-engineering.md)
