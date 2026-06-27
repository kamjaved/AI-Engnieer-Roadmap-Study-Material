# Assignment 3.2: Multi-Provider API Lab

> **Week 3** | [Back to Week 3 Plan](../week-3.md)

## Title
**Multi-Provider API Lab** -- Build a Provider Abstraction Layer

## Objective
Build a production-grade Python library that provides a unified interface across OpenAI, Anthropic, and Google Gemini. Implement intelligent fallback (if one provider fails, try the next), task-based routing (cheap models for simple tasks, powerful models for complex ones), per-request cost tracking, and streaming support across all providers. This is the kind of infrastructure layer that AI companies build internally.

## Difficulty
Intermediate-Advanced

## Estimated Time
4-5 hours

## Prerequisites
- Python 3.10+ installed
- Completed Assignment 2.1 (Python AI Toolkit -- retry logic, async patterns)
- API keys for at least 2 of: OpenAI, Anthropic, Google Gemini
- Install dependencies:
```bash
pip install openai anthropic google-generativeai httpx pydantic rich structlog
```

## Why This Matters
In production AI systems, you never rely on a single provider:
- **Outages**: OpenAI goes down, your app keeps working via Anthropic
- **Cost optimization**: Use GPT-4o-mini for simple tasks, Claude for complex reasoning
- **Rate limits**: Distribute load across providers
- **Capability matching**: Some models are better at code, others at creative writing
- **Vendor lock-in avoidance**: Swap providers without changing application code

This is the exact pattern used by libraries like LiteLLM, but building it yourself teaches you what is happening under the hood.

---

## Detailed Instructions

### Step 1: Project Setup (10 min)

```
multi-provider-lab/
  providers/
    __init__.py
    base.py          # Abstract base class
    openai_provider.py
    anthropic_provider.py
    gemini_provider.py
    mock_provider.py
  routing/
    __init__.py
    router.py        # Task-based routing
    fallback.py      # Fallback chain logic
  tracking/
    __init__.py
    cost_tracker.py  # Per-request cost tracking
  models/
    __init__.py
    messages.py      # Unified message format
    config.py        # Provider configurations
  tests/
    __init__.py
    test_providers.py
    test_router.py
    test_fallback.py
    test_cost_tracker.py
  demo.py
  pyproject.toml
```

### Step 2: Define the Unified Message Format (20 min)

In `models/messages.py`:

```python
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import AsyncIterator


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    role: Role
    content: str


class CompletionRequest(BaseModel):
    """Provider-agnostic completion request."""
    messages: list[Message]
    model: str | None = None  # None = use provider's default
    temperature: float = 0.7
    max_tokens: int = 1024
    stream: bool = False
    metadata: dict = Field(default_factory=dict)


class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    """Provider-agnostic completion response."""
    content: str
    model: str
    provider: str
    usage: TokenUsage
    finish_reason: str = "stop"
    latency_ms: float = 0.0
    cost: float = 0.0  # Estimated cost in USD
    request_id: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StreamChunk(BaseModel):
    """A single chunk from a streaming response."""
    content: str
    provider: str
    model: str
    finish_reason: str | None = None


class ProviderStatus(BaseModel):
    """Health status of a provider."""
    name: str
    is_available: bool
    last_error: str | None = None
    last_success: datetime | None = None
    error_count: int = 0
    avg_latency_ms: float = 0.0
```

### Step 3: Define the Provider Interface (15 min)

In `providers/base.py`:

```python
from abc import ABC, abstractmethod
from typing import AsyncIterator
from models.messages import (
    CompletionRequest, CompletionResponse, StreamChunk, ProviderStatus
)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name (e.g., 'openai', 'anthropic')."""
        ...

    @property
    @abstractmethod
    def available_models(self) -> list[str]:
        """List of models this provider supports."""
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Default model to use if none specified."""
        ...

    @abstractmethod
    async def complete(
        self, request: CompletionRequest
    ) -> CompletionResponse:
        """Send a completion request and return the response."""
        ...

    @abstractmethod
    async def stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[StreamChunk]:
        """Stream a completion response."""
        ...

    @abstractmethod
    async def health_check(self) -> ProviderStatus:
        """Check if the provider is available."""
        ...

    def supports_model(self, model: str) -> bool:
        """Check if this provider supports the given model."""
        return model in self.available_models

    def estimate_cost(
        self, prompt_tokens: int, completion_tokens: int, model: str
    ) -> float:
        """Estimate cost in USD. Override per provider."""
        return 0.0
```

