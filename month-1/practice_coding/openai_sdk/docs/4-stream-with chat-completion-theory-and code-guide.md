# Quick Note Before We Start

You didn't answer the architecture exercise from Topic 2 — that's fine, no pressure. Just internalize this one line for now: **Option A (own your data) gives you resilience and control; Option B (Responses API) gives you simplicity and lower engineering overhead, at the cost of vendor dependency.** Most production teams in 2026 actually do both — Responses API for the UX, but they log a shadow copy of the conversation into their own DB for compliance and resilience. Keep that in your back pocket; we'll revisit it when we hit RAG and agent memory later in your roadmap.

---

## ⚠️ A Correction That Matters More Now Than Ever

In Topics 1 and 2, we used the **sync** `OpenAI` client inside `async def` route handlers. This is a mistake I let slide because it wasn't critical yet — but streaming makes it critical, so let's fix it now.

**Why this matters:** FastAPI's `async def` routes run on a single event loop. When you call the *sync* OpenAI client inside an async route, that call **blocks the entire event loop** until it returns. While one user's request is waiting on OpenAI, your server can't handle *any other user's request* — even completely unrelated ones. This defeats the entire purpose of using `async def`.

You already know this instinct from Node.js — it's identical to blocking the single-threaded event loop with a synchronous `fs.readFileSync()` call instead of the async version.

**The fix: use `AsyncOpenAI` everywhere in a FastAPI app.**

```python
# dependencies.py
from __future__ import annotations

from openai import AsyncOpenAI  # ← not OpenAI
from config import settings

_async_client = AsyncOpenAI(api_key=settings.openai_api_key)

def get_openai_client() -> AsyncOpenAI:
    return _async_client
```

And every service function becomes `async def` with `await`:

```python
# services/chat_service.py — only the call site changes
response = await client.chat.completions.create(...)   # ← await added
```

I'm flagging this now rather than making you rewrite three files today — we'll apply this fix live as part of Topic 3's code, since streaming *requires* the async client anyway (the sync client doesn't support async iteration over stream chunks). Consider Topics 1–2 conceptually correct but implementation-outdated; we're aligning them going forward.

---

## Prerequisites / Required Packages

```bash
# No new packages — AsyncOpenAI ships in the same openai package
# Just confirm your version supports it (it does, >= 1.0)
uv add "openai>=1.66.0"

# For testing SSE from the terminal (optional but useful)
uv add httpx
```

---

## The Intuition: What Streaming Actually Solves

You've watched ChatGPT type out responses word by word. Ask yourself: **why does OpenAI bother doing this instead of just waiting and sending the full response at once?**

The answer isn't about being fancy — it's about **perceived latency**. A GPT-4o response with 500 output tokens might take 8-10 seconds to fully generate. If you make the user stare at a blank screen for 10 seconds, that feels broken. If you show them text appearing progressively starting at 300ms, the *same total wait* feels instant and alive.

This is a UX psychology problem solved with an engineering technique. You already know this pattern from elsewhere — it's why video streaming doesn't wait for the entire file to download before playing, and why a well-built React app shows skeleton loaders instead of a blank white screen.

**The core technical fact you need to understand:** LLMs generate text **one token at a time**, autoregressively. This is fundamental to how transformers work (you covered this in your foundations). This means streaming isn't a special "mode" grafted on top — it's actually *closer* to how the model natively operates. The non-streaming API is the one doing extra work: it waits for every token to be generated, buffers them all server-side, and only then sends you the complete response.

---

## SSE vs WebSockets — The Decision You Need to Understand

As a frontend-heavy dev, you've likely used WebSockets before (chat apps, live notifications). It's natural to assume LLM streaming needs WebSockets too. It doesn't, and understanding why is important system-design knowledge.

| | **SSE (Server-Sent Events)** | **WebSockets** |
|---|---|---|
| Direction | One-way: server → client only | Bidirectional |
| Protocol | Plain HTTP | Separate `ws://` protocol, needs upgrade handshake |
| Reconnection | Automatic (built into browser `EventSource`) | Manual, you write it yourself |
| Proxy/firewall friendliness | Excellent — it's just HTTP | Can be blocked by corporate proxies |
| Use case fit | Server pushes data, client doesn't need to talk back mid-stream | True two-way real-time (chat, multiplayer, collaborative editing) |

**Why OpenAI uses SSE for streaming:** An LLM completion is inherently one-directional — you send one prompt, the server streams tokens back. You don't need to send data *back* mid-stream. SSE is the right tool, simpler than WebSockets, and it rides on plain HTTP, which means your existing FastAPI app, your load balancers, your API gateway — nothing special needs to change to support it.

