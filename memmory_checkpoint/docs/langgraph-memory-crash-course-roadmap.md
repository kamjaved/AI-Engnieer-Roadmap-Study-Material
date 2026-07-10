# LangGraph Memory Architecture — Lean Crash Course

> Distilled from `roadmap-production-grade-project-guide.md`. This is a standalone learning document — every lesson below carries enough context to be pasted, on its own, into ChatGPT, Gemini, or Claude and produce correct, scoped code. You do not need to attach the original 3-week roadmap for any single lesson to make sense.

---

## 0. Summary & Objective — Read This First (Including If You're an AI Tool)

**What this is.** A ~4-hour, hands-on crash course that teaches the complete memory architecture behind modern LLM agents — raw transcript storage, checkpointing, manual summarization, framework-native summarization, and long-term memory — using a minimal slice of a cruise-booking assistant as the vehicle. It is *not* the production app. It is deliberately small so the memory concepts are visible and uncluttered by domain complexity, auth, UI polish, or infra.

**What you'll be able to do afterward.** Explain, from first principles and with working code you wrote yourself, the difference between conversation history, short-term memory, long-term memory, checkpoints, and context — and implement all five in Postgres, first by hand and then using LangMem's built-in utilities, so you understand exactly what the framework is doing for you before you rely on it.

**Domain used.** A single deterministic tool (`search_sailings`) backed by a small seeded Postgres table, wrapped in a LangGraph agent. That's the entire "business logic" for this crash course — deliberately thin, because the learning goal is memory, not domain modeling.

**Explicitly out of scope for this crash course** (all deferred to the full 3-week roadmap — see Section 9): authentication, multiple domain tables (ships/bookings/fare calculation), Alembic migrations, the `checkpoint_metadata` debug table, React UI, automated tests, logging polish, README/demo-script production. Where relevant, each lesson below flags exactly what it's skipping and where it resumes in the full roadmap.

**How to use this document.** Work top to bottom. Each lesson is self-contained: objective, why it matters, what state it assumes from the previous lesson, what to build, a short illustrative code pattern (to build your own mental model), and a ready-to-paste "AI Build Prompt" you can hand to a coding assistant to generate the actual implementation in your repo. Do the "Done When" check before moving on — memory bugs compound if you skip a lesson.

**Total time:** ~4 hours. Natural split point: Lessons 1–4 (~2h, gets you to a working, checkpointed, persisted agent) and Lessons 5–8 (~2h, all the memory-compression and long-term-memory content).

---

## 0.5 Verification Notes (checked July 2026)

Before starting, here's what was fact-checked against current PyPI releases and official LangChain/LangGraph reference docs, and what changed as a result. Read this once; it doesn't change the lesson flow, only two technical details and one piece of context worth having before Lesson 6.

**Confirmed still accurate, no changes needed:**
- `StateGraph`, `add_messages`, `AnyMessage`, `ToolNode`, `tools_condition` (still in `langgraph.prebuilt`), and `AsyncPostgresSaver`'s constructor (it does accept a connection/pool object directly, matching Lesson 4's `AsyncPostgresSaver(pool)` pattern) are all current — nothing here is deprecated as of the latest `langgraph` (~1.2.x) and `langgraph-checkpoint-postgres` (~3.x) releases.
- `langchain-openai`'s `ChatOpenAI`, `pydantic-settings`' `BaseSettings`, and psycopg3's native async support are all unchanged from what the roadmap describes.

**One real gap, fixed below (Lesson 1 + Lesson 4):** the dependency audit lists `psycopg[binary]` as sufficient for the checkpointer's `AsyncConnectionPool`. It isn't — `AsyncConnectionPool`/`ConnectionPool` ship in a **separate** distribution, `psycopg_pool` (installed via the `pool` extra: `psycopg[pool]`, or standalone `psycopg-pool`). Without it, Lesson 4's `from psycopg_pool import AsyncConnectionPool` import fails. Fixed in the dependency table and install command below.

**One piece of context, not a fix (relevant to Lesson 6 and Lesson 8):** LangChain hit a 1.0 milestone with a new `create_agent` + middleware system that ships its own first-party `SummarizationMiddleware`, built into core `langchain` rather than the separate `langmem` package. `langmem` itself is still functional and its last release predates that milestone by several months — it isn't deprecated, but it's now one of *three* production options for context-window summarization rather than the only framework-native one. This doesn't change what you build in Lesson 6 (LangMem's `SummarizationNode` is still the more instructive, graph-native path for learning what's actually happening), but Lesson 8's comparison table now includes the middleware as a fourth reference point so you have the full current picture.

None of this affects sequencing — proceed lesson by lesson exactly as written, with the two Lesson 4 corrections applied.

---

## 1. Lesson 1 — Prerequisites & Project Setup

### 🎯 Objective
Get the minimum viable backend running with exactly the dependencies this crash course needs — no more.

### 🧠 Why This Matters
Every extra abstraction you install before you need it is something you'll debug without understanding. The full roadmap's Week 1 sets up repositories, services, Alembic, and a layered folder structure — correct for a production app, wrong for a 4-hour concept workshop. Here we install only what touches memory/checkpointing directly.