### Step 4: Implement the Providers (60 min)

In `providers/openai_provider.py`:

```python
import time
from typing import AsyncIterator
from openai import AsyncOpenAI
from providers.base import LLMProvider
from models.messages import (
    CompletionRequest, CompletionResponse, StreamChunk,
    TokenUsage, ProviderStatus
)


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    PRICING = {  # per 1M tokens (input, output)
        "gpt-4o": (2.50, 10.00),
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4-turbo": (10.00, 30.00),
        "gpt-3.5-turbo": (0.50, 1.50),
    }

    def __init__(self, api_key: str | None = None):
        self.client = AsyncOpenAI(api_key=api_key)

    @property
    def name(self) -> str:
        return "openai"

    @property
    def available_models(self) -> list[str]:
        return list(self.PRICING.keys())

    @property
    def default_model(self) -> str:
        return "gpt-4o-mini"

    def estimate_cost(
        self, prompt_tokens: int, completion_tokens: int, model: str
    ) -> float:
        pricing = self.PRICING.get(model, (0.0, 0.0))
        input_cost = prompt_tokens * pricing[0] / 1_000_000
        output_cost = completion_tokens * pricing[1] / 1_000_000
        return input_cost + output_cost

    async def complete(
        self, request: CompletionRequest
    ) -> CompletionResponse:
        model = request.model or self.default_model
        messages = [
            {"role": m.role.value, "content": m.content}
            for m in request.messages
        ]

        start = time.time()
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        latency = (time.time() - start) * 1000

        usage = response.usage
        cost = self.estimate_cost(
            usage.prompt_tokens, usage.completion_tokens, model
        )

        return CompletionResponse(
            content=response.choices[0].message.content or "",
            model=model,
            provider=self.name,
            usage=TokenUsage(
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
            ),
            finish_reason=response.choices[0].finish_reason or "stop",
            latency_ms=latency,
            cost=cost,
            request_id=response.id,
        )

    async def stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[StreamChunk]:
        model = request.model or self.default_model
        messages = [
            {"role": m.role.value, "content": m.content}
            for m in request.messages
        ]

        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield StreamChunk(
                    content=chunk.choices[0].delta.content,
                    provider=self.name,
                    model=model,
                    finish_reason=chunk.choices[0].finish_reason,
                )

    async def health_check(self) -> ProviderStatus:
        try:
            start = time.time()
            await self.client.models.list()
            latency = (time.time() - start) * 1000
            return ProviderStatus(
                name=self.name,
                is_available=True,
                avg_latency_ms=latency,
            )
        except Exception as e:
            return ProviderStatus(
                name=self.name,
                is_available=False,
                last_error=str(e),
            )
```

Now implement `anthropic_provider.py` and `gemini_provider.py` following the same pattern. Key differences:

**Anthropic**: System messages are separated from the message list. Use `anthropic.AsyncAnthropic`. The API uses `input_tokens` / `output_tokens` instead of `prompt_tokens` / `completion_tokens`.

**Gemini**: Uses `google.generativeai`. The message format is different (uses `parts` instead of `content`). System instructions go in the model configuration.

Also implement `mock_provider.py` for testing without API keys:

```python
import asyncio
import time
import uuid
from typing import AsyncIterator
from providers.base import LLMProvider
from models.messages import (
    CompletionRequest, CompletionResponse, StreamChunk,
    TokenUsage, ProviderStatus
)


class MockProvider(LLMProvider):
    """Mock provider for testing. Configurable behavior."""

    def __init__(
        self,
        name: str = "mock",
        latency: float = 0.1,
        fail_rate: float = 0.0,
        fail_after: int | None = None,
    ):
        self._name = name
        self.latency = latency
        self.fail_rate = fail_rate
        self.fail_after = fail_after
        self._call_count = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def available_models(self) -> list[str]:
        return ["mock-fast", "mock-smart"]

    @property
    def default_model(self) -> str:
        return "mock-fast"

    async def complete(
        self, request: CompletionRequest
    ) -> CompletionResponse:
        self._call_count += 1
        await asyncio.sleep(self.latency)

        import random
        if random.random() < self.fail_rate:
            raise ConnectionError(f"{self._name} simulated failure")
        if self.fail_after and self._call_count > self.fail_after:
            raise ConnectionError(f"{self._name} exhausted after {self.fail_after} calls")

        user_msg = next(
            (m.content for m in reversed(request.messages) if m.role.value == "user"),
            "no message"
        )
        return CompletionResponse(
            content=f"[{self._name}] Response to: {user_msg[:50]}",
            model=request.model or self.default_model,
            provider=self.name,
            usage=TokenUsage(prompt_tokens=20, completion_tokens=15, total_tokens=35),
            latency_ms=self.latency * 1000,
            cost=0.0001,
            request_id=uuid.uuid4().hex[:8],
        )

    async def stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[StreamChunk]:
        words = f"[{self._name}] This is a mock streaming response".split()
        for i, word in enumerate(words):
            await asyncio.sleep(0.02)
            yield StreamChunk(
                content=word + " ",
                provider=self.name,
                model=request.model or self.default_model,
                finish_reason="stop" if i == len(words) - 1 else None,
            )

    async def health_check(self) -> ProviderStatus:
        return ProviderStatus(name=self.name, is_available=True, avg_latency_ms=10)
```

