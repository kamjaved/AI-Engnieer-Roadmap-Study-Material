# Assignment 2.1: Python AI Toolkit

> **Week 2** | [Back to Week 2 Plan](../week-2.md)

## Title
**Python AI Toolkit** -- Build Your GenAI Engineering Utility Belt

## Objective
Build a reusable Python utility module containing the core patterns every GenAI engineer uses daily: async batch API calling, streaming response handling, retry logic with exponential backoff, token counting, and structured logging. This module will become the foundation you carry into every future project.

## Difficulty
Intermediate

## Estimated Time
3-4 hours

## Prerequisites
- Python 3.10+ installed
- Comfort with Python basics (classes, functions, decorators)
- Basic understanding of async/await (we will deepen it here)
- Install dependencies:
```bash
pip install aiohttp httpx pytest pytest-asyncio tenacity tiktoken structlog rich
```

## Why This Matters
As a frontend developer, you are used to npm packages solving common problems. In GenAI engineering, you will find yourself writing the same patterns repeatedly:
- Calling LLM APIs with retries when they rate-limit you
- Processing streaming responses token by token
- Batching hundreds of API calls efficiently
- Logging every request for debugging and cost tracking

Building these once, correctly, saves you hours on every future project.

---

## Detailed Instructions

### Step 1: Project Setup (10 min)

```
python-ai-toolkit/
  ai_toolkit/
    __init__.py
    retry.py
    streaming.py
    batch.py
    tokens.py
    logging.py
  tests/
    __init__.py
    test_retry.py
    test_streaming.py
    test_batch.py
    test_tokens.py
  pyproject.toml
```

Set up `pyproject.toml` with your dependencies and configure pytest:
```toml
[project]
name = "ai-toolkit"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "aiohttp>=3.9",
    "httpx>=0.27",
    "tiktoken>=0.7",
    "structlog>=24.0",
    "tenacity>=8.0",
    "rich>=13.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Step 2: Retry Decorator with Exponential Backoff (40 min)

In `retry.py`, build a retry decorator from scratch (then optionally compare with `tenacity`):

```python
import asyncio
import functools
import random
import time
from typing import TypeVar, Callable, Any
from collections.abc import Awaitable

F = TypeVar("F", bound=Callable[..., Any])


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
        retryable_status_codes: tuple[int, ...] = (429, 500, 502, 503, 504),
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions
        self.retryable_status_codes = retryable_status_codes

    def compute_delay(self, attempt: int) -> float:
        """Calculate delay for the given attempt number."""
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)
        if self.jitter:
            delay = delay * (0.5 + random.random() * 0.5)
        return delay


class RetryExhaustedError(Exception):
    """Raised when all retry attempts have been exhausted."""

    def __init__(self, last_exception: Exception, attempts: int):
        self.last_exception = last_exception
        self.attempts = attempts
        super().__init__(
            f"Failed after {attempts} attempts. Last error: {last_exception}"
        )