### 📥 Dependency Audit
Your current `pyproject.toml`:

```toml
dependencies = [
  "fastapi[standard]>=0.139.0",
  "langchain>=1.3.12",
  "langgraph>=1.2.9",
  "openai>=2.45.0",
  "psycopg[binary,pool]>=3.3.4",
  "python-dotenv>=1.2.2",
  "sqlalchemy>=2.0.51",
]
[dependency-groups]
dev = ["mypy>=2.2.0", "ruff>=0.15.21"]
```

| Package | Status | Why |
|---|---|---|
| `fastapi[standard]` | ✅ have | API layer |
| `langchain` | ✅ have | core message/prompt primitives (`trim_messages`, `AnyMessage`, etc.) |
| `langgraph` | ✅ have | the graph/state/agent runtime |
| `openai` | ✅ have | underlying SDK — you won't call this directly, `langchain-openai` wraps it |
| `psycopg[binary,pool]` | ✅ have | psycopg **3** has native async support, so the base package covers both your SQLAlchemy async engine *and* LangGraph's Postgres checkpointer — you do not need `asyncpg` as well. **The `pool` extra is required separately**: `AsyncConnectionPool`/`ConnectionPool` (used in Lesson 4) live in the `psycopg_pool` distribution, not in `psycopg[binary]` — `binary` only gets you the compiled C driver, not pooling. Easy to miss and a common first-run `ImportError`. |
| `python-dotenv` | ✅ have | `.env` loading |
| `sqlalchemy` | ✅ have | 2.0 async ORM for your own app tables |
| `mypy`, `ruff` | ✅ have | dev tooling |
| `langchain-openai` | ❌ missing | `ChatOpenAI` model integration — `langchain` core does **not** include this |
| `langgraph-checkpoint-postgres` | ❌ missing | the actual Postgres-backed checkpointer implementation — `langgraph` core ships the interface, not the Postgres backend |
| `langmem` | ❌ missing | `SummarizationNode`, `summarize_messages`, and the long-term memory store manager (Lessons 6–7) |
| `pydantic-settings` | ❌ missing | `BaseSettings` was split out of core Pydantic v2 — needed for typed `.env` config |

Install:

```bash
uv add langchain-openai langgraph-checkpoint-postgres langmem pydantic-settings
uv add "psycopg[pool]"   # if psycopg was added previously without the pool extra
```

### 🛠️ What To Build
A folder structure thinner than the full roadmap's — everything memory-related lives together so you can see it as one system, not spread across a layered architecture you haven't earned the need for yet:

```text
src/
  app/
    main.py
    core/
      config.py          # pydantic-settings: DATABASE_URL, OPENAI_API_KEY, APP_ENV
    db/
      base.py             # SQLAlchemy declarative base
      session.py          # async engine + session factory
      models.py           # ALL tables in one file for now (see Lesson 1 schema below)
      seed.py              # seed script
    agent/
      graph.py             # built up across Lessons 3–7
      tools.py             # search_sailings
    memory/
      manual_summarizer.py # Lesson 5
      langmem_summarizer.py # Lesson 6
      long_term_memory.py   # Lesson 7
    api/
      routes_chat.py
      routes_debug.py
```

`.env`:
```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/cruise_crash_course
OPENAI_API_KEY=sk-...
APP_ENV=local
```

### 🗄️ Seed Schema
Six tables total — the full roadmap's `users`/`ships`/`sailings`/`bookings` domain is collapsed to just `users` + `sailings` (one table, enough for one realistic tool), plus the four memory tables that are the actual point of this crash course.

```text
users
  id (int, pk)
  name (text)

sailings
  id (int, pk)
  ship_name (text)
  departure_port (text)
  arrival_port (text)
  departure_date (date)
  adult_fare (numeric)
  currency (text)

conversation_threads
  thread_id (text, pk)          -- pattern: thread_{user_id}_{uuid}
  user_id (int, fk -> users.id)
  summary_mode (text)            -- 'manual' | 'langmem_function' | 'langmem_node'
  created_at (timestamptz)
  updated_at (timestamptz)

messages
  id (bigint, pk, identity)
  thread_id (text, fk -> conversation_threads.thread_id)
  role (text)                    -- 'user' | 'assistant' | 'tool' | 'system'
  content (text)
  created_at (timestamptz)

summaries
  id (bigint, pk, identity)
  thread_id (text, fk -> conversation_threads.thread_id)
  summary_text (text)
  covered_until_message_id (bigint, fk -> messages.id)
  strategy (text)                -- 'manual' | 'langmem'
  created_at (timestamptz)

long_term_memories
  id (bigint, pk, identity)
  user_id (int, fk -> users.id)
  memory_type (text)             -- travel_preference | communication_preference | profile | currency_preference | ignore
  content (text)
  confidence (numeric)
  source_thread_id (text)
  status (text)                  -- 'active' | 'deleted'
  created_at (timestamptz)
```

Note what's deliberately absent: `ships`, `bookings`, and `checkpoint_metadata` from the original roadmap. LangGraph's own checkpointer tables (created automatically by `checkpointer.setup()` in Lesson 4) are your real checkpoint storage — `checkpoint_metadata` was only ever a debug-UI convenience table, postponed to the full roadmap.