### Step 5: Build the Fallback Chain (40 min)

In `routing/fallback.py`:

```python
import structlog
from typing import AsyncIterator
from providers.base import LLMProvider
from models.messages import (
    CompletionRequest, CompletionResponse, StreamChunk, ProviderStatus
)

logger = structlog.get_logger()


class FallbackChain:
    """
    Tries providers in order. If one fails, falls back to the next.

    Usage:
        chain = FallbackChain([openai, anthropic, gemini])
        response = await chain.complete(request)
    """

    def __init__(
        self,
        providers: list[LLMProvider],
        max_retries_per_provider: int = 1,
    ):
        self.providers = providers
        self.max_retries = max_retries_per_provider
        self._provider_status: dict[str, ProviderStatus] = {}

    async def complete(
        self, request: CompletionRequest
    ) -> CompletionResponse:
        """Try each provider in order until one succeeds."""
        errors: list[tuple[str, Exception]] = []

        for provider in self.providers:
            for attempt in range(self.max_retries + 1):
                try:
                    logger.info(
                        "attempting_provider",
                        provider=provider.name,
                        attempt=attempt + 1,
                    )
                    response = await provider.complete(request)

                    # Update status on success
                    self._provider_status[provider.name] = ProviderStatus(
                        name=provider.name,
                        is_available=True,
                        avg_latency_ms=response.latency_ms,
                    )

                    if errors:
                        logger.warning(
                            "fallback_succeeded",
                            failed_providers=[e[0] for e in errors],
                            succeeded_provider=provider.name,
                        )
                    return response

                except Exception as e:
                    errors.append((provider.name, e))
                    logger.warning(
                        "provider_failed",
                        provider=provider.name,
                        attempt=attempt + 1,
                        error=str(e),
                    )

                    # Update status on failure
                    prev = self._provider_status.get(provider.name)
                    self._provider_status[provider.name] = ProviderStatus(
                        name=provider.name,
                        is_available=False,
                        last_error=str(e),
                        error_count=(prev.error_count + 1) if prev else 1,
                    )

        # All providers failed
        error_summary = "; ".join(
            f"{name}: {err}" for name, err in errors
        )
        raise RuntimeError(
            f"All providers failed. Errors: {error_summary}"
        )

    async def stream(
        self, request: CompletionRequest
    ) -> AsyncIterator[StreamChunk]:
        """Stream from the first available provider."""
        errors = []

        for provider in self.providers:
            try:
                async for chunk in provider.stream(request):
                    yield chunk
                return  # Success - exit after streaming completes
            except Exception as e:
                errors.append((provider.name, e))
                logger.warning(
                    "stream_fallback",
                    provider=provider.name,
                    error=str(e),
                )

        error_summary = "; ".join(f"{n}: {e}" for n, e in errors)
        raise RuntimeError(f"All providers failed streaming: {error_summary}")

    async def health_check_all(self) -> dict[str, ProviderStatus]:
        """Check health of all providers."""
        results = {}
        for provider in self.providers:
            results[provider.name] = await provider.health_check()
        return results

    @property
    def status(self) -> dict[str, ProviderStatus]:
        return self._provider_status
```

### Step 6: Build the Task Router (40 min)

In `routing/router.py`:

```python
import re
from enum import Enum
from pydantic import BaseModel, Field
from providers.base import LLMProvider
from models.messages import CompletionRequest, CompletionResponse, Message


class TaskComplexity(str, Enum):
    SIMPLE = "simple"     # Classification, yes/no, short answers
    MODERATE = "moderate"  # Summarization, translation, short generation
    COMPLEX = "complex"    # Reasoning, code generation, long-form writing
    CRITICAL = "critical"  # High-stakes decisions, multi-step reasoning


class RoutingRule(BaseModel):
    """Maps task complexity to a specific provider and model."""
    complexity: TaskComplexity
    provider: str
    model: str
    max_tokens: int = 1024
    temperature: float = 0.7


class TaskRouter:
    """
    Routes requests to providers based on task complexity.

    Simple tasks go to cheap/fast models.
    Complex tasks go to powerful/expensive models.
    """

    def __init__(
        self,
        providers: dict[str, LLMProvider],
        rules: list[RoutingRule],
    ):
        self.providers = providers
        self.rules = {rule.complexity: rule for rule in rules}

    def classify_complexity(self, request: CompletionRequest) -> TaskComplexity:
        """
        Heuristically classify the complexity of a request.
        In production, you might use an LLM for this classification.
        """
        user_messages = [
            m.content for m in request.messages if m.role.value == "user"
        ]
        if not user_messages:
            return TaskComplexity.SIMPLE

        last_message = user_messages[-1].lower()
        total_length = sum(len(m.content) for m in request.messages)

        # Heuristic rules
        complex_indicators = [
            r"\banalyze\b", r"\bcompare\b", r"\bexplain.*detail",
            r"\bwrite.*code\b", r"\bimplement\b", r"\bdebug\b",
            r"\bstep.by.step\b", r"\breason\b", r"\bprove\b",
            r"\barchitect\b", r"\bdesign.*system\b",
        ]
        moderate_indicators = [
            r"\bsummarize\b", r"\btranslate\b", r"\brewrite\b",
            r"\blist\b", r"\bdescribe\b", r"\bconvert\b",
        ]
        simple_indicators = [
            r"\byes or no\b", r"\bclassify\b", r"\btrue or false\b",
            r"\bhow many\b", r"\bwhat is\b", r"\bdefine\b",
        ]

        for pattern in complex_indicators:
            if re.search(pattern, last_message):
                return TaskComplexity.COMPLEX

        for pattern in moderate_indicators:
            if re.search(pattern, last_message):
                return TaskComplexity.MODERATE

        for pattern in simple_indicators:
            if re.search(pattern, last_message):
                return TaskComplexity.SIMPLE

        # Length-based fallback
        if total_length > 2000:
            return TaskComplexity.COMPLEX
        elif total_length > 500:
            return TaskComplexity.MODERATE
        return TaskComplexity.SIMPLE

    async def route(
        self, request: CompletionRequest
    ) -> CompletionResponse:
        """Route request to the appropriate provider based on complexity."""
        complexity = request.metadata.get("complexity")
        if complexity:
            complexity = TaskComplexity(complexity)
        else:
            complexity = self.classify_complexity(request)

        rule = self.rules.get(complexity)
        if not rule:
            raise ValueError(f"No routing rule for complexity: {complexity}")

        provider = self.providers.get(rule.provider)
        if not provider:
            raise ValueError(f"Provider not found: {rule.provider}")

        # Override model and parameters from routing rule
        routed_request = request.model_copy(update={
            "model": rule.model,
            "max_tokens": min(request.max_tokens, rule.max_tokens),
            "metadata": {
                **request.metadata,
                "routed_complexity": complexity.value,
                "routed_provider": rule.provider,
                "routed_model": rule.model,
            },
        })

        return await provider.complete(routed_request)
```

### Step 7: Build the Cost Tracker (30 min)

In `tracking/cost_tracker.py`:

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
from models.messages import CompletionResponse
from rich.console import Console
from rich.table import Table


@dataclass
class CostEntry:
    timestamp: datetime
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost: float
    latency_ms: float


