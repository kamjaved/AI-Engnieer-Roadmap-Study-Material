# Memory, Context, History, and Checkpointing in LangChain/LangGraph — A Production Architecture Deep Dive

> Note on freshness: LangGraph and LangChain ship breaking changes frequently. The APIs below reflect the stable, idiomatic patterns as of early 2026 (`langgraph` 0.2/0.3+ line, Postgres checkpointer + Store API, `add_messages` reducer). Before you ship, diff against the current `langchain-ai/langgraph` docs — treat this as architecture-correct, verify signatures.

---

## 1. First Principles

The reason engineers get confused here is that four genuinely different concepts get flattened into one word — "memory" — in casual conversation. They live at different layers of the stack, and conflating them is what makes production systems buggy. Let's separate them precisely.

**Context** is the literal set of tokens you send to the LLM in a single inference call. It is ephemeral — it exists only for the duration of that one forward pass. Context = system prompt + retrieved documents + tool schemas + conversation turns + the current user message, all serialized into the model's input. The LLM itself is stateless: it has no idea a previous call ever happened unless you re-supply everything it needs to know, every single time, inside this token window. This is the single most important fact to internalize — every "memory" system you build is really just an engineering pipeline whose job is to **assemble context correctly for the next call**.

**Conversation history** is the raw, ordered log of messages exchanged in a thread — every `HumanMessage`, `AIMessage`, `ToolMessage`, `SystemMessage`. It is a *data structure*, typically append-only, and it is *not* the same thing as context. History is the full, unabridged truth of what was said. Context is a *derived, filtered, possibly compressed view* of that history that you choose to send to the model on a given turn. You almost never send raw, unbounded history as context in production — you transform it first.

**Memory** is the strategy layer that decides how conversation history (and other state) gets turned into context. Memory is not storage — it's policy. "Keep the last 10 turns," "summarize anything older than 20 turns," "extract durable facts about the user and retrieve them semantically" — these are all memory strategies. LangChain's various `Memory` classes, and LangGraph's `Store` API, are implementations of this policy layer. Memory typically splits into two scopes: **short-term memory** (continuity within a single thread/session — usually just managed history) and **long-term memory** (durable knowledge that survives across threads and sessions — user preferences, extracted facts, prior project context).

**Checkpoint** is an infrastructure-level concept, specific to stateful graph execution engines like LangGraph. A checkpoint is a complete, serialized snapshot of a graph's execution state at a given step — not just messages, but *every* state channel your graph defines (messages, retrieved docs, scratch variables, pending tool calls, which node runs next). Checkpointing exists to solve a different problem than memory: **durable execution**. It answers "if my server crashes mid-agent-loop, or a human needs to approve a tool call, or I want to replay a run for debugging, how do I resume exactly where I left off?" That's an operational/reliability concern, not an information-design concern.

Why are these four different things instead of one? Because they solve different engineering problems and have different failure modes. Context has a hard token ceiling and a cost/latency curve. History has unbounded growth and is your source of truth. Memory is a lossy compression/retrieval decision that trades fidelity for cost and relevance. Checkpointing is about crash-safety, resumability, and time-travel — it would exist even for an agent that has *no* conversational memory at all (e.g., a long-running data pipeline agent). If you merge these concepts in your mental model, you'll build systems that either blow their token budget, lose state on redeploys, or can't debug production issues because there's no snapshot history to inspect.

---

## 2. Anatomy of a Single Message Turn

Walk through exactly what happens, in order, when a user hits send. This is the sequence a senior engineer should be able to draw on a whiteboard from memory.

**Step 1 — Ingress.** The message arrives at your API (FastAPI endpoint). It carries a `thread_id` (identifying the conversation) and possibly a `user_id` (identifying the person, for long-term memory scoping). At this point you have raw text and two identifiers — nothing else is loaded yet.

**Step 2 — Checkpoint load (this is where conversation history is loaded).** You invoke the compiled LangGraph graph with `config={"configurable": {"thread_id": thread_id}}`. Before your graph runs a single node, the checkpointer (e.g. `AsyncPostgresSaver`) fetches the *latest checkpoint* for that `thread_id` from Postgres. This checkpoint contains the full prior state — critically, the `messages` channel, which is your conversation history up to this point. This is the exact moment history re-enters your process. Nothing before this step has history in memory; it lived only in Postgres.

**Step 3 — State update.** The new `HumanMessage` is merged into state via the reducer you defined on the `messages` channel (typically `add_messages`, which appends by id and handles dedup/replace semantics). State now = old history + new message.

**Step 4 — Memory read (long-term).** If your graph has a retrieval/memory node, it runs here — before the LLM call. It queries your long-term store (Postgres `Store` with pgvector, or a separate vector DB) using the current message (or a rewritten query) to pull back relevant facts: user preferences, prior decisions, RAG documents. This is a *separate* read from the checkpoint load in step 2 — checkpoint gives you *this thread's* history, the memory/store read gives you *cross-thread* durable knowledge.