### 🤖 AI Build Prompt
```text
Using SQLAlchemy 2.0 async ORM and psycopg3, generate:
1. src/app/core/config.py using pydantic-settings BaseSettings, loading
   DATABASE_URL, OPENAI_API_KEY, APP_ENV from .env
2. src/app/db/base.py with a DeclarativeBase
3. src/app/db/session.py with an AsyncEngine (postgresql+psycopg driver)
   and an async_sessionmaker, plus a FastAPI dependency get_db_session()
4. src/app/db/models.py with SQLAlchemy models for exactly these six
   tables, no others: users, sailings, conversation_threads, messages,
   summaries, long_term_memories — [paste the schema block above]
5. src/app/db/seed.py — an async script that seeds:
   - 2 users: "Kamran", "Sarah"
   - 5 sailings across at least 2 different ship names and at least 2
     different months in 2026
   Do not add authentication, additional tables, or foreign key
   cascades beyond basic referential integrity.
6. src/app/main.py — a minimal FastAPI app with a GET /health endpoint
   and a startup event that creates tables via Base.metadata.create_all
   if they don't exist (skip Alembic entirely for this crash course).
```

### ✅ Done When
`uv run uvicorn app.main:app --reload` starts cleanly, `GET /health` returns 200, and the six tables exist with seed rows in them.

### ⏭️ Deferred to Full Roadmap
Alembic migrations, repository/service layering, `ships`/`bookings` tables, Ruff/mypy CI wiring — all Lesson 1.1–1.3 in the original roadmap, unchanged, come back to those once this crash course is done.

### ⏱️ ~20 minutes

---

## 2. Lesson 2 — The Memory Mental Model

### 🎯 Objective
Before writing a line of agent code, fix five terms so precisely that you can't accidentally conflate them later — this is the single biggest source of confusion in production memory bugs.

### 🧠 Why This Matters
Every table you just created maps to exactly one of these concepts. If the mapping is fuzzy in your head, it'll be fuzzy in your schema and your bugs will be silent (e.g., "why did the agent forget something the user said two turns ago" is almost always a context-assembly bug, not a storage bug).

```text
Context
  The literal set of tokens sent to the LLM on THIS call.
  Ephemeral. Assembled fresh every turn. Never stored as-is.

Conversation history
  The raw, append-only log of every message ever exchanged in a thread.
  Stored forever in `messages`. Source of truth. Never lossy.

Short-term memory
  The thread-scoped strategy for turning history into context: which
  recent raw messages plus which summary get sent this turn.
  Lives partly in `summaries`, partly in LangGraph's checkpointed state.

Long-term memory
  Durable, user-scoped facts that outlive any single thread.
  Stored in `long_term_memories`, retrieved by user_id across ALL
  future threads, not just this one.

Checkpoint
  A snapshot of the LangGraph *execution state* (not just messages —
  every state channel) taken after each graph step, keyed by thread_id.
  Exists for crash recovery and resumability, not for chat display.
```

The core relationship to hold in your head for the rest of this course: **`messages` is truth, `summaries` is compressed truth for one thread, `long_term_memories` is durable truth across threads, and the checkpoint is infrastructure plumbing that happens to also durably hold the graph's working copy of recent messages.** You will build all four as physically separate things in Postgres, on purpose, so the distinction stays real instead of theoretical.

### 🤖 AI Build Prompt
None — this lesson is conceptual. If you want to sanity-check your own understanding with an AI tool, ask it: *"Given this schema [paste Lesson 1's schema], which table(s) would a request to 'show me everything the user has ever said' query? Which table(s) would 'does the assistant know I prefer balcony cabins' query? Which table(s) would 'resume this conversation after a server crash' query?"* — the answers should be `messages`; `long_term_memories`; and the checkpointer's own tables (not any table you created), respectively.

### ⏱️ ~15 minutes

---

## 3. Lesson 3 — Minimal Tool-Calling Agent + Raw Transcript Persistence

### 🎯 Objective
Build the smallest working LangGraph agent — one tool, no summarization, no checkpointing yet — and persist every message it produces into `messages`. This establishes the "truth" layer everything else compresses or supplements.

### 🧠 Why This Matters
You need a real, tool-augmented `messages` table before summarization or checkpointing mean anything to build against — summarizing an empty table teaches nothing. Persisting to `messages` here, deliberately *without* a checkpointer yet, also makes an important point concrete: **conversation history and checkpointing are two independent persistence paths.** You're about to feel that independence directly, because right now if you restart the server mid-conversation, the transcript survives (it's in Postgres) but the *graph* has no memory of where it was — that gap is exactly what Lesson 4 closes.

### 📥 Assumed State
Lesson 1's tables exist and are seeded.

### 🛠️ What To Build
- `agent/tools.py` — one `@tool`-decorated `search_sailings(ship_name: str | None, month: str | None)` that queries `sailings`.
- `agent/graph.py` — a `StateGraph` with `messages: Annotated[list[AnyMessage], add_messages]`, an `agent` node (model + bound tool), a `ToolNode`, and a conditional edge (`tools_condition`) — **no checkpointer compiled in yet**.
- `api/routes_chat.py` — `POST /chat` taking `{user_id, thread_id, message}`. Before invoking the graph, insert the user message into `messages`. After the graph returns, insert the assistant message (and, if you want visibility, tool-call messages) into `messages`.