class CostTracker:
    """Track per-request costs across providers."""

    def __init__(self):
        self.entries: list[CostEntry] = []
        self._by_provider: dict[str, list[CostEntry]] = defaultdict(list)
        self._by_model: dict[str, list[CostEntry]] = defaultdict(list)

    def record(self, response: CompletionResponse) -> None:
        """Record a completed request."""
        entry = CostEntry(
            timestamp=response.timestamp,
            provider=response.provider,
            model=response.model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            cost=response.cost,
            latency_ms=response.latency_ms,
        )
        self.entries.append(entry)
        self._by_provider[response.provider].append(entry)
        self._by_model[response.model].append(entry)

    @property
    def total_cost(self) -> float:
        return sum(e.cost for e in self.entries)

    @property
    def total_tokens(self) -> int:
        return sum(
            e.prompt_tokens + e.completion_tokens for e in self.entries
        )

    @property
    def total_requests(self) -> int:
        return len(self.entries)

    def cost_by_provider(self) -> dict[str, float]:
        return {
            provider: sum(e.cost for e in entries)
            for provider, entries in self._by_provider.items()
        }

    def cost_by_model(self) -> dict[str, float]:
        return {
            model: sum(e.cost for e in entries)
            for model, entries in self._by_model.items()
        }

    def cost_last_n_minutes(self, minutes: int = 60) -> float:
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        return sum(
            e.cost for e in self.entries if e.timestamp > cutoff
        )

    def avg_latency_by_provider(self) -> dict[str, float]:
        result = {}
        for provider, entries in self._by_provider.items():
            if entries:
                result[provider] = sum(e.latency_ms for e in entries) / len(entries)
        return result

    def print_summary(self) -> None:
        """Print a rich summary table."""
        console = Console()
        console.rule("[bold]Cost Tracker Summary[/bold]")

        table = Table(title="Cost by Provider")
        table.add_column("Provider", style="cyan")
        table.add_column("Requests", justify="right")
        table.add_column("Tokens", justify="right")
        table.add_column("Cost", justify="right", style="green")
        table.add_column("Avg Latency", justify="right")

        for provider, entries in self._by_provider.items():
            tokens = sum(e.prompt_tokens + e.completion_tokens for e in entries)
            cost = sum(e.cost for e in entries)
            avg_lat = sum(e.latency_ms for e in entries) / len(entries) if entries else 0
            table.add_row(
                provider,
                str(len(entries)),
                f"{tokens:,}",
                f"${cost:.6f}",
                f"{avg_lat:.0f}ms",
            )

        console.print(table)
        console.print(f"\n[bold]Total cost: ${self.total_cost:.6f}[/bold]")
        console.print(f"[bold]Total requests: {self.total_requests}[/bold]")
        console.print(f"[bold]Total tokens: {self.total_tokens:,}[/bold]")
```

### Step 8: Integration Demo and Tests (30 min)

In `demo.py`:

```python
import asyncio
from providers.mock_provider import MockProvider
from routing.fallback import FallbackChain
from routing.router import TaskRouter, RoutingRule, TaskComplexity
from tracking.cost_tracker import CostTracker
from models.messages import CompletionRequest, Message, Role


async def demo_fallback():
    """Demo: Provider A fails, falls back to Provider B."""
    print("=" * 60)
    print("DEMO: Fallback Chain")
    print("=" * 60)

    # Provider 1 fails after 2 calls, Provider 2 always works
    provider_a = MockProvider(name="primary", fail_rate=0.7, latency=0.05)
    provider_b = MockProvider(name="backup", latency=0.1)

    chain = FallbackChain([provider_a, provider_b])
    tracker = CostTracker()

    for i in range(5):
        request = CompletionRequest(
            messages=[Message(role=Role.USER, content=f"Question {i+1}")]
        )
        response = await chain.complete(request)
        tracker.record(response)
        print(f"  Request {i+1}: Handled by [{response.provider}]")

    tracker.print_summary()


async def demo_routing():
    """Demo: Route by task complexity."""
    print("\n" + "=" * 60)
    print("DEMO: Task-Based Routing")
    print("=" * 60)

    cheap = MockProvider(name="cheap-provider", latency=0.02)
    smart = MockProvider(name="smart-provider", latency=0.2)

    router = TaskRouter(
        providers={"cheap": cheap, "smart": smart},
        rules=[
            RoutingRule(
                complexity=TaskComplexity.SIMPLE,
                provider="cheap", model="mock-fast",
                max_tokens=256, temperature=0.3,
            ),
            RoutingRule(
                complexity=TaskComplexity.MODERATE,
                provider="cheap", model="mock-fast",
                max_tokens=512, temperature=0.5,
            ),
            RoutingRule(
                complexity=TaskComplexity.COMPLEX,
                provider="smart", model="mock-smart",
                max_tokens=2048, temperature=0.7,
            ),
            RoutingRule(
                complexity=TaskComplexity.CRITICAL,
                provider="smart", model="mock-smart",
                max_tokens=4096, temperature=0.2,
            ),
        ],
    )

    test_prompts = [
        ("What is Python?", TaskComplexity.SIMPLE),
        ("Summarize the history of AI in 3 paragraphs", TaskComplexity.MODERATE),
        ("Implement a binary search tree in Python with balancing", TaskComplexity.COMPLEX),
        ("Classify this email: 'Hello, nice day'", TaskComplexity.SIMPLE),
    ]

    tracker = CostTracker()
    for prompt, expected in test_prompts:
        request = CompletionRequest(
            messages=[Message(role=Role.USER, content=prompt)]
        )
        classified = router.classify_complexity(request)
        response = await router.route(request)
        tracker.record(response)
        print(
            f"  '{prompt[:45]}...' -> "
            f"Classified: {classified.value}, "
            f"Routed to: [{response.provider}]"
        )

    tracker.print_summary()