**Step 5 — Context assembly.** A node (often called `prepare_context` or folded into your `call_model` node) takes: system prompt + retrieved long-term memory + trimmed/summarized conversation history + current message, and assembles the actual prompt. This is where `trim_messages` or a summarization sub-graph runs to keep you under the token budget. This step is what actually produces "context" as defined in Section 1 — everything before this was history and stored memory, not yet context.

**Step 6 — LLM inference.** The assembled context is sent to the model (OpenAI Responses API, Anthropic Messages API, whatever). If the model requests a tool call, you branch to a `ToolNode`, execute it, append the `ToolMessage` to state, and loop back to step 5/6 — this is the classic ReAct loop, and each iteration is its own graph "superstep."

**Step 7 — Checkpoint save.** This is the part people miss: LangGraph checkpoints **after every superstep, not just at the end of the turn**. Each node execution that mutates state triggers a checkpoint write. So during a single user turn with two tool calls, you might get four or five checkpoints written, not one. This is *why* interrupt-and-resume (human-in-the-loop) works mid-turn — there's always a durable snapshot to resume from, even between tool calls.

**Step 8 — Memory update (long-term).** After the AI's final response, if you're extracting durable facts ("user prefers TypeScript over JS," "user is targeting a GenAI architect role"), that extraction typically happens as a *separate*, often asynchronous step — either a background task or a dedicated LangGraph node that runs an LLM call over the recent exchange and upserts results into the long-term `Store`. This is deliberately decoupled from the checkpoint save in step 7 because long-term memory extraction is expensive (another LLM call) and shouldn't block the user's response latency.

**Step 9 — Response returned.** Streamed back to the client via SSE/WebSocket, sourced from `astream_events` on the graph.

The key insight engineers miss: **checkpointing is automatic and fine-grained (every superstep); long-term memory updates are deliberate and coarse-grained (once per turn, often async).** These are not the same write path, even though they might land in the same Postgres instance.

---

## 3. LangChain Memory

First, an important production caveat: the legacy `langchain.memory` module (`ConversationBufferMemory`, `ConversationSummaryMemory`, etc.) is **deprecated**. LangChain's own maintainers have moved the recommended pattern to explicit state management via LangGraph — you define what "memory" means as fields in your graph's state schema and manage it with regular Python/reducers, rather than instantiating a `Memory` object and wiring it through a `Chain`. I'm covering the legacy classes below because (a) you'll encounter them in every pre-2024 tutorial and a lot of production code still running them, and (b) the *concepts* they encode map directly onto patterns you re-implement by hand in LangGraph. Understanding why each one exists tells you what design problem you're solving when you build the equivalent yourself.

**`ConversationBufferMemory`** stores the entire raw history and replays all of it as context every turn. It exists because it's the trivial correct baseline — zero information loss. Its limitation is the obvious one: unbounded token growth. A 200-turn conversation eventually exceeds the context window, and even before it does, you're paying full price and full latency for tokens that add no marginal value (older turns are usually irrelevant to the current question).

**`ConversationBufferWindowMemory`** keeps only the last *k* turns. It bounds cost and latency, but it's a blunt instrument — it has no concept of *importance*, only recency. A critical fact stated at turn 1 is silently dropped at turn *k+1* even if it's still relevant. Use this only when you're confident the task is genuinely short-context (simple support bots, single-purpose tools) where old turns truly stop mattering.

**`ConversationSummaryMemory`** replaces old turns with an LLM-generated running summary. It solves the unbounded-growth problem without hard-cutting recency like the window approach — but it introduces its own costs: an extra LLM call per turn (or per threshold), added latency, and, critically, **lossy compression**. Summarization is a form of information destruction; anything the summarizing LLM judges unimportant is gone, and you can't always predict what will turn out to matter three turns later.

**`ConversationSummaryBufferMemory`** is the practical middle ground: keep a raw buffer of the most recent turns *in full fidelity*, and summarize everything older than that once a token threshold is crossed. This is the pattern you'll actually reimplement by hand in LangGraph (see Section 8) — it's the right default for most chat products.

**`ConversationTokenBufferMemory`** is the window variant but bounded by token count rather than turn count — more precise for staying under a hard context ceiling, since turns vary wildly in length (a one-word reply vs. a pasted stack trace).

**`VectorStoreRetrieverMemory`** and **`ConversationKGMemory`** are a different axis entirely — instead of "recent vs. summarized," they're semantic/entity retrieval: embed every turn (or every extracted fact/entity) and retrieve by similarity to the current query rather than by recency. This is what you actually want for *long-term* cross-session memory (Section 6), and it's structurally what LangGraph's `Store` API formalizes.

The unifying limitation across all of these: they're single-strategy, hardcoded, and bolted onto the old `Chain`/`AgentExecutor` abstraction, which itself doesn't give you fine-grained control over *when* memory gets read/written relative to tool calls, retries, or interrupts. That control gap is exactly what LangGraph's state-machine model was built to close — which is why the ecosystem moved there.

---

## 4. LangGraph Checkpointing