### 💡 Core Pattern
```python
# The point of this snippet: message persistence is YOUR code, called
# explicitly around the graph invocation — it is not something LangGraph
# does for you, because LangGraph doesn't know about your `messages` table.
async def chat(req: ChatRequest, db: AsyncSession):
    await save_message(db, req.thread_id, role="user", content=req.message)

    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=req.message)]},
        config={"configurable": {"thread_id": req.thread_id}},
    )
    reply = result["messages"][-1]

    await save_message(db, req.thread_id, role="assistant", content=reply.content)
    return {"thread_id": req.thread_id, "answer": reply.content}
```

Notice: without a checkpointer, `graph.ainvoke` starts from an **empty** `messages` state every call — the `[HumanMessage(...)]` you pass in is the *entire* input, not appended to prior state. If you send two messages in the same thread right now, the agent has no idea the first one happened, even though it's sitting in your Postgres `messages` table. Confirm this yourself — it's the clearest possible demonstration that Postgres-persisted history and in-graph state are not automatically the same thing.

### 🤖 AI Build Prompt
```text
Using langgraph>=1.2 and langchain-openai, generate:
1. src/app/agent/tools.py — one LangChain tool, search_sailings(ship_name:
   str | None, month: str | None), querying the `sailings` table (async
   SQLAlchemy session) and returning a short list of matching sailings.
2. src/app/agent/graph.py — a StateGraph with a MessagesState-style
   schema (messages: Annotated[list[AnyMessage], add_messages]), an
   agent node calling ChatOpenAI bound to the tool, a ToolNode, and a
   conditional edge using tools_condition. Compile WITHOUT a
   checkpointer for now — that's the next lesson.
3. src/app/api/routes_chat.py — POST /chat({user_id, thread_id, message})
   that persists the user message to `messages` before invoking the
   graph and the assistant's reply to `messages` after, using the
   schema from Lesson 1.
Do not add checkpointing, summarization, or long-term memory yet —
those are separate lessons.
```

### ✅ Done When
`POST /chat` twice in the same `thread_id` produces two rows each in `messages`, and you can demonstrate — by asking a follow-up question that depends on the first message — that the agent currently has no memory of the first turn.

### 🔑 Concepts You Must Be Able to Explain
Why `messages` (Postgres) having full history didn't stop the agent from "forgetting" — and why that's not a bug, it's the expected behavior of an uncheckpointed graph.

### ⏱️ ~40 minutes

---

## 4. Lesson 4 — LangGraph Postgres Checkpointing & Thread Recovery

### 🎯 Objective
Close the gap from Lesson 3: compile the graph with a Postgres checkpointer so the agent actually continues a conversation across calls — and across server restarts.

### 🧠 Why This Matters
This is the lesson that makes "checkpoint ≠ conversation history" stop being an abstract claim and become something you can point at in two different Postgres schemas: your own `messages` table, and the entirely separate tables `checkpointer.setup()` creates for you, which you never touch directly.

### 📥 Assumed State
Lesson 3's uncheckpointed agent works and you've confirmed it "forgets" between calls.

### 🛠️ What To Build
- A pooled `AsyncConnectionPool` (psycopg3) dedicated to the checkpointer.
- `AsyncPostgresSaver(pool)`, with `.setup()` called once at startup.
- Recompile the graph: `builder.compile(checkpointer=checkpointer)`.
- Update `routes_chat.py`: keep passing only the *new* `HumanMessage` as input (not the full history) — the checkpointer now handles reloading prior state for you.
- A debug endpoint `GET /debug/threads/{thread_id}/checkpoint` that calls `graph.aget_state(config)` and returns the raw state — this is your window into "what does the graph currently believe," separate from what `messages` says.

### 💡 Core Pattern
```python
# AsyncConnectionPool lives in psycopg_pool — a SEPARATE distribution from
# psycopg itself. Install it via `uv add "psycopg[pool]"` (or standalone
# `psycopg-pool`) if you haven't already — `psycopg[binary]` alone does
# not include it, and this is the single most common import error at
# this step.
from psycopg_pool import AsyncConnectionPool

# Setup, once at startup:
pool = AsyncConnectionPool(conninfo=DATABASE_URL, max_size=10, open=False)
await pool.open()
checkpointer = AsyncPostgresSaver(pool)
await checkpointer.setup()          # idempotent — creates checkpoint tables once
graph = builder.compile(checkpointer=checkpointer)

# Per request — note you STILL only pass the new message, not full history.
# The checkpointer is what makes that sufficient now:
result = await graph.ainvoke(
    {"messages": [HumanMessage(content=req.message)]},
    config={"configurable": {"thread_id": req.thread_id}},
)
```