async def demo_streaming():
    """Demo: Streaming across providers."""
    print("\n" + "=" * 60)
    print("DEMO: Streaming with Fallback")
    print("=" * 60)

    provider = MockProvider(name="stream-provider")
    chain = FallbackChain([provider])

    request = CompletionRequest(
        messages=[Message(role=Role.USER, content="Tell me about Python")],
        stream=True,
    )

    print("  Streaming: ", end="")
    async for chunk in chain.stream(request):
        print(chunk.content, end="", flush=True)
    print()


async def main():
    await demo_fallback()
    await demo_routing()
    await demo_streaming()


if __name__ == "__main__":
    asyncio.run(main())
```

Write tests in `tests/` that verify:
- Fallback chain tries providers in order
- Fallback chain succeeds when first provider fails but second succeeds
- Fallback chain raises when all providers fail
- Task router classifies complexity correctly for known patterns
- Cost tracker accumulates costs accurately
- Streaming yields all chunks

---

## Expected Output

Running `python demo.py` should show:

```
============================================================
DEMO: Fallback Chain
============================================================
  Request 1: Handled by [primary]
  Request 2: Handled by [backup]     (primary failed, fell back)
  Request 3: Handled by [primary]
  ...

          Cost by Provider
┌──────────┬──────────┬────────┬──────────┬─────────────┐
│ Provider │ Requests │ Tokens │ Cost     │ Avg Latency │
├──────────┼──────────┼────────┼──────────┼─────────────┤
│ primary  │ 3        │ 105    │ $0.0003  │ 50ms        │
│ backup   │ 2        │ 70     │ $0.0002  │ 100ms       │
└──────────┴──────────┴────────┴──────────┴─────────────┘
```

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **Provider Implementation** | 25% | At least 2 real providers + mock, all following the interface |
| **Fallback Logic** | 20% | Correct fallback behavior, proper error propagation, logging |
| **Routing Logic** | 20% | Complexity classification works, routing rules applied correctly |
| **Cost Tracking** | 15% | Accurate per-request, per-provider, per-model cost tracking |
| **Streaming** | 10% | Streaming works through the abstraction layer |
| **Tests** | 10% | At least 8 tests covering fallback, routing, and tracking |

---

## Bonus Challenges

1. **Adaptive Routing**: Track each provider's error rate and latency in real time. Automatically demote providers that are slow or failing. Promote them back when they recover (circuit breaker pattern).
2. **Cost Budgeting**: Add a budget system. Set a daily budget (e.g., $5.00). When the budget is 80% consumed, automatically downgrade to cheaper models. When exhausted, reject requests.
3. **Provider Load Balancing**: Instead of fallback (try in order), implement round-robin or least-connections load balancing across healthy providers.
4. **LiteLLM Comparison**: Install the `litellm` library and compare its interface to yours. Document what features LiteLLM has that yours does not, and vice versa.
5. **Caching Layer**: Add a semantic cache -- before calling any provider, embed the request and check if a similar request was recently answered. Use a similarity threshold to decide whether to return the cached response.

---

## Key Concepts You Will Learn

- **Provider abstraction**: Decoupling your app from specific AI providers
- **Fallback patterns**: Resilience through redundancy
- **Task-based routing**: Optimizing cost and quality by matching tasks to models
- **Cost management**: Essential for any production AI system
- **Streaming across abstractions**: Maintaining async iterators through middleware layers
- **Circuit breaker pattern**: Protecting your app from cascading failures