A **checkpoint** is a serialized snapshot of every channel in your `StateGraph`'s state, taken after a superstep (a superstep = one round of node execution). Concretely, it contains: the current values of every state channel (your `messages` list, plus any custom fields you defined — `summary`, `retrieved_docs`, `pending_approval`, whatever your schema has), the channel *versions* (used for conflict detection), metadata (`thread_id`, a unique `checkpoint_id`, the `parent_checkpoint_id` forming a linked history, a `step` counter, a `source` tag), and the set of pending writes/tasks describing which node(s) execute next. That last part is what makes resumability possible — the checkpoint doesn't just know *what happened*, it knows *what was about to happen*, so execution can continue mid-graph, not just at message boundaries.

Why checkpointing instead of just "memory" (a buffer of messages)? Because LangGraph models an agent as an arbitrary, possibly cyclic, state machine — not a linear chain. An agent loop can call three tools, hit a human-approval gate, wait an indeterminate amount of time for a human to respond, then resume. A message buffer has no way to represent "we're paused after tool call 2 of 3, waiting on external input." A checkpoint can, because it captures the *entire execution state*, not just the conversational transcript. This is what enables three specific production capabilities that plain memory can't: **crash recovery** (server dies mid-loop, restart, resume from last checkpoint instead of restarting the whole turn), **human-in-the-loop interrupts** (`interrupt()` pauses the graph, persists state, waits for external input via `Command(resume=...)`), and **time-travel/debugging** (you can load any historical checkpoint by id, inspect exact state, or fork a new execution branch from it — invaluable for reproducing a bad agent decision in production).

Checkpointing enables state persistence structurally simply: every `thread_id` maps to an ordered history of checkpoints in your backing store. On the next `invoke`, LangGraph doesn't ask you to reconstruct history manually — it loads the most recent checkpoint for that `thread_id` automatically as part of graph initialization. You never manually "load memory into a variable" the way you would with `ConversationBufferMemory.load_memory_variables()` — it's structural, not something you call.

Why do multiple checkpointer backends exist (Postgres, Redis, MongoDB, SQLite, in-memory)? Because checkpointing is a durability/consistency/throughput tradeoff, and different products land in different places on that tradeoff:

- **`MemorySaver`** (in-process dict) — zero durability, wiped on restart. Use only for local dev/testing, never production.
- **`SqliteSaver`** — durable, single-file, but single-writer/single-instance. Fine for a local desktop app or a CLI agent, wrong for a horizontally scaled web service.
- **`PostgresSaver`/`AsyncPostgresSaver`** — the standard production choice for most chat products: ACID transactions, concurrent multi-instance access (critical if you run multiple FastAPI workers/pods behind a load balancer — state has to live outside process memory so *any* instance can serve *any* request for a thread), and you likely already run Postgres for your app's other data, so it's operationally simple to co-locate. This is what enables the "stateless API server" pattern that makes horizontal scaling trivial.
- **`RedisSaver`** — chosen when you need very low checkpoint-write latency and high throughput (e.g., agents that checkpoint dozens of times per second in tight tool loops), at the cost of needing to think explicitly about persistence/eviction policy (Redis is not durable by default the way Postgres is, unless configured with AOF/RDB carefully).
- **`MongoDBSaver`** — chosen when your state schema is highly variable/nested and you'd rather store it as flexible documents than fight JSONB columns, or when Mongo is already your org's primary datastore.

The choice is an infra decision, not a LangGraph decision — pick the backend that matches your existing operational stack and your durability/latency requirements, not because one is "more correct."

---

## 5. Memory vs. Checkpointing — Same Problem or Different?

Not the same problem, though they're adjacent and easy to conflate because they often live in the same physical database. Checkpointing solves **durable execution** — "how do I never lose the exact state of a running or paused graph." Memory solves **information design** — "what should the agent know, and how do I get the right subset of that knowledge into the prompt without blowing the token budget." A system could have checkpointing with zero memory strategy (just replay raw unbounded history every time until it errors) and, conversely, you could imagine a memory strategy without any checkpointing (a stateless function that reconstructs context from an external database on every call, never pausing mid-execution). They're orthogonal axes.

In practice, though, LangGraph blurs this productively: the checkpointer *is* the mechanism that implements short-term memory, because your `messages` channel — your conversation history — lives inside the checkpointed state. So "short-term memory" in a LangGraph app isn't a separate memory object you manage; it's just... state, and the checkpointer happens to be what persists it. Long-term memory, however, is deliberately kept separate — LangGraph exposes a distinct `Store` interface (`InMemoryStore` for dev, `AsyncPostgresStore` with pgvector for production) specifically because long-term memory needs to be addressable *across threads*, keyed by `user_id` or namespace rather than `thread_id`, and often needs semantic (embedding) search rather than exact-key lookup. A checkpoint is scoped to one thread's execution history; a `Store` entry is scoped to a user or organization and outlives any single thread.

Yes, production applications should use both, and almost every serious chat product does: checkpointer for within-thread continuity, resumability, and crash safety; `Store` for durable, cross-session facts about the user that should surface even in a brand-new conversation. They're connected in one direction — long-term memory is frequently *derived from* checkpointed history. Your extraction pipeline (Section 2, step 8) reads the checkpointed conversation, runs an LLM pass to pull out durable facts, and writes those facts into the `Store`. The checkpoint is the source-of-truth transcript; the `Store` is a distilled, queryable index over what mattered from that transcript. Choose checkpointing alone when you only need "continue this conversation correctly." Add the `Store` when you need "remember this user across conversations they haven't opened yet."