### 🤖 AI Build Prompt
```text
Using langgraph-checkpoint-postgres (AsyncPostgresSaver) and the graph
from the previous lesson:
1. Add a pooled psycopg3 AsyncConnectionPool (from the psycopg_pool
   package — ensure "psycopg[pool]" or "psycopg-pool" is installed,
   not just "psycopg[binary]") created at FastAPI startup and closed
   at shutdown.
2. Instantiate AsyncPostgresSaver(pool), call .setup() once at startup.
3. Recompile the graph with checkpointer=checkpointer.
4. Add GET /debug/threads/{thread_id}/checkpoint that calls
   graph.aget_state({"configurable": {"thread_id": thread_id}}) and
   returns the values dict as JSON.
Do not touch the `messages`, `summaries`, or `long_term_memories`
tables in this lesson — checkpointing is a separate persistence path
from those.
```

### ✅ Done When
You can: chat in a thread, ask a follow-up that depends on the first message and get a correct answer, **stop the FastAPI process, restart it**, continue the same `thread_id`, and the agent still has full context — with zero code re-sending prior messages. Then compare `GET /debug/threads/{thread_id}/checkpoint` against `GET /threads/{thread_id}/messages` (if you built that debug route) and see two structurally different representations of "the conversation so far."

### 🔑 Concepts You Must Be Able to Explain
Why the checkpointer needing its own tables (separate from `messages`) is a deliberate design, not duplication — one is durable execution state (arbitrary graph channels, resumable mid-tool-call), the other is your application's canonical, audit-friendly transcript.

### ⏭️ Deferred to Full Roadmap
The `checkpoint_metadata` convenience table for a debug UI — you don't need it, `aget_state` is sufficient for this crash course.

### ⏱️ ~30 minutes

---

## 5. Lesson 5 — Manual Summarization From Scratch

*(This is the flagship lesson of the whole crash course — spend the time here before touching LangMem.)*

### 🎯 Objective
Implement conversation summarization entirely by hand: define a threshold, generate a summary via an explicit LLM call, persist it, and inject it into the next turn's context — with zero framework help. You should be able to draw the full data flow from memory before Lesson 6 shows you the shortcut.

### 🧠 Why This Matters
If you learn LangMem's `SummarizationNode` first, you'll be able to use it without being able to explain what it's doing — and the first time it misbehaves in production, you won't know where to look. Building this by hand once means every later abstraction is legible instead of magic. This is also where "context" (Lesson 2) stops being abstract: you're about to write the exact function that assembles it.

### 📥 Assumed State
Checkpointed agent from Lesson 4 works. You'll add a step *before* the agent node runs.

### 🛠️ What To Build
`memory/manual_summarizer.py` implementing this flow, run before every LLM call:

```text
1. Count raw messages in `messages` for this thread since the last
   summary's covered_until_message_id (or from the start, if none).
2. If count > 10:
     a. Fetch all messages except the most recent 6.
     b. Call the LLM once: "Summarize this conversation segment,
        preserving facts, decisions, and preferences."
     c. Persist to `summaries`: thread_id, summary_text,
        covered_until_message_id = id of the last message just
        summarized, strategy = 'manual'.
3. Build context for the agent node:
     system_prompt
     + latest summary (if one exists), injected as part of the system
       message — e.g. "Earlier in this conversation: {summary_text}"
     + last 6 raw messages from `messages`
     + the current user message
```

### 💡 Core Pattern
```python
async def get_context_for_turn(db: AsyncSession, thread_id: str, current_message: str) -> list[AnyMessage]:
    summary = await get_latest_summary(db, thread_id)
    recent = await get_messages_after(db, thread_id, after_id=summary.covered_until_message_id if summary else None, limit=6)

    system = SYSTEM_PROMPT
    if summary:
        system += f"\n\nEarlier in this conversation:\n{summary.summary_text}"

    return [SystemMessage(content=system), *to_langchain_messages(recent), HumanMessage(content=current_message)]


async def maybe_summarize(db: AsyncSession, thread_id: str) -> None:
    """Call this BEFORE building context for a turn — never after,
    or the newest turn gets folded into the summary a message too early."""
    unsummarized_count = await count_messages_since_last_summary(db, thread_id)
    if unsummarized_count <= 10:
        return

    to_summarize = await get_messages_to_summarize(db, thread_id, keep_recent=6)
    prompt = "Summarize this conversation segment. Preserve facts, decisions, and stated preferences:\n\n"
    prompt += format_messages_for_prompt(to_summarize)

    summary_text = (await summarizer_model.ainvoke(prompt)).content

    await save_summary(
        db, thread_id,
        summary_text=summary_text,
        covered_until_message_id=to_summarize[-1].id,
        strategy="manual",
    )
```

Note the ordering guarantee `covered_until_message_id` gives you: it's what stops you re-summarizing the same messages on every turn once you're over the threshold — without it, you'd either re-summarize (wasted LLM calls, drifting summaries) or double-count.