**When would you actually need WebSockets in a GenAI app?** Multiplayer collaborative AI tools (like a shared AI whiteboard where multiple users see the model's output live), or when the client needs to interrupt/cancel generation mid-stream via a message *back* to the server. Keep this in mind — it'll matter later in your roadmap when you build voice/realtime features.

---

## How Streaming Works at the OpenAI SDK Level

Let's build this up piece by piece, starting outside of FastAPI so you see the raw mechanism clearly before we wrap it in a web layer.

**Step 1 — Non-streaming (what you already know from Topic 1), for comparison:**

```python
response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a haiku about async programming"}],
)
print(response.choices[0].message.content)  # Full text, all at once
```

**Step 2 — Add `stream=True`:**

```python
stream = await client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a haiku about async programming"}],
    stream=True,
)

async for chunk in stream:
    print(chunk)
```

Run this mentally and think about what you'd see. Instead of one response object, you get **many small chunk objects** — each one is a `ChatCompletionChunk`. Most of them look like this:

```python
ChatCompletionChunk(
    id='chatcmpl-abc123',
    choices=[Choice(delta=ChoiceDelta(content='Async', role=None), finish_reason=None)],
    ...
)
```

**Key insight:** the field is called `delta`, not `message`. That word is doing real work — it means "the *incremental change* since the last chunk," not "the full message so far." This is exactly like a Git diff vs a full file snapshot. Your job is to **accumulate these deltas** yourself.

**Step 3 — Extract just the text and accumulate it:**

```python
full_reply = ""

stream = await client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a haiku about async programming"}],
    stream=True,
)

async for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:  # delta can be None (e.g., on the role-announcing first chunk)
        full_reply += delta
        print(delta, end="", flush=True)  # typewriter effect in your terminal

print("\n\nFinal:", full_reply)
```

**Why the `if delta:` check?** The very first chunk in a stream often carries `role="assistant"` with `content=None` — it's just announcing "an assistant message is starting." If you don't guard against `None`, you'll get a `TypeError` trying to concatenate `None` to a string. This is the single most common beginner bug in streaming code.

**Step 4 — Detecting the end of the stream and why it matters:**

```python
async for chunk in stream:
    choice = chunk.choices[0]
    delta = choice.delta.content

    if delta:
        full_reply += delta

    if choice.finish_reason is not None:
        # This is the LAST chunk. finish_reason is only populated here.
        print(f"\nStream ended. Reason: {choice.finish_reason}")
```

`finish_reason` is `None` on every chunk *except the very last one*. This is your signal that generation is complete — same meaning as Topic 1 (`stop`, `length`, `tool_calls`), just delivered at a different moment in the flow.

---

## Streaming with the Responses API (Different Event Model)

Here's something that trips people up: **the Responses API doesn't stream raw text deltas the same way.** Instead, it streams **typed events** — this is actually a more sophisticated design because a single Responses API call might involve multiple types of output (text, tool calls, reasoning) and you need to know which kind of event you're looking at.

```python
stream = await client.responses.create(
    model="gpt-4o",
    input="Write a haiku about async programming",
    stream=True,
)

async for event in stream:
    match event.type:
        case "response.output_text.delta":
            print(event.delta, end="", flush=True)  # incremental text
        case "response.completed":
            print(f"\n\nDone. Final response ID: {event.response.id}")
        case _:
            pass  # other event types: tool calls, reasoning steps, etc.
```

**Why `match/case` here?** This is Python 3.10+ structural pattern matching — the modern, readable way to branch on event types instead of a chain of `if event.type == "..."`. Since you're aiming for current production style, this is exactly the kind of code a senior engineer writes today. Event-driven APIs like this (many event types, need to route on `.type`) are the textbook use case for `match`.

**The key architectural insight:** the Responses API's event stream is designed for **agentic workflows** — when you get to Tool Calling (Topic 4) and beyond, a single stream might contain text output *and* tool call events *and* status updates, all interleaved. The typed-event design scales to that complexity. Chat Completions' simpler delta model doesn't.

---

## Wiring This Into FastAPI — The SSE Endpoint

Now let's expose this over HTTP so your React frontend can consume it.

**Step 1 — The schema (minimal, since streaming responses aren't a single JSON blob):**

```python
# schemas/streaming.py
from __future__ import annotations

from pydantic import BaseModel, Field


class StreamChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    system_prompt: str | None = Field(default="You are a helpful assistant.")
    conversation_history: list[dict] | None = Field(default=None)
```

**Step 2 — The service layer: an async generator**

This is the core new concept. Instead of a function that `return`s a value, we write an **async generator** that `yield`s chunks as they arrive.

```python
# services/streaming_service.py
from __future__ import annotations

import json
from collections.abc import AsyncGenerator

from openai import AsyncOpenAI

from config import settings
from schemas.streaming import StreamChatRequest


async def stream_chat_completion(
    request: StreamChatRequest,
    client: AsyncOpenAI,
) -> AsyncGenerator[str, None]:
    """
    Yields Server-Sent Event formatted strings, one per token delta.

    SSE wire format is strict: each event MUST be:
        data: <payload>\n\n
    The double newline is what tells the browser "this event is complete."
    Missing it means the client will buffer forever waiting for more.
    """
    messages = [{"role": "system", "content": request.system_prompt}]

    if request.conversation_history:
        messages.extend(request.conversation_history)

    messages.append({"role": "user", "content": request.message})

    stream = await client.chat.completions.create(
        model=settings.default_model,
        messages=messages,
        stream=True,
        # Ask OpenAI to include token usage in the final chunk of the stream.
        # Without this flag, usage data is NOT available in streaming mode at all.
        stream_options={"include_usage": True},
    )

    async for chunk in stream:
        if not chunk.choices:
            # This is the special final usage-only chunk when include_usage=True
            if chunk.usage:
                usage_payload = {
                    "type": "usage",
                    "input_tokens": chunk.usage.prompt_tokens,
                    "output_tokens": chunk.usage.completion_tokens,
                }
                yield f"data: {json.dumps(usage_payload)}\n\n"
            continue

        delta = chunk.choices[0].delta.content
        if delta:
            payload = {"type": "token", "content": delta}
            yield f"data: {json.dumps(payload)}\n\n"

        finish_reason = chunk.choices[0].finish_reason
        if finish_reason:
            payload = {"type": "done", "finish_reason": finish_reason}
            yield f"data: {json.dumps(payload)}\n\n"

    # SSE convention: signal true stream termination to the client
    yield "data: [DONE]\n\n"
```

**Why JSON-wrap every event instead of sending raw text?** Because in a real app, you need to distinguish "this is a text token" from "this is usage info" from "this is a tool call event" (later). A typed envelope (`{"type": "token", ...}`) is the production pattern — it lets your frontend `switch` on `type` instead of guessing from raw string shape. This is the same reasoning behind `match event.type` above — typed messages over a stream, not ambiguous raw strings.

**Why `stream_options={"include_usage": True}`?** By default, streaming responses **do not include token usage** — a genuinely surprising gotcha. If you need cost tracking (and in production, you always do), you must explicitly opt in with this flag. Without it, you'd have no idea how many tokens a streamed response cost you.

**Step 3 — The router using `StreamingResponse`:**

```python
# routers/streaming.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

from dependencies import get_openai_client
from schemas.streaming import StreamChatRequest
from services.streaming_service import stream_chat_completion

router = APIRouter()


@router.post(
    "/chat/stream",
    summary="Streaming chat via Server-Sent Events",
    description="Streams the assistant's reply token-by-token using SSE.",
)
async def stream_chat_endpoint(
    request: StreamChatRequest,
    client: AsyncOpenAI = Depends(get_openai_client),
) -> StreamingResponse:
    return StreamingResponse(
        stream_chat_completion(request, client),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # Disables buffering on nginx reverse proxies — CRITICAL in production.
            # Without this header, nginx buffers the whole response before sending
            # it to the client, completely defeating the purpose of streaming.
            "X-Accel-Buffering": "no",
        },
    )
```

**That `X-Accel-Buffering: no` header is one of the most commonly missed production bugs.** Your code works perfectly on `localhost`. You deploy behind nginx (extremely common — EC2, DigitalOcean, most self-managed infra). Suddenly streaming appears completely broken — the client gets one giant chunk instead of a smooth stream. The bug is invisible in your FastAPI code; it's nginx buffering the entire response before forwarding it. This single header fixes it. Remember this — it's a real interview "gotcha" question for backend GenAI roles.

---

## The React Side — Consuming the Stream

This is where your existing strength kicks in. One important fact first: **the browser's built-in `EventSource` only supports GET requests** — it cannot send a JSON body. Since our endpoint is a `POST` (we need to send the message and history), we can't use `EventSource` directly. Instead, we use the modern `fetch` + `ReadableStream` approach, which is what production chat UIs actually use.

```jsx
// useStreamingChat.js
import { useState, useCallback } from "react";

export function useStreamingChat() {
  const [reply, setReply] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = useCallback(async (message, history = []) => {
    setReply("");
    setIsStreaming(true);

    const response = await fetch("/api/v1/chat/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, conversation_history: history }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // SSE events are separated by \n\n — split and process complete events only
      const events = buffer.split("\n\n");
      buffer = events.pop(); // last item may be an incomplete event — keep in buffer

      for (const event of events) {
        if (!event.startsWith("data: ")) continue;
        const raw = event.slice(6); // strip "data: " prefix

        if (raw === "[DONE]") {
          setIsStreaming(false);
          continue;
        }

        const parsed = JSON.parse(raw);

        if (parsed.type === "token") {
          setReply((prev) => prev + parsed.content); // typewriter effect
        } else if (parsed.type === "usage") {
          console.log("Tokens used:", parsed.input_tokens, parsed.output_tokens);
        }
      }
    }
  }, []);

  return { reply, isStreaming, sendMessage };
}
```

**Why the `buffer` variable and the `.pop()` trick?** TCP/HTTP chunks don't respect your SSE event boundaries — a single network chunk might contain half of one event and all of the next. You cannot assume `value` from `reader.read()` lines up neatly with your `data: ...\n\n` events. The buffer pattern handles partial events correctly: you split on `\n\n`, process every *complete* event, and keep the last (possibly incomplete) fragment in the buffer for the next iteration. **This is the #1 bug in hand-rolled SSE parsers** — people forget this and get garbled JSON parse errors intermittently in production, especially under slow networks.

A component using this hook:

```jsx
function ChatBox() {
  const { reply, isStreaming, sendMessage } = useStreamingChat();

  return (
    <div>
      <button onClick={() => sendMessage("Explain event loops")} disabled={isStreaming}>
        Ask
      </button>
      <p>{reply}{isStreaming && <span className="cursor-blink">▋</span>}</p>
    </div>
  );
}
```

That blinking cursor span is the actual trick behind the "typing" visual effect you see in ChatGPT — it's pure CSS, not anything special from the API.

---

## Common Beginner Mistakes

1. **Using the sync `OpenAI` client instead of `AsyncOpenAI`** — blocks your event loop, kills concurrency under load. We fixed this above.
2. **Forgetting `if delta:` before concatenating** — crashes on the role-announcement chunk with `content=None`.
3. **Missing `stream_options={"include_usage": True}`** — silently lose cost-tracking data.
4. **Forgetting `X-Accel-Buffering: no`** — works locally, breaks in production behind nginx.
5. **Not buffering partial SSE events on the client** — intermittent JSON parse errors that are hard to reproduce.
6. **Using `EventSource` for a POST-based stream** — it literally cannot send a request body; a common but wrong first instinct.
7. **Not handling client disconnects** — if a user closes the tab mid-stream, your FastAPI generator should stop cleanly rather than continuing to burn OpenAI tokens generating a response nobody will see. (FastAPI handles this via `request.is_disconnected()` — worth knowing exists, we can go deeper if you want a dedicated look.)

---

## Updated Project State

```
openai_service/
├── main.py                     ← add streaming router
├── dependencies.py             ✅ Fixed (AsyncOpenAI)
├── routers/
│   ├── chat.py
│   ├── responses.py
│   └── streaming.py            ✅ New
├── schemas/
│   ├── chat.py
│   ├── responses.py
│   └── streaming.py            ✅ New
└── services/
    ├── chat_service.py         ⚠️ needs await + AsyncOpenAI update
    ├── responses_service.py    ⚠️ needs await + AsyncOpenAI update
    └── streaming_service.py    ✅ New
```

---

## Mini Exercise

Here's a real scenario to reason through, not code:

Your streaming endpoint is live. A user starts a long response, then **closes their browser tab** 2 seconds in. Your FastAPI generator is still running, still calling `async for chunk in stream`, still consuming OpenAI tokens for a response nobody will ever see.

**Question:** What's the actual cost impact of this at scale — say, 10,000 users a day, 5% of whom close the tab mid-response? And what would you check for, on every loop iteration in `stream_chat_completion`, to stop early? (You don't need exact code — just describe what condition you'd check and where you'd get that information from in FastAPI.)

---

Let me know when you're ready for **Topic 4: Function / Tool Calling** — that's where this whole SDK starts feeling like building actual agents instead of chatbots.