---

## 6. How Production Assistants Actually Remember

Let's ground this in real systems, because the terminology gets sloppy across products.

A **thread ID** identifies one continuous conversation — the unit checkpointing is scoped to. A **session ID** is usually an *auth/browser session* concept (how long you're logged in, unrelated to which conversation you're in) — one session can span many threads. A **conversation ID** is typically just another name for thread ID, though some products (analytics-heavy ones) keep a separate immutable conversation ID even if the underlying thread gets forked or renamed. Don't assume these three terms are interchangeable across codebases — check what each system actually scopes them to.

**Short-term memory** is what's kept live and fully-fidelity within the current thread — the trimmed/windowed recent turns that get sent as-is. **Long-term memory** is durable, cross-thread knowledge extracted and stored separately, retrieved by relevance rather than recency. **Context window** is the hard ceiling — the model's actual token limit — that both of the above have to fit inside alongside system prompt, tool schemas, and retrieved documents.

Concretely, in tools you likely use daily: **ChatGPT** keeps the active thread's messages as short-term context (trimmed as it grows) and separately maintains an explicit, user-visible, user-editable "memory" feature — discrete extracted facts, stored durably, retrieved and injected into future conversations regardless of thread, functioning exactly like a LangGraph `Store`. **Claude.ai**'s memory feature works similarly at a conceptual level: it derives memories from past conversations and can surface them in new chats, separate from the live conversation transcript of any single thread — same architecture, cross-thread durable store distinct from thread-scoped history. **GitHub Copilot Chat** and **Cursor** lean much more heavily on retrieval than on conversational memory per se: their "long-term memory" is really a vector index over your codebase (embeddings of files/symbols), refreshed as you edit, and their "short-term memory" is just the current chat buffer plus whatever files are open/attached. The mental model is the same — short-term = recent buffer, long-term = semantic retrieval store — just applied to code instead of chat history. **Enterprise assistants** (support bots, internal knowledge assistants) typically combine: a RAG layer over a document corpus (vector DB, e.g. pgvector or a dedicated vector store), a thread-scoped buffer for conversational continuity, and a separate user/org profile store for personalization — three distinct retrieval paths merged at context-assembly time.

Why summarize instead of just sending everything, given models now support huge context windows? Four independent reasons, and it's worth having all four ready in an interview: **cost** — every token in context is billed on every single call, and unbounded history means cost grows quadratically with conversation length across a session; **latency** — larger prompts measurably slow both time-to-first-token and total generation time; **the "lost in the middle" effect** — empirically, models attend less reliably to information buried in the middle of a very long context than to information near the start or end, so cramming in everything doesn't guarantee the model actually *uses* the old information correctly; and **the hard ceiling** — even generous context windows are finite, and a genuinely long-running agent (days of usage, thousands of turns) will eventually exceed any fixed window regardless. Summarization and retrieval aren't hacks around a limitation that will disappear — they're a permanent architectural pattern for managing relevance and cost, the same way you wouldn't load an entire production database into RAM just because your server technically has enough RAM to try.

---

## 7. Reference Architecture — React + FastAPI + LangGraph + Postgres/PGVector + OpenAI Responses API

Trace one message end to end through this stack.

The **React client** POSTs the user's message to `/chat` along with a `thread_id` (generated client-side on "new conversation," persisted in local component state/URL) and the authenticated `user_id` (from your auth layer, not the client). **FastAPI** receives it, does auth/rate-limit checks, and calls `graph.astream_events({"messages": [HumanMessage(...)]}, config={"configurable": {"thread_id": thread_id, "user_id": user_id}}, version="v2")`. It does *not* touch history or memory directly — that's entirely the graph's responsibility, which is the point of the abstraction.