Also note the important interaction with the checkpointer from Lesson 4: **the checkpointer still holds the full, unsummarized message history in its own state** — it doesn't know or care that you're summarizing anything, because it's checkpointing whatever you pass into the graph. If you want the *graph's* context to actually shrink (not just your manual context-assembly function), you have two options worth understanding as a real design decision rather than a detail: (a) keep feeding the graph only the trimmed/summarized context you build here, bypassing whatever's in the checkpoint, or (b) actively prune the checkpointed `messages` channel using `RemoveMessage` the way LangMem's node does in Lesson 6. Doing it manually here, you'll almost always want (a) for simplicity — build context explicitly every turn rather than trying to mutate checkpointed state by hand.

### 🤖 AI Build Prompt
```text
Implement src/app/memory/manual_summarizer.py with two async functions
against the schema from Lesson 1 (`messages`, `summaries` tables):

1. maybe_summarize(db, thread_id) — if more than 10 messages exist
   since the last summary's covered_until_message_id (or since thread
   start if no summary exists yet), call ChatOpenAI once to summarize
   all but the most recent 6 messages, and persist a new row to
   `summaries` with strategy='manual' and the correct
   covered_until_message_id.

2. get_context_for_turn(db, thread_id, current_message) — returns a
   list of LangChain messages: a system message (base prompt + latest
   summary text if one exists), the most recent 6 raw messages from
   `messages`, then the current user message as a HumanMessage.

Wire maybe_summarize() to run before get_context_for_turn() on every
POST /chat call, and pass the result of get_context_for_turn() as the
graph's input `messages` for that invocation instead of just the
single new HumanMessage.

Add GET /debug/threads/{thread_id}/summary returning the latest
summary row, raw message count since it, and whether summarization
would trigger on the next turn.
```

### ✅ Done When
You can have an 12+ message conversation, confirm a `summaries` row was created after message 11, confirm the debug endpoint shows the correct `covered_until_message_id`, and confirm — by asking about something from early in the conversation — that the agent still answers correctly using the injected summary rather than the (now-excluded) raw early messages.

### 🔑 Concepts You Must Be Able to Explain
Why `covered_until_message_id` exists; why summarization must run *before* context assembly, not after; why the checkpointer's own state and your manually-assembled context can silently diverge if you're not deliberate about which one you feed the graph.

### ⏱️ ~50 minutes

---

## 6. Lesson 6 — Framework-Native Summarization with LangMem

### 🎯 Objective
Reimplement Lesson 5's behavior using LangMem's `summarize_messages` and, separately, its `SummarizationNode`, and be able to say precisely what each one buys you over your manual version.

### 🧠 Why This Matters
This is the payoff lesson — everything LangMem does here is legible to you now, because you built the same thing by hand first. The point isn't "LangMem is better," it's understanding exactly which parts of your manual code it's replacing and which parts (thresholds, persistence, injection policy) remain your decision regardless of which approach you use.

### 📥 Assumed State
Lesson 5's manual summarizer works and you understand its data flow.

### 🛠️ What To Build
Two variants, toggled by `conversation_threads.summary_mode`:

**Variant A — `summarize_messages` (function-style, called before the model node, same shape as your manual pre-processing step):**
```python
from langmem.short_term import summarize_messages
from langchain_core.messages.utils import count_tokens_approximately

summarized, running_summary = summarize_messages(
    messages,
    running_summary=previous_running_summary,   # you still persist this yourself
    model=summarizer_model,
    max_tokens_before_summary=3000,
    max_summary_tokens=512,
    token_counter=count_tokens_approximately,
)
# You still write `running_summary` to your `summaries` table — LangMem
# doesn't know your schema exists.
```

**Variant B — `SummarizationNode` (graph-native, a formal node in the graph instead of a pre-processing function you call manually):**
```python
from langmem.short_term import SummarizationNode

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarizer_model,
    max_tokens=3000,
    max_summary_tokens=512,
    output_messages_key="llm_input_messages",  # writes to a SEPARATE state
                                                 # key — your checkpointed
                                                 # `messages` channel stays
                                                 # untouched and full-fidelity
)
# Add as a graph node before your agent node; agent node reads from
# state["llm_input_messages"] instead of state["messages"].
```

### 🤖 AI Build Prompt
```text
Add two summarization modes to src/app/memory/langmem_summarizer.py,
selected by conversation_threads.summary_mode:

1. "langmem_function": before invoking the graph, call
   langmem.short_term.summarize_messages on the thread's messages,
   using max_tokens_before_summary=3000, max_summary_tokens=512.
   Persist the returned running_summary to the `summaries` table
   with strategy='langmem'. Use it to build context the same way
   Lesson 5's get_context_for_turn does.

2. "langmem_node": add langmem.short_term.SummarizationNode as a node
   in the graph (src/app/agent/graph.py) before the agent node, with
   output_messages_key="llm_input_messages", max_tokens=3000,
   max_summary_tokens=512. Update the agent node to read from
   state["llm_input_messages"] instead of state["messages"] when
   assembling the prompt, while state["messages"] continues to hold
   full, unsummarized history via the checkpointer.

Add support for summary_mode in ["manual", "langmem_function",
"langmem_node"] in POST /chat, dispatching to the right implementation.
Extend GET /debug/threads/{thread_id}/summary to show which mode is
active, raw message count, and whether a summary currently exists.
```