def with_retry(config: RetryConfig | None = None) -> Callable[[F], F]:
    """
    Decorator that adds retry logic with exponential backoff.

    Works with both sync and async functions.

    Usage:
        @with_retry(RetryConfig(max_retries=5))
        async def call_api(prompt: str) -> str:
            ...
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e
                    if attempt < config.max_retries:
                        delay = config.compute_delay(attempt)
                        # Log the retry (you'll integrate with structlog later)
                        print(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        await asyncio.sleep(delay)
            raise RetryExhaustedError(last_exception, config.max_retries + 1)

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e
                    if attempt < config.max_retries:
                        delay = config.compute_delay(attempt)
                        print(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        time.sleep(delay)
            raise RetryExhaustedError(last_exception, config.max_retries + 1)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        return sync_wrapper  # type: ignore

    return decorator
```

**Write tests** in `test_retry.py`:
- Test that a function succeeding on the first try works normally
- Test that a function failing 2 times then succeeding returns the result
- Test that a function failing more than `max_retries` raises `RetryExhaustedError`
- Test that the delay increases exponentially
- Test that non-retryable exceptions are raised immediately
- Test both sync and async versions

### Step 3: Streaming Response Handler (40 min)

In `streaming.py`, build utilities for handling Server-Sent Events (SSE) streaming -- the format used by OpenAI and Anthropic:

```python
import asyncio
from typing import AsyncIterator, Callable
from dataclasses import dataclass, field


@dataclass
class StreamChunk:
    """A single chunk from a streaming response."""
    content: str
    finish_reason: str | None = None
    model: str | None = None
    usage: dict | None = None


@dataclass
class StreamAccumulator:
    """Accumulates streaming chunks into a complete response."""
    chunks: list[StreamChunk] = field(default_factory=list)
    _full_content: str = ""

    def add(self, chunk: StreamChunk) -> None:
        self.chunks.append(chunk)
        self._full_content += chunk.content

    @property
    def content(self) -> str:
        return self._full_content

    @property
    def is_complete(self) -> bool:
        return any(c.finish_reason is not None for c in self.chunks)

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)


async def stream_to_console(
    stream: AsyncIterator[StreamChunk],
    on_chunk: Callable[[StreamChunk], None] | None = None,
) -> StreamAccumulator:
    """
    Consume a stream, printing each chunk to console in real-time.

    This mimics the ChatGPT typing effect.
    Returns the complete accumulated response.
    """
    accumulator = StreamAccumulator()
    async for chunk in stream:
        accumulator.add(chunk)
        print(chunk.content, end="", flush=True)
        if on_chunk:
            on_chunk(chunk)
    print()  # newline at end
    return accumulator


async def simulate_llm_stream(
    text: str, chunk_size: int = 3, delay: float = 0.05
) -> AsyncIterator[StreamChunk]:
    """
    Simulate an LLM streaming response for testing.

    Yields chunks of the given text with realistic delays.
    """
    words = text.split(" ")
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i : i + chunk_size]
        content = " ".join(chunk_words)
        if i > 0:
            content = " " + content

        is_last = (i + chunk_size) >= len(words)
        yield StreamChunk(
            content=content,
            finish_reason="stop" if is_last else None,
        )
        if not is_last:
            await asyncio.sleep(delay)


async def stream_with_timeout(
    stream: AsyncIterator[StreamChunk],
    timeout: float = 30.0,
    chunk_timeout: float = 10.0,
) -> AsyncIterator[StreamChunk]:
    """
    Wrap a stream with overall and per-chunk timeouts.

    Raises TimeoutError if the entire stream or a single chunk
    takes too long.
    """
    start = asyncio.get_event_loop().time()
    async for chunk in stream:
        elapsed = asyncio.get_event_loop().time() - start
        if elapsed > timeout:
            raise TimeoutError(
                f"Stream exceeded total timeout of {timeout}s"
            )
        yield chunk
```

**Write tests** in `test_streaming.py`:
- Test `simulate_llm_stream` produces correct chunks
- Test `StreamAccumulator` builds the full content correctly
- Test `is_complete` returns True only after finish_reason is set
- Test `stream_with_timeout` raises on slow streams

### Step 4: Async Batch API Caller (45 min)

In `batch.py`, build an async batch processor with concurrency control:

```python
import asyncio
from typing import TypeVar, Callable, Any
from dataclasses import dataclass

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class BatchResult:
    """Result of a batch operation."""
    successful: list[tuple[int, Any]]  # (index, result)
    failed: list[tuple[int, Exception]]  # (index, error)

    @property
    def success_rate(self) -> float:
        total = len(self.successful) + len(self.failed)
        return len(self.successful) / total if total > 0 else 0.0

    @property
    def total(self) -> int:
        return len(self.successful) + len(self.failed)


async def batch_process(
    items: list[T],
    processor: Callable[[T], Any],
    max_concurrency: int = 5,
    rate_limit_per_second: float | None = None,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchResult:
    """
    Process a list of items concurrently with rate limiting.

    Args:
        items: List of items to process
        processor: Async function to call for each item
        max_concurrency: Maximum concurrent tasks
        rate_limit_per_second: Max requests per second (None = unlimited)
        on_progress: Callback(completed, total) for progress updates
    """
    semaphore = asyncio.Semaphore(max_concurrency)
    successful: list[tuple[int, Any]] = []
    failed: list[tuple[int, Exception]] = []
    completed = 0

    # Rate limiter
    rate_limiter: asyncio.Semaphore | None = None
    if rate_limit_per_second:
        rate_limiter = asyncio.Semaphore(int(rate_limit_per_second))

        async def refill_rate_limiter():
            while True:
                await asyncio.sleep(1.0)
                # Release up to rate_limit tokens
                for _ in range(int(rate_limit_per_second)):
                    try:
                        rate_limiter.release()
                    except ValueError:
                        break

        asyncio.create_task(refill_rate_limiter())

    async def process_one(index: int, item: T) -> None:
        nonlocal completed
        async with semaphore:
            if rate_limiter:
                await rate_limiter.acquire()
            try:
                result = await processor(item)
                successful.append((index, result))
            except Exception as e:
                failed.append((index, e))
            finally:
                completed += 1
                if on_progress:
                    on_progress(completed, len(items))

    tasks = [process_one(i, item) for i, item in enumerate(items)]
    await asyncio.gather(*tasks)

    # Sort by index to maintain order
    successful.sort(key=lambda x: x[0])
    failed.sort(key=lambda x: x[0])

    return BatchResult(successful=successful, failed=failed)
```

**Write tests** in `test_batch.py`:
- Test that all items get processed
- Test that max_concurrency is respected (use timing checks)
- Test that failures do not stop other items from processing
- Test progress callback is called correctly
- Test with a mix of succeeding and failing processors

### Step 5: Token Counter Utility (25 min)

In `tokens.py`, build a utility that counts tokens and estimates costs:

```python
import tiktoken
from dataclasses import dataclass


@dataclass
class TokenCount:
    """Token count with cost estimation."""
    text_length: int
    token_count: int
    model: str
    estimated_input_cost: float
    estimated_output_cost: float

    @property
    def chars_per_token(self) -> float:
        return self.text_length / self.token_count if self.token_count > 0 else 0

    def __repr__(self) -> str:
        return (
            f"TokenCount(tokens={self.token_count}, "
            f"chars/token={self.chars_per_token:.1f}, "
            f"est_cost=${self.estimated_input_cost:.6f})"
        )


# Pricing per 1M tokens (update as needed)
MODEL_PRICING: dict[str, dict[str, float]] = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
}


def count_tokens(
    text: str,
    model: str = "gpt-4o",
) -> TokenCount:
    """
    Count tokens for the given text and model.
    Returns token count with cost estimation.
    """
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fall back to cl100k_base for unknown models
        enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(text)
    pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})

    return TokenCount(
        text_length=len(text),
        token_count=len(tokens),
        model=model,
        estimated_input_cost=len(tokens) * pricing["input"] / 1_000_000,
        estimated_output_cost=len(tokens) * pricing["output"] / 1_000_000,
    )


def count_messages_tokens(
    messages: list[dict[str, str]],
    model: str = "gpt-4o",
) -> TokenCount:
    """
    Count tokens for a list of chat messages.
    Accounts for the message formatting overhead.
    """
    # Each message has ~4 tokens of overhead (role, content markers)
    TOKENS_PER_MESSAGE = 4
    TOKENS_REPLY_OVERHEAD = 3  # <|start|>assistant<|message|>

    total_text = ""
    overhead = TOKENS_REPLY_OVERHEAD

    for message in messages:
        overhead += TOKENS_PER_MESSAGE
        total_text += message.get("role", "") + message.get("content", "")

    base_count = count_tokens(total_text, model)
    adjusted_count = base_count.token_count + overhead

    pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
    return TokenCount(
        text_length=base_count.text_length,
        token_count=adjusted_count,
        model=model,
        estimated_input_cost=adjusted_count * pricing["input"] / 1_000_000,
        estimated_output_cost=adjusted_count * pricing["output"] / 1_000_000,
    )


def estimate_conversation_cost(
    messages: list[dict[str, str]],
    expected_output_tokens: int = 500,
    model: str = "gpt-4o",
) -> dict[str, float]:
    """Estimate total cost for a conversation turn."""
    input_count = count_messages_tokens(messages, model)
    pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
    output_cost = expected_output_tokens * pricing["output"] / 1_000_000

    return {
        "input_tokens": input_count.token_count,
        "estimated_output_tokens": expected_output_tokens,
        "input_cost": input_count.estimated_input_cost,
        "output_cost": output_cost,
        "total_cost": input_count.estimated_input_cost + output_cost,
    }
```

**Write tests** in `test_tokens.py`:
- Test token counts match expected values for known strings
- Test cost calculations are accurate
- Test message overhead is accounted for
- Test unknown models fall back gracefully

### Step 6: Structured Logging Setup (30 min)

In `logging.py`, configure production-grade logging:

```python
import structlog
import logging
import sys
from typing import Any


def setup_logging(
    level: str = "INFO",
    json_output: bool = False,
    log_file: str | None = None,
) -> structlog.stdlib.BoundLogger:
    """
    Configure structured logging for AI applications.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        json_output: If True, output JSON lines (for production)
        log_file: Optional file path for log output
    """
    # Configure standard library logging
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper()),
        handlers=handlers,
    )

    # Configure structlog
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    return structlog.get_logger()


def create_api_logger(
    provider: str, model: str
) -> structlog.stdlib.BoundLogger:
    """
    Create a logger pre-bound with API context.

    Usage:
        log = create_api_logger("openai", "gpt-4o")
        log.info("request_sent", prompt_tokens=150)
        log.info("response_received", completion_tokens=89, latency_ms=1200)
    """
    logger = structlog.get_logger()
    return logger.bind(provider=provider, model=model)
```

### Step 7: Integration Demo (20 min)

Create a `demo.py` at the project root that shows all components working together:

```python
"""
Demo: All toolkit components working together.
Simulates a batch of LLM API calls with retries, streaming, and logging.
"""
import asyncio
from ai_toolkit.retry import with_retry, RetryConfig
from ai_toolkit.streaming import simulate_llm_stream, stream_to_console
from ai_toolkit.batch import batch_process
from ai_toolkit.tokens import count_tokens, estimate_conversation_cost
from ai_toolkit.logging import setup_logging, create_api_logger


async def main():
    # Set up logging
    log = setup_logging(level="DEBUG")
    api_log = create_api_logger("simulated", "demo-model")

    # 1. Token counting
    prompt = "Explain quantum computing in simple terms"
    token_info = count_tokens(prompt, "gpt-4o")
    api_log.info("token_count", **vars(token_info))

    # 2. Streaming
    print("\n--- Streaming Demo ---")
    stream = simulate_llm_stream(
        "Quantum computing uses quantum bits or qubits which can exist "
        "in multiple states simultaneously unlike classical bits."
    )
    result = await stream_to_console(stream)
    print(f"(Received {result.chunk_count} chunks)")

    # 3. Batch processing with retries
    print("\n--- Batch Processing Demo ---")
    prompts = [f"Question {i}: What is {i}+{i}?" for i in range(10)]

    call_count = 0

    @with_retry(RetryConfig(max_retries=2, base_delay=0.1))
    async def process_prompt(prompt: str) -> str:
        nonlocal call_count
        call_count += 1
        # Simulate occasional failures
        if call_count % 4 == 0:
            raise ConnectionError("Simulated API error")
        await asyncio.sleep(0.1)  # Simulate API latency
        return f"Answer to: {prompt}"

    def progress(done: int, total: int) -> None:
        print(f"  Progress: {done}/{total}", end="\r")

    results = await batch_process(
        prompts, process_prompt, max_concurrency=3, on_progress=progress
    )
    print(f"\nBatch complete: {results.success_rate:.0%} success rate")
    print(f"  Succeeded: {len(results.successful)}")
    print(f"  Failed: {len(results.failed)}")

    # 4. Cost estimation
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    cost = estimate_conversation_cost(messages, model="gpt-4o")
    api_log.info("cost_estimate", **cost)


if __name__ == "__main__":
    asyncio.run(main())
```

### Step 8: Run All Tests (10 min)

```bash
pytest tests/ -v --tb=short
```

All tests should pass. Aim for at least 15 test cases across all modules.

---

## Expected Output

Running `pytest -v` should show:
```
tests/test_retry.py::test_success_on_first_try PASSED
tests/test_retry.py::test_success_after_retries PASSED
tests/test_retry.py::test_retry_exhausted PASSED
tests/test_retry.py::test_exponential_backoff_delay PASSED
tests/test_retry.py::test_non_retryable_exception PASSED
tests/test_streaming.py::test_simulate_stream PASSED
tests/test_streaming.py::test_accumulator PASSED
tests/test_streaming.py::test_stream_completion PASSED
tests/test_batch.py::test_all_items_processed PASSED
tests/test_batch.py::test_concurrency_limit PASSED
tests/test_batch.py::test_partial_failures PASSED
tests/test_tokens.py::test_known_token_count PASSED
tests/test_tokens.py::test_cost_calculation PASSED
tests/test_tokens.py::test_message_overhead PASSED
...
```

Running `python demo.py` should show structured log output, streaming text, batch progress, and cost estimates.

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **Type Hints** | 15% | Every function has complete type annotations |
| **Async Correctness** | 20% | Proper use of async/await, no race conditions |
| **Test Coverage** | 25% | At least 15 tests, covering happy path and edge cases |
| **Error Handling** | 20% | Custom exceptions, graceful degradation, clear error messages |
| **Code Organization** | 10% | Clean module boundaries, no circular imports |
| **Documentation** | 10% | Docstrings on all public functions, README with usage examples |

---

## Bonus Challenges

1. **Rate Limiter with Token Bucket**: Implement a proper token bucket rate limiter that tracks requests per minute (RPM) and tokens per minute (TPM) separately, matching OpenAI's actual rate limiting behavior.
2. **Circuit Breaker Pattern**: Implement a circuit breaker that opens (stops trying) after N consecutive failures and periodically tests if the service has recovered.
3. **Publish to PyPI**: Package your toolkit as a proper Python package and publish to TestPyPI. Practice the packaging workflow you will use professionally.
4. **Observability Dashboard**: Use `rich` to build a live terminal dashboard showing: active requests, success/failure rates, token usage, and estimated costs in real time.
5. **Async Generator Streaming**: Refactor the streaming module to use `async yield` chains, allowing middleware-style processing (e.g., stream -> filter profanity -> accumulate -> log).

---

## Key Concepts You Will Learn

- **Decorators**: Python's most powerful metaprogramming tool
- **async/await**: Concurrent I/O for making many API calls efficiently
- **Generators**: Lazy evaluation for processing streams without loading everything into memory
- **Type hints**: Essential for AI codebases where data shapes change often
- **Structured logging**: Machine-readable logs for debugging production AI systems
- **Exponential backoff**: The standard pattern for handling rate limits and transient failures