Inside **LangGraph**, the compiled graph is backed by two separate Postgres-based components: an `AsyncPostgresSaver` (checkpointer, thread-scoped, holds the `messages` channel and any scratch state) and an `AsyncPostgresStore` configured with a pgvector index (long-term, user-scoped, embeddings-searchable). On invoke, the checkpointer loads the latest checkpoint for `thread_id` — this is your conversation history reappearing in process memory. A `retrieve_memory` node queries the store by `user_id` namespace for relevant durable facts. A `prepare_context` node applies `trim_messages` (token-budget aware, using the actual model's tokenizer) or triggers the summarization sub-flow if the thread has grown past a threshold. A `call_model` node invokes the LLM — here, the OpenAI Responses API via `ChatOpenAI` — with tool definitions bound if the agent has tools. If the model returns a tool call, control passes to a `ToolNode`, the tool executes (this might itself hit Postgres, an external API, whatever), the result comes back as a `ToolMessage`, and the loop returns to `call_model`. Each of these node transitions is an independent superstep, and the checkpointer durably persists state after each one — so if your pod gets rescheduled mid-tool-call, the next request to that `thread_id` resumes cleanly rather than losing the turn.

Once the model produces its final `AIMessage`, it streams token-by-token back through `astream_events`, which FastAPI forwards to the **React** client over Server-Sent Events (or WebSocket). Separately — not blocking the response — a background task (FastAPI `BackgroundTasks`, or better, a proper queue like Arq/Celery for anything non-trivial) runs a lightweight extraction pass over the last exchange, decides whether anything durable was learned about the user, and if so upserts it into the `Store` (which embeds it via pgvector on write). The **next message** the user sends repeats the exact same cycle: checkpoint load gives correct thread continuity, store query gives correct cross-session recall, and neither has to be manually stitched together by application code — it's structural to the graph.

The single most important consequence of this design for scalability: because all state (checkpoints and long-term memory) lives in Postgres and not in FastAPI process memory, your API layer is fully stateless and horizontally scalable — any pod can serve any request for any `thread_id`, with no sticky sessions required. That property alone is worth designing for deliberately from day one; retrofitting it after you've accidentally built in-memory state is painful.

---

## 8. Production Code

```txt
# requirements.txt
fastapi>=0.115
uvicorn[standard]>=0.30
langgraph>=0.3
langgraph-checkpoint-postgres>=2.0
langchain-openai>=0.2
langchain-core>=0.3
psycopg[binary,pool]>=3.2
pydantic>=2.8
```

### 8.1 State schema and graph definition

```python
# graph.py
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, SystemMessage, RemoveMessage, trim_messages
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# `messages` uses the add_messages reducer: new messages are appended
# (or replace an existing message with the same `id`, which is how tool
# result streaming and edits work without duplicating history).
# `summary` is our own field — this is what makes short-term memory a
# *managed* buffer instead of an unbounded list.
class ChatState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    summary: str

model = ChatOpenAI(model="gpt-4.1", temperature=0.3)
# tools = [...]  # your @tool-decorated functions
# model_with_tools = model.bind_tools(tools)

SYSTEM_PROMPT = "You are a precise, senior-engineer-level assistant."

def prepare_and_call_model(state: ChatState) -> dict:
    """Assembles context (system prompt + optional running summary +
    token-trimmed recent history) and calls the LLM. This is the exact
    point where 'context' as distinct from 'history' comes into being."""
    system = SYSTEM_PROMPT
    if state.get("summary"):
        # Fold the running summary into the system message so older,
        # compressed context is still available without spending tokens
        # on the raw turns it replaced.
        system += f"\n\nSummary of earlier conversation:\n{state['summary']}"

    trimmed = trim_messages(
        state["messages"],
        max_tokens=6000,           # leave headroom under the model's window
        strategy="last",            # keep the most recent turns
        token_counter=model,        # uses the model's real tokenizer, not len()
        include_system=False,
        start_on="human",           # never truncate mid tool-call pair
    )
    response = model.invoke([SystemMessage(content=system), *trimmed])
    return {"messages": [response]}

def should_summarize(state: ChatState) -> str:
    # Trigger summarization once the raw buffer gets long, independent of
    # the token-trim step above — this keeps the *stored* history compact
    # too, not just what we happen to send on a given call.
    return "summarize" if len(state["messages"]) > 20 else END

def summarize_conversation(state: ChatState) -> dict:
    """Collapses older turns into a running summary and issues
    RemoveMessage ops to actually delete them from stored state — this
    is what keeps Postgres rows bounded over a long-running thread."""
    existing_summary = state.get("summary", "")
    prompt = (
        f"Extend this summary with the new messages below:\n{existing_summary}"
        if existing_summary
        else "Summarize the conversation above concisely, preserving facts and decisions."
    )
    result = model.invoke(state["messages"] + [SystemMessage(content=prompt)])
    # Keep the most recent 4 messages in full fidelity; delete the rest.
    to_delete = [RemoveMessage(id=m.id) for m in state["messages"][:-4]]
    return {"summary": result.content, "messages": to_delete}

builder = StateGraph(ChatState)
builder.add_node("agent", prepare_and_call_model)
builder.add_node("summarize", summarize_conversation)
# builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
# builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: "check_summary"})
builder.add_conditional_edges("agent", should_summarize, {"summarize": "summarize", END: END})
builder.add_edge("summarize", END)
```

`add_messages` is doing real work here, not just list-append boilerplate: it deduplicates by message `id`, which is what lets streaming partial-tool-call updates overwrite rather than duplicate, and it's what makes `RemoveMessage` in the summarization node actually delete specific stored messages instead of you manually filtering the list. The `should_summarize` conditional edge is a *separate* control point from the `trim_messages` call inside `prepare_and_call_model` — one manages what gets *sent* to the model this turn (temporary, recomputed every call), the other manages what gets *persisted* in the checkpoint (permanent, until summarized again). Conflating those two is a common bug: people trim for the prompt but never shrink stored state, and their Postgres rows grow forever anyway.

### 8.2 Checkpointer and long-term store setup

```python
# persistence.py
import os
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from langchain_openai import OpenAIEmbeddings

DB_URI = os.environ["DATABASE_URL"]  # postgresql://user:pass@host:5432/db

# A pooled connection is mandatory in production — a single connection
# serializes every concurrent user's checkpoint reads/writes.
pool = AsyncConnectionPool(conninfo=DB_URI, max_size=20, open=False)

async def build_persistence():
    await pool.open()

    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()  # idempotent: creates tables on first run only

    # The Store is deliberately separate from the checkpointer: it's
    # keyed by (namespace, key) — typically namespace=("memories", user_id) —
    # not by thread_id, and it's configured with an embeddings index so
    # `.asearch()` does semantic similarity, not exact lookup.
    store = AsyncPostgresStore(
        pool,
        index={"embed": OpenAIEmbeddings(model="text-embedding-3-small"), "dims": 1536},
    )
    await store.setup()

    return checkpointer, store
```

```python
# main.py (graph compilation)
from graph import builder
from persistence import build_persistence

checkpointer, store = await build_persistence()
graph = builder.compile(checkpointer=checkpointer, store=store)
```

Two separate `setup()` calls, two separate physical concerns even though both live in the same Postgres instance: the checkpointer's tables hold execution-state snapshots keyed by `thread_id`/`checkpoint_id`; the store's tables hold embedded, namespace-and-key-addressed facts. Compiling with *both* `checkpointer=` and `store=` is what makes both available inside every node via `config` and the injected `store` argument, respectively.

### 8.3 FastAPI streaming endpoint

```python
# api.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    thread_id: str
    user_id: str
    message: str

@app.post("/chat")
async def chat(req: ChatRequest, background_tasks: BackgroundTasks):
    config = {"configurable": {"thread_id": req.thread_id, "user_id": req.user_id}}

    async def event_stream():
        async for event in graph.astream_events(
            {"messages": [HumanMessage(content=req.message)]},
            config=config,
            version="v2",
        ):
            # Filter to just the model's token stream for the client;
            # other event types (node-start, tool-call) are useful for
            # server-side logging/tracing but shouldn't hit the wire.
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"].content
                if chunk:
                    yield f"data: {chunk}\n\n"

        # Long-term memory extraction happens *after* the response has
        # been fully streamed — it must never add latency to the user's
        # turn-around time.
        background_tasks.add_task(extract_long_term_memory, req.thread_id, req.user_id)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


async def extract_long_term_memory(thread_id: str, user_id: str):
    state = await graph.aget_state({"configurable": {"thread_id": thread_id}})
    recent = state.values["messages"][-4:]
    extraction_prompt = (
        "Extract any durable facts about the user worth remembering "
        "in future conversations (preferences, goals, constraints). "
        "Return nothing if there's nothing durable to save."
    )
    result = await model.ainvoke(recent + [SystemMessage(content=extraction_prompt)])
    if result.content.strip():
        await store.aput(
            namespace=("memories", user_id),
            key=str(uuid.uuid4()),
            value={"fact": result.content},
        )
```

Note the deliberate asymmetry: the checkpointer writes are synchronous and automatic (they happen inside `graph.astream_events` as part of normal graph execution — you never call them explicitly), while the long-term memory write is explicit, manual, and pushed to a background task specifically so a slow extraction LLM call can't delay the user-visible response. This is the single most common performance mistake in early implementations — doing memory extraction inline and eating the extra 1-2 seconds of latency on every single turn.

### 8.4 Injecting long-term memory into context

```python
# inside prepare_and_call_model, before building `system`:
from langgraph.store.base import BaseStore

def prepare_and_call_model(state: ChatState, config: dict, *, store: BaseStore) -> dict:
    user_id = config["configurable"]["user_id"]
    last_user_msg = state["messages"][-1].content
    memories = store.search(("memories", user_id), query=last_user_msg, limit=5)
    memory_block = "\n".join(m.value["fact"] for m in memories)
    system = SYSTEM_PROMPT
    if memory_block:
        system += f"\n\nRelevant facts about this user:\n{memory_block}"
    # ...rest as before
```

`store` is injected automatically by LangGraph when the node signature declares it — you don't pass it manually at call time. `store.search` runs a semantic similarity query against the pgvector index built at store setup, which is exactly why long-term memory retrieval feels categorically different from checkpoint loading: one is exact-key ("give me this thread's history"), the other is similarity-ranked ("give me whatever's relevant to what the user just said, regardless of which thread it came from").

---

## 9. Summary

**Common beginner misconceptions.** Thinking the LLM "remembers" anything between calls — it doesn't; every call is stateless and you resupply everything. Thinking `ConversationBufferMemory` and friends are still the recommended pattern — they're deprecated in favor of explicit LangGraph state. Thinking checkpointing *is* long-term memory — it's thread-scoped execution durability, not cross-session user knowledge. Thinking trimming messages for the prompt also shrinks what's stored — it doesn't unless you separately delete from state. Thinking bigger context windows remove the need for summarization/retrieval — cost, latency, and attention-degradation on long contexts make this a permanent architectural pattern, not a stopgap.

**Best practices.** Separate your `trim_messages`-for-this-call logic from your summarize-and-delete-from-state logic — they solve different problems on different cadences. Never run long-term memory extraction inline in the response path; always background it. Always use a connection pool for your Postgres checkpointer, never a single connection, or you serialize all your concurrent users. Design your API layer to be fully stateless from day one — all state in Postgres — so horizontal scaling is free.

**Production recommendations.** `AsyncPostgresSaver` + `AsyncPostgresStore` (pgvector-indexed) is the default correct choice for most chat products unless you have a specific throughput reason to reach for Redis. Keep system-prompt-injected long-term memory small (top-5 relevant facts, not a full dump) — it competes for attention with the actual conversation. Version your state schema deliberately; adding/removing fields on a `TypedDict` that's already checkpointed in production requires a migration plan, not just a code change.

**Performance considerations.** Token-counting with the real model tokenizer (not `len(str)`) in `trim_messages` avoids silently overshooting the context window. Streaming (`astream_events`) is not optional for perceived latency on anything beyond trivial responses. Summarization LLM calls are real cost centers at scale — consider a cheaper/faster model for the summarization node than for the main agent.

**Scalability considerations.** Stateless FastAPI workers behind a load balancer, all state in Postgres, is what lets you scale horizontally without sticky sessions. Checkpoint tables grow unbounded per thread unless you actively summarize/prune — plan a retention/archival policy before it becomes a hot-path query performance problem. Long-term memory stores can grow to millions of rows across users; pgvector index tuning (HNSW parameters) matters at that scale in a way it doesn't in a demo.

**Interview questions and answers, in the register you'll actually be asked them:**

*"What's the difference between memory and checkpointing in LangGraph?"* — Checkpointing is durable execution-state persistence keyed by thread, enabling crash recovery, human-in-the-loop pausing, and time-travel debugging; memory is the policy layer deciding what information (short-term buffer, long-term facts) gets assembled into context for the model, implemented via managed state (short-term) and a separate `Store` (long-term).

*"Why would you summarize conversation history instead of just using a bigger context window?"* — Cost scales with every token on every call; latency scales with prompt size; models attend less reliably to information in the middle of very long contexts; and even large windows are eventually finite for long-running agents. Summarization is a permanent architectural pattern, not a workaround.

*"How do you scale a LangGraph-based chat API horizontally?"* — Keep the API layer stateless; back the checkpointer and long-term store with Postgres (or another shared, durable backend) instead of in-process memory, so any instance can serve any thread; use connection pooling.

*"When would you choose Redis over Postgres for checkpointing?"* — When you need very high checkpoint-write throughput/low latency (tight tool-calling loops checkpointing many times per second) and you're willing to own explicit persistence/eviction configuration, versus Postgres's ACID durability by default.

*"How does long-term memory get populated — synchronously or asynchronously, and why?"* — Asynchronously, as a background task after the response streams, because extraction requires its own LLM call and must not add latency to the user-facing turn.

**Real-world architecture patterns worth citing in an interview:** ChatGPT's split between live thread context and an explicit, user-editable, cross-session memory store; Claude.ai's derived-memory system separate from any single conversation's transcript; Cursor/Copilot's reliance on embedding-indexed codebase retrieval as their "long-term memory" rather than conversational summarization; and enterprise RAG assistants layering document retrieval, thread-scoped buffers, and user/org profile stores as three independent, mergeable context sources. In every case, the pattern is the same one this document walks through: stateless model, durable execution layer, and a deliberately separate policy layer deciding what enters the prompt.

Good — this is the exact question that separates "I read the LangGraph docs" from "I understand the design space." Short answer: **yes, tooling exists for both, but at different levels of maturity.** LangGraph core gives you primitives, not automation. LangMem (a separate LangChain-maintained library, purpose-built for this) gives you actual drop-in summarization and memory-management utilities. OpenAI's own API gives you truncation, not summarization — those are not the same thing, and conflating them is a common mistake. Let me break down each piece.

## Short-term summarization — is there a built-in method?

**LangGraph core**: no automatic summarization node ships in the base library. What I hand-wrote for you last time (`RemoveMessage` + a `summary` field + a conditional edge) *is* the documented reference pattern — LangGraph expects you to assemble it from primitives (`add_messages`, `RemoveMessage`, `trim_messages`).

**LangMem**: does ship a ready-made node — `SummarizationNode` — that packages this same pattern with one important improvement over what I showed you: it's **token-threshold triggered, not turn-count triggered**, and it's **non-destructive**.

```python
from langmem.short_term import SummarizationNode
from langchain_core.messages.utils import count_tokens_approximately

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarization_model,          # can be a cheaper model than your main agent
    max_tokens=1500,                    # trigger point
    max_tokens_before_summary=1500,     # when raw history exceeds this, summarize
    max_summary_tokens=256,
    output_messages_key="llm_input_messages",   # <- key detail below
)
```

The important design decision here: it writes the compacted history to a **separate state key** (`llm_input_messages`), leaving your original `messages` channel — the checkpointed source of truth — untouched. My earlier version deleted old messages from state via `RemoveMessage`. That's a real tradeoff you should decide deliberately, not by accident:

- **Destructive** (delete from state, like my earlier code): smaller checkpoints, cheaper storage, but you lose the raw transcript forever — bad for audit, debugging, or re-summarizing with a better prompt later.
- **Non-destructive** (LangMem's default): raw history stays in Postgres forever, only the *model-facing view* gets compacted. Costs more storage, but you can always regenerate a better summary, run analytics on real transcripts, or satisfy compliance requirements that need the unedited record.

For a product you're building toward a senior/architect portfolio, default to non-destructive — it's the correct answer in almost every real system, and "why did you throw away the audit trail" is exactly the kind of question that gets asked in a design review.

**On turn-count vs token-count thresholds**: token-count is the better practice, and here's the concrete reason — 10 one-line messages and 10 messages containing pasted stack traces are wildly different token loads, but "reached 10 messages" treats them identically. If you still want turn-count for simplicity (e.g., a lightweight prototype), it's a two-line conditional edge, exactly like `should_summarize` in the code I gave you earlier — that part of what I wrote wasn't a simplification, it's a legitimate, if less precise, option.

## What about OpenAI's own API — does it summarize for you?

No, and this is worth being precise about in an interview. The Responses API's `previous_response_id` chaining and its `truncation` parameter (`"auto"` vs `"disabled"`) manage *conversation state storage* — OpenAI keeps prior turns server-side so you don't have to resend them — but `truncation="auto"` just **drops messages from the middle** when you exceed the context window. That's blunt truncation, not compression. No LLM call happens to preserve the gist of what got dropped. If you rely on this alone, you silently lose information with no summary standing in for it. Real summarization always requires an explicit extra LLM call — that's true whether you write it by hand or use LangMem's node; there's no way around that cost, only decisions about who pays it and when.

## Long-term memory — filtering and categorization

This is where LangMem earns its keep, and where "ideal practice" actually has a named taxonomy, not just a vibe. LangMem categorizes long-term memory into three types, borrowed from cognitive-architecture literature:

**Semantic memory** — durable facts. "Prefers TypeScript over vanilla JS," "targeting a GenAI architect role," "works at a mid-size fintech." Stored as discrete, retrievable facts or a structured profile object.

**Episodic memory** — specific past interactions worth recalling as examples. Not "what's true about the user" but "here's a case where this approach worked well for this user" — functions like a few-shot example bank, retrieved when a similar situation recurs.

**Procedural memory** — instructions about *how the assistant itself should behave* for this user/org, effectively a learned, evolving system prompt. "This user wants terse code answers, no preamble" is procedural, not semantic.

The filtering question — what *should* graduate to long-term storage — comes down to four criteria, and this is the part developers get wrong most often by just dumping everything:

1. **Durability** — will this matter in an unrelated future conversation, or is it only relevant to resolving *this* task? "User wants the bug fixed in `auth.py`" is not durable. "User strongly prefers functional components over class components" is.
2. **Explicit vs. inferred** — if the user says "remember that I use pnpm, not npm," save it with high confidence, low bar. If you're *inferring* a preference from behavior, that needs a higher confidence threshold before you persist it — false inferred memories are worse than no memory, because they silently bias future responses in a way the user can't see or correct.
3. **Generality** — a one-off request isn't memory-worthy; a repeated pattern across multiple threads is a stronger signal.
4. **Deduplication/consolidation** — don't just append. If you already have "prefers TypeScript" and the extraction pass produces "really likes TypeScript over JS," that should *update* the existing memory, not create a duplicate. This is a real failure mode at scale — unmanaged memory stores accumulate redundant, sometimes contradictory entries, and retrieval quality degrades. LangMem's memory manager does this consolidation reasoning for you rather than naively appending.

## Two paradigms for populating long-term memory — pick deliberately

**Background/scheduled extraction** (deterministic, threshold-triggered — this maps to your original question): a separate pass runs after N turns or after the conversation ends, reads recent history, and writes to the store.

```python
from langmem import create_memory_store_manager

memory_manager = create_memory_store_manager(
    "openai:gpt-4.1-mini",              # cheap model — this runs constantly
    namespace=("memories", "{user_id}"),
)
# Call after N turns, or as a background task, or on a cron/queue job:
await memory_manager.ainvoke({"messages": recent_messages})
```

**Agent-invoked memory tools** (the agent decides, in-context, that something is worth remembering — no fixed threshold at all):

```python
from langmem import create_manage_memory_tool, create_search_memory_tool

tools = [
    create_manage_memory_tool(namespace=("memories", "{user_id}")),
    create_search_memory_tool(namespace=("memories", "{user_id}")),
]
# bind these alongside your other tools — the model calls them like any tool
```

This second pattern is genuinely the more modern, more agentic approach, and it's worth understanding why it's gaining ground: instead of a rigid "every 10 messages, run extraction" rule, the LLM itself recognizes *in the moment* — "the user just told me something durable" — and calls a tool to save it, the same way it'd call any other tool. It's less predictable in timing but far more precise in *what* gets saved, because the model has full conversational context when deciding, rather than a separate extraction pass working from a message window after the fact.

**In practice, production systems run both**: agent-invoked tools for high-confidence, explicit "remember this" moments during the conversation, plus a periodic background consolidation pass (LangMem's manager) that sweeps through recent threads, catches things the agent didn't proactively flag, and de-duplicates/merges the memory store. Relying on only the threshold-based background job misses things the user explicitly asked to be remembered mid-conversation; relying on only agent-invoked tools misses subtler patterns that only become obvious in aggregate across many turns.

Want me to append this as a new section to the guide document from before, so you've got it all in one reference file?