### ✅ Done When
You can switch a thread between all three modes (`manual`, `langmem_function`, `langmem_node`) via `conversation_threads.summary_mode` and get correct summarization behavior in each, and you can articulate — without looking anything up — why `SummarizationNode` writing to `output_messages_key` instead of overwriting `messages` matters (it keeps your checkpointed transcript full-fidelity, exactly like the audit-friendly design decision your `messages` table already embodies).

### 🔑 Concepts You Must Be Able to Explain
`summarize_messages` is function-style (you call it, like your manual version); `SummarizationNode` is graph-node style (it's part of the graph's execution flow). Neither replaces your `messages` table as the durable transcript — both only ever affect what gets *sent* to the model. Manual gives you full control over persistence format and business-specific summary rules; LangMem gives you less code and a maintained running-summary implementation, at the cost of your database schema needing to accommodate however LangMem structures its output.

### 📌 A Fourth Option You Should Know Exists
LangChain's own `create_agent` (its 1.0 high-level agent API, separate from hand-built `StateGraph`s like the one you're using here) ships a first-party `SummarizationMiddleware` that does token-threshold summarization declaratively — `middleware=[SummarizationMiddleware(model=..., trigger=("tokens", 4000), keep=("messages", 20))]` — with no LangMem dependency at all. It's not a fit for this lesson (it only attaches to `create_agent`, not to a custom `StateGraph` you're wiring by hand), but it's the option you'd reach for if you rebuild this agent on top of `create_agent` later. Lesson 8's comparison table places it alongside the other three.

### ⏱️ ~35 minutes

---

## 7. Lesson 7 — Long-Term Memory: Classification, Storage, Retrieval

### 🎯 Objective
Add the last piece: durable, cross-thread facts about a user, distinct from anything thread-scoped.

### 🧠 Why This Matters
Everything so far — checkpoints, summaries — is scoped to one `thread_id`. Start a new thread with the same user and all of it is gone; that's correct behavior for short-term memory, and exactly the gap long-term memory exists to fill. This is also where "not everything should be remembered" becomes a real engineering decision you have to encode, not just a nice idea.

### 📥 Assumed State
Any summarization mode from Lesson 5/6 works.

### 🛠️ What To Build
- `memory/long_term_memory.py`: after each assistant turn, an LLM classification call deciding whether anything in the exchange is durable, using exactly these categories (from the original roadmap, kept as-is — they're a good minimal taxonomy):
  `travel_preference`, `communication_preference`, `profile`, `currency_preference`, `ignore`.
- If classified as anything but `ignore`, persist to `long_term_memories` with `confidence`, `source_thread_id`.
- Before building context for a turn, retrieve active `long_term_memories` for the `user_id` and inject them into the system message alongside (not instead of) the summary.
- `GET /debug/users/{user_id}/memories` and `DELETE .../{memory_id}` — long-term memory must be inspectable and correctable, not a black box.

### 💡 Core Pattern
```python
CLASSIFY_PROMPT = """Classify whether this exchange contains a durable,
reusable fact about the user. Categories: travel_preference,
communication_preference, profile, currency_preference, ignore.
Only classify as non-'ignore' if the fact would still be true and
useful in a completely different conversation next month.
Respond with just the category and, if not 'ignore', the fact in one
sentence."""

async def classify_and_store(db, user_id, thread_id, exchange):
    result = await classifier_model.ainvoke([
        SystemMessage(content=CLASSIFY_PROMPT),
        HumanMessage(content=exchange),
    ])
    category, fact = parse_classification(result.content)
    if category == "ignore":
        return
    await save_long_term_memory(
        db, user_id=user_id, memory_type=category, content=fact,
        confidence=0.8, source_thread_id=thread_id, status="active",
    )

async def get_active_memories(db, user_id) -> list[str]:
    rows = await fetch_memories(db, user_id, status="active")
    return [r.content for r in rows]
```

Injection point — this is the piece that makes long-term memory actually *do* something, easy to build and easy to forget:
```python
memories = await get_active_memories(db, user_id)
if memories:
    system += "\n\nRelevant facts about this user:\n" + "\n".join(f"- {m}" for m in memories)
```

### 🤖 AI Build Prompt
```text
Implement src/app/memory/long_term_memory.py against the
`long_term_memories` table:

1. classify_and_store(db, user_id, thread_id, exchange_text) — one
   LLM call classifying the exchange into travel_preference,
   communication_preference, profile, currency_preference, or ignore.
   Persist non-'ignore' results with confidence=0.8 and
   source_thread_id set.

2. get_active_memories(db, user_id) -> list[str] — returns content of
   all status='active' rows for this user.

Wire classify_and_store to run after every assistant turn (as a
background task, not blocking the response). Wire get_active_memories
into context assembly (in both the manual and LangMem paths from
Lessons 5-6) — inject as a "Relevant facts about this user" block in
the system message, alongside whatever summary is active.

Add GET /debug/users/{user_id}/memories and
DELETE /debug/users/{user_id}/memories/{memory_id} (soft delete —
set status='deleted', don't hard-delete the row).
```

### ✅ Done When
State a preference in thread A ("I always want prices in INR"), start a *brand new* `thread_id` for the same user, and confirm the agent already knows the preference without you restating it — with zero relationship to the checkpoint or summary from thread A, because both of those are thread-scoped and this isn't.

### 🔑 Concepts You Must Be Able to Explain
Why long-term memory is deliberately not automatic for every message — the classification step is a filter, and getting that filter's judgment wrong in either direction (too aggressive = false memories bias future answers invisibly; too conservative = the assistant never learns anything) is a real production tuning problem, not a solved one. Why long-term memory needs `source_thread_id` and to be deletable — unlike a summary, which is disposable and regeneratable, a wrong long-term memory silently corrupts every future conversation until someone finds and removes it.

### ⏭️ Deferred to Full Roadmap
Semantic/embedding-based memory retrieval (pgvector) — this crash course uses "load all active memories for the user," which is fine at low volume; retrieval-by-relevance is a Week 3+ concern once a user has dozens of memories. Also deferred: LangMem's own `create_memory_store_manager`/`create_manage_memory_tool` agent-invoked pattern — worth knowing exists (an alternative to this lesson's scheduled-classification approach, where the agent itself decides mid-conversation to save a memory via tool call), but the classification-pass approach above is more legible for a first build and sufficient for the full roadmap's demo requirements.

### ⏱️ ~30 minutes

---

## 8. Lesson 8 — Recap, Comparison, and Bridge Back to the Full Roadmap

### 🎯 Objective
Consolidate what you built into language you can defend in a design review or interview, and know exactly what to build next.

### 🧠 Full System Recap
```text
messages              → raw transcript, source of truth, never lossy
checkpointer's tables  → LangGraph execution state, thread-scoped, for
                          crash recovery/resumability (not for display)
summaries              → your compressed context, thread-scoped
long_term_memories     → durable facts, user-scoped, cross-thread
context (never stored) → assembled fresh each turn from all of the above
```

### 📊 Manual vs. LangMem vs. LangChain Middleware — When to Choose Which

| | Manual | `summarize_messages` | `SummarizationNode` | `SummarizationMiddleware` (LangChain 1.0, `create_agent` only) |
|---|---|---|---|---|
| Control over summary format/persistence | Full | Partial — you still own persistence | Partial — you still own persistence | Least — declarative config, persistence is your responsibility if you need it durably |
| Code you maintain | Most | Less | Least | Least |
| Where it runs | Your pre-processing function | Your pre-processing function | Formal graph node | Middleware hook inside `create_agent`'s loop |
| Requires | Nothing extra | `langmem` | `langmem` | `langchain` core only — no `langmem` dependency |
| Works with a hand-built `StateGraph`? | Yes | Yes | Yes | No — only attaches to `create_agent` |
| Best for | Learning, business-specific summary rules, strict auditability | Quick token-threshold summarization with less custom code | When summarization should be visible as a first-class step in the graph itself | Rebuilding on `create_agent` instead of a custom graph; fastest path if you don't need a custom `StateGraph` |
| Risk | More surface area for bugs (thresholds, edge cases) | Less control if requirements get bespoke | Coupling your context strategy to LangMem's node lifecycle | Couples your agent architecture to `create_agent` instead of a graph you fully control |

None of the four touch your `messages` table — that's a constant across all of them, and worth stating explicitly if asked: **summarization strategy is a context-assembly decision, never a transcript-storage decision.** This crash course builds the first three because a hand-built `StateGraph` is what makes the mechanism visible; `SummarizationMiddleware` is included here only so you know it exists when you evaluate `create_agent` for a future project.

### 🌉 Bridge to the Full 3-Week Roadmap
You've now built the memory-critical parts of the original roadmap's Lessons 2.1–2.4 and 3.1–3.3, in a simplified domain. Returning to the full roadmap, here's exactly what's left and why each was deferred:

| Original Lesson | Status | Why deferred here |
|---|---|---|
| 1.1 Project setup, layered structure | Partial | You used a flat structure; full roadmap wants domain/repositories/services separation for a larger codebase |
| 1.2 Full domain model (ships, bookings) | Skipped | One `sailings` table was enough to prove the memory mechanisms |
| 1.3 Fare calculation, multiple tools | Skipped | One tool was enough to prove tool-results-enter-context |
| 2.1–2.4 Agent, threads, checkpointing, manual summary | ✅ Done | This crash course |
| 3.1–3.3 Long-term memory, LangMem | ✅ Done | This crash course |
| 3.4 React + Tailwind UI | Not started | Pure demo polish, zero memory-architecture content |
| 3.5 Tests, logging, README, interview polish | Not started | Production hygiene, not a memory concept |
| Alembic migrations | Not started | `create_all` was fine for a throwaway crash-course DB |

Nothing about the memory architecture itself needs to be redone — you're extending the same tables and the same graph, just adding domain breadth and production polish around it.

### ⏱️ ~15 minutes

---

## Appendix — What This Crash Course Never Builds (By Design, Not Just "Later")

Carried over unchanged from the full roadmap's own list, because these were never in scope for this project at all, crash course or not: authentication, real cruise supplier APIs, payment flow, Redis, Kafka, vector database, Kubernetes, multi-agent architecture, complex role permissions, admin dashboard, mobile UI, voice interface.
