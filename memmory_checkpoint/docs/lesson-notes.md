# Lesson Notes & Decision Log — LangGraph Memory Crash Course

> Retrospective notes, written at the end of each lesson: what we learned, what we decided and why, what broke and how it got fixed, and the exact commands used. Meant to stand on its own — if you're picking this project back up weeks later, or this is a new Claude session, start here before re-reading the full roadmap.

---

## Lesson 1 — Prerequisites & Project Setup

### Key concepts learned
- **`uv`** as the project/dependency manager — lockfile-based (`uv.lock`), replaces the pip + venv + requirements.txt combo, resolves dependencies deterministically.
- **`src` layout** — code lives at `src/app/`, not the project root. Keeps "the installed package" and "the project root" cleanly separated so imports can't work "by accident" via the current working directory being on `sys.path`.
- **pydantic-settings `BaseSettings`** — typed, validated, fail-fast application configuration sourced from `.env`. A missing required setting raises at startup, not mid-request.
- **SQLAlchemy 2.0 async ORM** — `Engine` (the connection pool, created once per process) vs. `Session` (one per unit of work / request); typed `Mapped`/`mapped_column` declarative models; the Unit-of-Work pattern (`session.add()` stages a change, `session.commit()` persists it, nothing touches the DB in between).
- **FastAPI `lifespan`** — one async context manager for startup + shutdown, the modern replacement for the older `@app.on_event("startup")` / `@app.on_event("shutdown")` decorator pair.
- **`create_all()` vs. Alembic** — `create_all()` only knows "does this table exist yet." Fine for a throwaway crash-course DB; not a substitute for real migrations once the schema needs to *change* over time rather than just be created once.

### Important decisions & why
- **`psycopg[binary,pool]`**, not just `psycopg[binary]` — `AsyncConnectionPool`/`ConnectionPool` live in the separate `psycopg_pool` distribution. `binary` alone only gets you the compiled C driver, not pooling.
- **Explicit `[build-system]` + `[tool.hatch.build.targets.wheel] packages = ["src/app"]`** added to `pyproject.toml` — without it, hatchling can't auto-map `src/app` to the importable name `app`, because the project name (`memmory_checkpoint`) doesn't match the package directory name (`app`). Without this, nothing was actually being installed as a package at all.
- **`BigInteger` primary keys** on `messages`, `summaries`, `long_term_memories` (high-growth, append-only tables) vs. plain 32-bit `int` on `users`/`sailings` (small, slow-growing reference tables) — avoids a genuinely painful primary-key-type migration later, once other tables hold foreign keys pointing at it.
- **`server_default=func.now()`**, not a Python-side `default=` — timestamp correctness shouldn't depend on which app server (or which client, e.g. `psql` directly) performed the insert.
- **`Numeric(10, 2)` for `adult_fare`**, never `Float` — money must never be represented as binary floating point (`0.1 + 0.2 != 0.3`).
- **Explicit `index=True` on every foreign-key column** (`user_id`, `thread_id`, `source_thread_id`) — Postgres indexes primary keys automatically but *not* foreign keys. Invisible with 5 seed rows; a real sequential-scan problem once `messages` has millions of rows and every chat request filters by `thread_id`.
- **No cascade deletes** on any foreign key — deliberate. `messages` is meant to be a permanent, audit-friendly transcript; `ON DELETE CASCADE` would mean deleting a `conversation_thread` silently destroys its history.

### Bugs hit and fixes (keep these — some will resurface in later lessons)

1. **`ModuleNotFoundError: No module named 'app'`** when running `from app.core.config import ...`, but `from src.app.core.config import ...` worked. Root cause: `pyproject.toml` had no `[build-system]` section, so `uv sync` never actually installed `src/app` as the package `app` — the `src.app...` import only "worked" as a side effect of Python adding the current working directory to `sys.path` for `python -c`. Fixed by adding the hatchling config above and re-running `uv sync`.
2. **`UndefinedTable: relation "users" does not exist`** — models existed in Python but `CREATE TABLE` had never run against Postgres. Fixed with a standalone `db/create_tables.py` script (`Base.metadata.create_all()`), and permanently via `main.py`'s `lifespan` startup hook.
3. **`InterfaceError` running the seed script on Windows** — psycopg3's async mode is incompatible with Windows' default `ProactorEventLoop`; it needs `SelectorEventLoop`. Fixed with:
   ```python
   import sys, asyncio
   if sys.platform == "win32":
       asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
   ```
   applied before `asyncio.run(...)` in every standalone script (`seed.py`, `create_tables.py`), and at import time in `main.py` for the live server process.
4. **Same event-loop issue resurfaces inside uvicorn itself** — recent uvicorn versions (0.36+) have a known regression where setting the event loop policy before starting the server doesn't reliably take effect. Worked around by explicitly passing `--loop asyncio` on the command line, in addition to the module-level guard in `main.py`.
5. **`AsyncGenerator[AsyncSession:None]` typo** in `session.py` — a colon instead of a comma turns this into Python *slice* syntax (`slice(AsyncSession, None)`), silently passing the wrong thing to a generic type instead of the two expected type arguments. Fixed to `AsyncGenerator[AsyncSession, None]`.
6. **`fastapi dev app.main.py` → "Path Does not Exist"** — `fastapi dev` takes an actual file *path* (e.g. `fastapi dev src/app/main.py`), not a dotted module string like uvicorn's `app.main:app`. Standardizing on the uvicorn invocation for this project since FastAPI CLI has no `--loop` flag to control the Windows fix above.

### Commands used
```powershell
uv init --python 3.13
uv add "fastapi[standard]" langchain langchain-openai langgraph langgraph-checkpoint-postgres langmem openai "psycopg[binary,pool]" pydantic-settings python-dotenv sqlalchemy
uv add --dev mypy ruff
uv sync
uv run python -c "from app.core.config import get_settings; print(get_settings().app_env)"
uv run python -m app.db.create_tables
uv run python -m app.db.seed
uv run uvicorn app.main:app --reload --loop asyncio
```

---

## Lesson 2 — The Memory Mental Model

Conceptual lesson, no code. Goal: never conflate five terms that map 1:1 onto Lesson 1's schema (plus one table that doesn't exist yet).

### The five terms
- **Context** — the literal tokens sent to the LLM on *this* call. Ephemeral, assembled fresh every turn, never itself stored anywhere. Mental model: like props passed into a React component on a single render — built from current state, discarded once that render is done.
- **Conversation history** — the raw, append-only log of everything exchanged in a thread. Lives in `messages`. Source of truth, never lossy, never edited.
- **Short-term memory** — the thread-scoped *strategy* for turning history into context (which recent raw messages + which summary get sent this turn). Lives partly in `summaries`, partly in the checkpointer's state.
- **Long-term memory** — durable, user-scoped facts that outlive any single thread. Lives in `long_term_memories`, retrieved by `user_id` across every future thread, not just the current one.
- **Checkpoint** — a snapshot of LangGraph's own execution state (every state channel, not just messages), taken after each step the graph takes, keyed by `thread_id`. For crash recovery and mid-execution resumability — not something the application reads from directly, and not part of context assembly.

### Core relationship (the one sentence worth memorizing)
`messages` is truth → `summaries` is compressed truth for one thread → `long_term_memories` is durable truth across threads → the checkpoint is separate execution-state plumbing that happens to also durably hold a working copy of recent messages internally.

### The one misconception worth remembering
Self-check Q3 ("resume this conversation after a crash — which table?") was answered as `conversation_threads`, reasoning that its `thread_id` gets passed to the checkpointer. The `thread_id`-as-shared-key instinct was actually correct and important — but `conversation_threads` itself is only an application-level registry (which thread exists, which user owns it, which summary mode it uses). It holds **zero** information about what the graph was doing mid-execution.

The real answer: **the checkpointer's own tables — separate ones, created in Lesson 4 via `checkpointer.setup()`, not any of the six tables built in Lesson 1.** They live in the same `langgraph_memmory` database but are a wholly separate schema that LangGraph manages internally; the app never writes to them directly, only through the checkpointer's API (`.put()`, `.get_tuple()`), called internally by `graph.ainvoke()` / `graph.aget_state()`.

The precise mechanic: a checkpoint is written after **each step** the graph takes — not once per full user turn. A tool call is one step; the LLM processing that tool's result is another. That granularity is what lets LangGraph resume mid-tool-call after a crash, not just "replay the user's last message." The connective tissue between the app's own tables and LangGraph's separate ones is exactly the `thread_id` string — one shared key, two independent storage systems. That's the concrete version of "checkpoint ≠ conversation history, deliberately, not by accident."

### Self-check results
1. "Show me everything the user has ever said" → `messages`. Correct on first attempt.
2. "Does the assistant know I prefer balcony cabins" → `long_term_memories`. Correct on first attempt, with the added (accurate) insight that this gets injected into context as instruction — correctly anticipating Lesson 7.
3. "Resume this conversation after a crash" → corrected from `conversation_threads` to the checkpointer's own tables (see above).

---

## Lesson 3 — Minimal Tool-Calling Agent + Raw Transcript Persistence

### Key concepts learned
- **`@tool` decorator** — turns a plain async function into something an LLM can invoke. It does not execute anything itself; it generates a JSON schema from the function's type hints + docstring, and the model returns a message containing a *request* to call it with certain arguments. The docstring is the only contract the LLM has with the function — there's no compiler to catch drift the way TypeScript would catch an interface mismatch.
- **`StateGraph` as a reducer** — the closest frontend analogy is `useReducer`/Redux: the graph has a typed `state` shape, nodes are functions that read the full state and return a *partial* update, and a reducer function decides how each key merges old + new. `add_messages` is LangGraph's built-in reducer for the `messages` key — it **appends**, it never overwrites, the same way a message-list reducer should never just replace the whole array on every dispatch.
- **`ToolNode` + `tools_condition`** — `ToolNode` is the node that actually executes whatever tool the model asked for and turns the result into a `ToolMessage`. `tools_condition` is a conditional edge: it inspects the last message in `state["messages"]`, and routes to the tools node if it has `tool_calls`, or to `END` if not. This is the graph-structure equivalent of an `if/else` inside a reducer's dispatch logic.
- **Checkpoint granularity, precisely** — a checkpoint is written after every graph *step*, not once per full user turn. A turn with no tool call is roughly one step (the agent node runs once). A turn where the model calls a tool is at least two steps: one where the model decides to call the tool, another where it reads the tool's result and replies. So across N message exchanges, the number of checkpoints is **N or more** — more, specifically, for every turn that involved a tool call — never fewer.
- **How resuming from a checkpoint actually works** — the key mental model: each checkpoint is a full, cumulative snapshot of state as of that point, not a delta. Analogy that clicked: a video game save file. Every save contains your *entire* progress so far, not just the latest move — so resuming only ever needs the *one* most recent save file, never all previous ones stitched together. LangGraph works the same way: loading checkpoint #40 already contains everything from turns 1–40 baked in. Turn 41's new message gets appended on top via the `add_messages` reducer, and the **whole resulting list** — all 40 prior exchanges plus the new one — is what gets sent to the model.
- **The real risk that follows from that** — a checkpointer has *no* concept of tokens, models, or context-window limits. It's dumb persistence: it saves whatever is in `state["messages"]`, however large that gets. Relying on a checkpointer alone, with no summarization, means every turn resends a larger and larger pile of history to the model — first as rising cost/latency, eventually as a hard context-window failure. This is *why* checkpointing (Lesson 4) and summarization (Lesson 5/6) are treated as two separate, independent mechanisms rather than one feature: checkpointing solves "does the graph survive a crash and remember," summarization solves "does what actually gets sent to the model stay a sane size." Solving the first does not solve the second.

### Important decisions & why
- **Hand-built `StateGraph` instead of `create_react_agent`** — LangGraph ships a one-line shortcut that would produce a working tool-calling agent immediately. Deliberately not used here: it hides exactly the mechanism (state, reducer, conditional routing) this lesson exists to teach. Revisited later (Lesson 8) as a legitimate production option once the underlying mechanics are understood, not a black box.
- **Tool opens its own `AsyncSession` per call** rather than accepting an injected session — simplest thing that works for a single-tool crash course. Tradeoff flagged: the tool doesn't share a transaction with the rest of the `/chat` request. At production scale with several DB-backed tools per turn, this would more likely move to a shared session injected via context, to avoid connection-pool churn and to keep multiple tool calls in one turn transactionally consistent.
- **`.where()` / `.ilike()` for the tool's query, never an f-string** — tool arguments come from the LLM, which functionally means they should be treated as untrusted input, same as HTTP request params. SQLAlchemy's query-builder methods parameterize values automatically; string-concatenating LLM-supplied values into raw SQL would be a real SQL-injection surface.
- **`.limit(5)` inside `search_sailings`** — a tool that can return an unbounded result set is a production failure mode in its own right (blown context window, runaway token cost), independent of the summarization discussion above.
- **Commit the user's message to Postgres *before* invoking the graph, not after** — so the user's message is durable even if the (possibly slow, possibly failing) LLM call times out or errors downstream.
- **`_ensure_thread` helper in the route** — creates the `conversation_threads` row on first use of a new `thread_id`, before inserting into `messages`. Without it, a genuinely new thread hits a foreign-key violation immediately, since `messages.thread_id` references `conversation_threads.thread_id`.
- **Compiled the graph with no checkpointer, and the route sends only the new `HumanMessage`** — both deliberate, matching the lesson's point: this combination is what makes the forgetting behavior visible and provable, rather than something to avoid yet.

### Bugs hit and fixes
None this lesson — `tools.py`, `graph.py`, and `routes_chat.py` were empty (0 bytes) going in, with some stale `.pyc` bytecode left over in `__pycache__` from before they were emptied. Noted, not investigated further (no functional impact — bytecode cache regenerates from whatever source is currently on disk).

### Commands used
No new `uv add` — every package this lesson needs (`langchain-openai`, `langgraph`, `langchain` core for `@tool`) was already installed in Lesson 1.

Manual test of the two Done-When checks, same `thread_id`, run twice:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "thread_id": "thread_1_test", "message": "Are there any sailings on the Ocean Voyager?"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "thread_id": "thread_1_test", "message": "What was the fare on that one again?"}'
```

### Self-check / confirmation results
- 3.4 confirmed via a live view of the `messages` table (pgAdmin/DB client) — each `POST /chat` call produced one `user` row and one `assistant` row, correctly tied to `thread_1_test`.
- 3.5 confirmed in the same data: "Are there any sailings on the Ocean Voyager?" → correct "no sailings" answer; immediately followed by "What was the fare on that one again?" → "Could you please specify which cruise or sailing you're referring to?" — clean proof the agent had zero memory of the first exchange.
- 3.6 explain-back: root cause identified as "nothing about the previous turn is present in the input to the second call" — correctly named both valid remedies (a checkpointer auto-reinjecting prior state, *or* manually re-assembling and passing full history yourself), and correctly recognized these aren't independent bugs stacked together, they're two sides of one mechanism, with Lesson 4 wiring in the first and Lesson 5 wiring in the second.
- Follow-up concept (checkpoint count for 40 exchanges, and whether turn 41 "contains" all 40 checkpoints) worked through using the video-game-save-file analogy above — resolved cleanly on the second pass after dialing back from a denser, more academic explanation style to a plainer, mentor-style one. That plain, one-idea-at-a-time, short-sentence explanation style is now the standing default for this course (recorded in `claude/teaching-preferences.md`).

---

## Lesson 4 — LangGraph Postgres Checkpointing & Thread Recovery

### Key concepts learned
- **Two separate connection pools, deliberately** — the SQLAlchemy `Engine` from Lesson 1 handles the app's own tables; a raw `psycopg_pool.AsyncConnectionPool` handles the checkpointer. `AsyncPostgresSaver` speaks raw `psycopg`, not SQLAlchemy, so it can't share the ORM's pool — two independent "fleets" against the same physical database.
- **`psycopg_pool.AsyncConnectionPool` current best practice** — construct with `open=False`, then explicitly `await pool.open()` / `await pool.close()` inside FastAPI's `lifespan`. Implicit opening at construction time is deprecated in current `psycopg_pool` versions. `kwargs={"row_factory": dict_row, "autocommit": True}` is required by `AsyncPostgresSaver` internals — dict-style row access, and `.setup()`'s DDL needing to commit immediately.
- **`AsyncPostgresSaver`** — LangGraph's Postgres implementation of the `BaseCheckpointSaver` interface (swap in `AsyncSqliteSaver` or an in-memory saver elsewhere without changing graph code). Takes the pool directly; one long-lived singleton instance, same rule as the engine.
- **`.setup()` is idempotent *and* versioned** — unlike Lesson 1's `create_all()` (which only ever checks "does this table exist"), `.setup()` tracks schema version in its own `checkpoint_migrations` table and applies only missing migrations. Safe to call on every app startup for a single instance; flagged as a place production teams often instead run migrations as a one-off deploy step, to avoid multiple replicas racing on concurrent DDL.
- **`compile(checkpointer=checkpointer)`** — turns on an automatic load → merge → save cycle around every `ainvoke()` call: load the latest checkpoint for the `thread_id` in `config`, merge the new input through the existing `add_messages` reducer, save the result back as the next checkpoint. Requires `config={"configurable": {"thread_id": ...}}` on every invoke — a compiled-with-checkpointer graph will error without it.
- **`graph.aget_state(config)`** — read-only: does not run any node, just loads the latest checkpoint for a thread. Returns a `StateSnapshot` with `.values` (the state dict, e.g. `messages`) and `.next` (a tuple of node(s) that would run next). Empty tuple `()` = the graph reached a clean stop (`END`). A non-empty value would mean the graph was captured mid-execution — e.g. paused right after requesting a tool call but before running it — which is the exact mechanism that lets a mid-tool-call crash resume correctly instead of restarting the whole turn from scratch.
- **How checkpoint data is actually stored** — `checkpoints` holds small JSON-ish metadata (thread_id, checkpoint_id, timestamps). `checkpoint_blobs` holds the heavy stuff — the actual message list — as `BYTEA` binary, packed by LangGraph's own serializer (not plain readable text). Not human-readable and not SQL-queryable by design; only LangGraph's own Python code ever unpacks it.
- **Checkpoint vs. `messages` — empirically confirmed, not just theoretical** — for the same thread, `messages` showed 6 rows but the debug endpoint reported `message_count: 8`. Root cause: `routes_chat.py` only ever persists the user's message and the *final* assistant reply to `messages`. The checkpointer captures *everything* in `state["messages"]` after every step, unconditionally — so one tool-call round trip (the `AIMessage` requesting the tool + the `ToolMessage` with its result) shows up in the checkpoint but never in `messages`. Confirms `messages` is a deliberately partial transcript (final answers only), while the checkpoint is the only place the full step-by-step reasoning durably lives.
- **Why separate tables is deliberate design, not duplication** — the data-type/access-path difference (binary vs. text, raw pool vs. SQLAlchemy ORM) is real but is a *symptom*, not the root cause. The actual reason: `messages` is a business-level, human-readable audit record, written by app code on the app's own schedule. The checkpoint tables are portable, library-owned execution state, written by LangGraph itself on every step, versioned independently via `checkpoint_migrations`. LangGraph's checkpointer ships identically to any app regardless of that app's own schema — it has no knowledge of `messages` and shouldn't need any, so that neither system's schema changes can ever break the other.

### Important decisions & why
- **`AsyncConnectionPool(open=False, ...)` + explicit `await pool.open()`/`await pool.close()` in `lifespan`** — matches current `psycopg_pool` guidance (avoids the deprecated implicit-open behavior) and the same "fail fast, explicit startup ordering" philosophy already used for the SQLAlchemy engine.
- **Two separate `.env` URLs for Postgres** — one SQLAlchemy-dialect URL (`postgresql+psycopg://...`) for the existing engine, one plain psycopg/libpq URL (`postgresql://...`) for the checkpointer pool — rather than deriving one from the other via string manipulation. More explicit and less fragile than stripping `+psycopg` programmatically; each library gets exactly the format it expects.
- **`min_size=5, max_size=20`** picked as a reasonable default for a single-instance crash-course app, with the explicit caveat that this isn't a universal number — real sizing has to account for Postgres's shared `max_connections` ceiling across *every* pool the app opens, multiplied by however many worker processes/replicas run concurrently.
- **`.setup()` called on every app startup** rather than as a separate one-off migration step — fine for one process; flagged as worth revisiting once running multiple replicas, where concurrent DDL from several processes booting at once becomes a real race-condition risk.
- **`checkpointer` and `checkpointer_pool` both defined in the same `checkpointer_pool.py`** — kept together deliberately since the checkpointer has no independent existence without its pool; avoided over-splitting into more files than the crash course needs.

### Bugs hit and fixes
1. **`AsyncConnectionPool` rejected the app's existing `DATABASE_URL`** — SQLAlchemy's connection URL uses dialect+driver notation (`postgresql+psycopg://...`), which is SQLAlchemy-only syntax, not something raw psycopg/libpq understands. `psycopg_pool` hands its `conninfo` straight to `psycopg.connect()`, which expects a plain libpq-style URL (`postgresql://...`). Fixed by adding a second, separate env var holding the plain psycopg-format URL, used only by `checkpointer_pool.py`, leaving the SQLAlchemy engine's URL untouched.

### Commands used
No new `uv add` — `langgraph-checkpoint-postgres` was already installed in Lesson 1.

Confirming the checkpointer's schema after `.setup()`:
```sql
\dt
-- 10 tables total: the original 6 app tables + checkpoints, checkpoint_blobs,
-- checkpoint_writes, checkpoint_migrations (all blank immediately after .setup())
```

Manual memory + restart test, same `thread_id` throughout:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "thread_id": "thread_lesson4_test", "message": "Are there any sailings on the Ocean?"}'

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "thread_id": "thread_lesson4_test", "message": "What was the fare on that one again?"}'

# Ctrl+C to kill the uvicorn process outright, then restart:
uv run uvicorn app.main:app --reload --loop asyncio

# same thread_id, referencing pre-restart context:
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "thread_id": "thread_lesson4_test", "message": "<follow-up referencing the earlier exchange>"}'
```

Debug endpoint, used throughout for inspection:
```bash
curl http://localhost:8000/debug/threads/thread_lesson4_test/checkpoint
```

### Self-check / confirmation results
- 4.1–4.2 confirmed via pgAdmin: 4 new tables (`checkpoint_blobs`, `checkpoint_migrations`, `checkpoint_writes`, `checkpoints`) created alongside the original 6, all blank immediately after `.setup()` — expected, since `.setup()` only builds schema and doesn't write rows.
- 4.3/4.4/4.6 confirmed together via one live test: two `/chat` calls, same `thread_id` — "Are there any sailings on the Ocean?" then "What was the fare on that one again?" — correctly resolved "that one" using prior turn's context. Confirmed `routes_chat.py` needed zero changes: it already threaded `req.thread_id` into `graph.ainvoke()`'s config from Lesson 3, so the fix was entirely on the `compile()` side.
- 4.5 confirmed: valid `thread_id` returned all prior exchanges via the debug endpoint (14 exchanges at one point during testing); an invalid/never-used `thread_id` returned a blank state rather than an error — matches `aget_state()`'s documented behavior of returning an empty `StateSnapshot` instead of raising.
- 4.7 confirmed: killed the uvicorn process outright (not relying on `--reload`), restarted it, sent a follow-up in the same `thread_id` referencing pre-restart context — correct answer, zero code re-sending prior messages. Proves the app itself is stateless; all memory lives in Postgres, independent of the FastAPI process's own lifetime.
- 4.8 confirmed via direct comparison: `messages` showed 6 rows for a thread the debug endpoint reported `message_count: 8` for. Self-diagnosed correctly as one tool-call round trip (`AIMessage`-with-tool-call + `ToolMessage`) captured by the checkpointer but never persisted to `messages`. Also confirmed: `checkpoint_blobs` content isn't SQL-queryable (binary, not text), and role naming differs between the two systems (`assistant`/`user` in `messages` vs. `ai`/`human`/`tool` as LangChain's own message `.type` values).
- 4.9 explain-back: initial answer correctly identified the data-type/schema mismatch and differing DB-access path (raw pool vs. SQLAlchemy ORM) as reasons for separate tables; supplemented with the deeper reason — separation of concerns (business-level audit record vs. portable, library-owned execution state) and portability (LangGraph's checkpointer schema has to work identically across any app regardless of that app's own tables). Also asked about and correctly resolved the significance of `next_node`: empty tuple `()` means the graph reached a clean stop (as seen in every checkpoint tested so far); a non-empty value would mean the graph was captured mid-execution, the exact mechanism that lets a mid-tool-call crash resume correctly rather than restarting the turn.

---

## Lesson 5 — Manual Summarization From Scratch

*(Flagship lesson of the course, per the roadmap. 5.1–5.7 implementation + Done-When checks completed and verified live; 5.8–5.10 concept explain-backs deliberately skipped — see note below.)*

### Key concepts learned
- **Rolling/updating summary, not from-scratch resummarization** — each time `maybe_summarize()` triggers, it folds the *existing* summary text together with the new raw messages into an updated summary, rather than summarizing the new slice in isolation. Confirmed working across two real trigger cycles in testing: the second summary correctly preserved the first summary's content while appending new detail, rather than losing it.
- **`covered_until_message_id` as an ID-based ordering bookmark** — the same "compare IDs, never content" pattern shows up twice: once as the bookmark that stops re-summarizing already-covered messages, and again in `get_context_for_turn()`'s raw-window query (`Message.id < current_message.id`), which is what prevents the current turn's own message from being pulled into its own context twice.
- **Shared constants prevent silent drift between independently-computed windows** — `KEEP_RAW_COUNT` and `SUMMARIZE_TRIGGER_COUNT` are each defined once in `manual_summarizer.py` and imported everywhere else that needs the same number (`get_context_for_turn()`, `routes_debug.py`'s `/summary` endpoint). Re-typing the same number in two places is exactly how two windows that are supposed to agree quietly stop agreeing.
- **`add_messages` only ever appends, never replaces** — this is the mechanism (not a bug) behind LangGraph's checkpointer, and it's exactly why feeding a fully-assembled context list into a checkpointer-backed graph on a *stable* `thread_id` every turn causes unbounded accumulation: the reducer has no way to know "replace what's there," only "add to it."
- **Checkpoint scope correction** — since Lesson 2, the checkpoint's conceptual job was always "can this one execution survive a crash," never "remember the conversation." Lesson 4 demonstrated it *can* carry conversation memory as a side effect of the reducer; Lesson 5 deliberately walked that back — the checkpointer's `thread_id` is now scoped per-turn (`f"{thread_id}:{uuid.uuid4()}"`), so cross-turn memory lives exclusively in Postgres (`messages`/`summaries`) again, and the checkpointer returns to single-turn execution-state recovery only.
- **`expire_on_commit=False` (set back in Lesson 1) quietly enables Lesson 5's design** — `_save_message()` now returns the persisted `Message` row and the route keeps using `.id` on it *after* `await db.commit()`. In a normal SQLAlchemy session, commit expires every object, and touching an expired attribute in an *async* session raises `MissingGreenlet` (no way to sneak in an implicit reload). `expire_on_commit=False`, chosen for unrelated reasons back in Lesson 1, is exactly what makes this safe now.

### Important decisions & why
- **Deliberately lowered `SUMMARIZE_TRIGGER_COUNT` (10→6) and `KEEP_RAW_COUNT` (6→3)** for faster manual testing — a legitimate, common dev-testing practice, not a mistake. Recorded explicitly here and in the tracker so these numbers aren't later mistaken for production-tuned values.
- **Per-turn checkpoint `thread_id` chosen over `RemoveMessage`-based pruning** — two valid ways existed to stop the checkpointer from re-accumulating history: (A) scope the checkpoint identity per-turn so it never has anything to accumulate, or (B) keep a stable `thread_id` and actively wipe old checkpointed messages with `RemoveMessage(id=REMOVE_ALL_MESSAGES)` each turn. Went with (A) — keeps the checkpointer scoped to its original Lesson 2 purpose, and avoids pre-empting Lesson 6's actual technique. Tradeoff accepted: loses true crash-resume across a full process restart mid-turn — judged a narrow edge case for a synchronous HTTP endpoint, since the caller already got a connection error and would just resend.
- **Dedicated, cheaper/faster summarizer model** (`gpt-4.1-mini`, `temperature=0`), separate from the main chat agent's model — summarization is a background bookkeeping task, not a user-facing answer, so it doesn't need frontier-model reasoning; `temperature=0` for faithful, repeatable compression rather than creative variation.
- **`get_context_for_turn()`'s `current_message` parameter is the already-persisted `Message` row**, not raw text — its `.id` is the raw-window boundary, same ID-based-not-content-based approach as `covered_until_message_id`.

### Bugs hit and fixes
1. **Function name typo** (`may_sumamrize` instead of `maybe_summarize`) — would have broken 5.3's wiring with an `ImportError`. Straightforward fix, but took several rounds to actually land on disk due to a device-bridge caching issue (see #6) unrelated to the typo itself.
2. **Checkpointer accumulation bug** — graph compiled with a Lesson-4 checkpointer + a stable `thread_id` + a manually-assembled multi-message context every turn caused `add_messages` to append the *entire* context on top of prior turns' checkpointed state, every single turn, forever. Silently defeated summarization even though the Postgres-level Done-When checks (5.5/5.6) would have still looked correct. Fixed by scoping the checkpoint `thread_id` per-turn (see decisions above).
3. **Raw/summary window overlap bug** — when `maybe_summarize()` triggers on the *same* turn as the current message, its "keep raw" boundary was computed over a window that included that current message, while `get_context_for_turn()`'s raw window explicitly excludes it. Produced a 1-message overlap: the boundary message got sent to the LLM both compressed (inside the summary) *and* raw, in the same turn. Confirmed live — message 47 appeared verbatim in `raw_window` while also folded into that same turn's updated `summary_text`. Fixed by excluding the current message from `maybe_summarize()`'s window before computing `to_summarize`. Found via 5.7's Done-When test, not a dedicated bug hunt.
4. **Wrong return type hint on `_save_message`** (`-> None` instead of `-> Message`) after it was changed to actually return the persisted row. Not a runtime bug — a real `mypy`-relevant typing bug.
5. **Repeated stray/unused-import pattern** — editor-autocomplete artifacts (`concurrent.futures.thread`, `urllib.response`, `app.db.seed`, `multiprocessing.get_context`, an unused `HumanMessage`). All harmless, but the pattern recurred enough to be worth a `ruff --fix` pass before committing going forward.
6. **Device-bridge content-staging cache bug (tooling, not app code)** — `device_stage_files` repeatedly reported fresh metadata (byte count, mtime) for files Kamran had just edited and saved, but the very next content read through the same staged path served stale, previously-cached content. No fix found within the tooling itself; the reliable workaround was having Kamran attach the file directly to chat instead of relying on the stage-then-read path. This same bug recurred in Lesson 6 (see below) — same workaround applied immediately.

### Commands used
No new `uv add` this lesson — everything needed was already installed by Lesson 1. Testing was done via Postman against `POST /chat` and `GET /debug/threads/{thread_id}/summary`, plus direct Postgres queries against `messages`/`summaries` via a DB client — no new CLI commands this lesson.

### Self-check / confirmation results
- **5.1–5.4 (implementation)**: all confirmed via direct review of the actual files on disk, not Kamran's say-so — this is what caught the `maybe_summarize` typo, the checkpointer accumulation bug, and the `_save_message` return-type bug before they could compound into Lesson 6.
- **5.5 confirmed**: live test against `thread_summary_test` — trigger fired on the 4th exchange (7th raw message overall), `summaries` row created with `covered_until_message_id` matching hand-traced expected math exactly for the lowered thresholds.
- **5.6 confirmed** by the same test: `/debug/threads/{thread_id}/summary` reported `covered_until_message_id` and `raw_message_count_since_summary` both matching the DB exactly.
- **5.7 confirmed**: "what was the very first thing I told you I wanted?" was answered correctly using only summarized content — and inspecting this exact turn's full `raw_window`/`final_context` is what surfaced bug #3 above.
- **5.8–5.10 (concept explain-backs) — explicitly skipped.** Kamran made a deliberate choice to close out the lesson on implementation + Done-When checks alone, confirmed via a direct question rather than inferred from context.

---

## Lesson 6 — Framework-Native Summarization with LangMem

*Two independently-swappable strategies were built this lesson, matching the roadmap's Variant A / Variant B split: `'langmem_function'` (function-style, `summarize_messages()` called directly, Postgres-driven — architecturally mirrors Lesson 5) and `'langmem_node'` (graph-node style, `SummarizationNode`, checkpoint-driven — architecturally mirrors Lesson 4 with automatic trimming bolted on). 6.5 (debug endpoint `summary_mode` reporting) was deliberately skipped; everything else, including all three concept explain-backs, was completed.*

### Key concepts learned
- **`summarize_messages()`'s real trigger is tokens, not message count** — the beginner mistake Lesson 5 deliberately committed to teach the mechanism by hand (`SUMMARIZE_TRIGGER_COUNT`, a message count) is replaced here by a genuine token budget (`max_tokens_before_summary`), because token budget is what a context window actually enforces — messages vary wildly in size (a "yes" vs. a 2000-token tool result), so counting them is a proxy that can silently mislead.
- **`RunningSummary` / `SummarizationResult` — verified against LangMem's actual source, not just its docs.** `last_summarized_message_id` is what does the real work: on every call, `summarize_messages()` scans the incoming message list for a message whose `.id` matches it, and treats everything up to and including that position as already-summarized. `summarized_message_ids` (the full set) is a safety net — it raises `ValueError` if a message already in that set gets handed back in for summarizing again. Confirming this from source (not assuming from the dataclass's docstring alone) is what made 6.2's reconstruction defensible rather than a guess.
- **The `.id` wiring requirement** — LangMem's own cross-call bookkeeping is keyed off each message object's `.id` field. Lesson 5's `get_context_for_turn()` never bothered setting `.id` on the messages it built, because Lesson 5's bookkeeping (`covered_until_message_id`) lived entirely outside the messages, in a separate DB column. Skip setting `.id` here and LangMem has nothing stable to track between calls — every message looks new, every time.
- **`max_tokens` is a required LangMem parameter with no default** — verified directly against the library's source/API reference; the roadmap's own 6.1 item description omitted it. A concrete example of a spec drifting from the real API — worth checking the source, not just trusting a doc summary, especially for a library still under active development.
- **`SummarizationNode` is not a different algorithm** — it's a thin wrapper around the exact same `summarize_messages()` function used in Variant A, packaged to drop into a LangGraph node. It reads messages from `input_messages_key` (default `"messages"`), reads/writes the running summary via a special `context` state key, and writes its trimmed output to a separate `output_messages_key` you name.
- **Why the output goes to a *separate* key, not overwriting `state["messages"]`** — this is the core design of Variant B. `state["messages"]` stays the full, untouched, permanently growing checkpointed history (the same role Postgres's `messages` table plays for Variant A, except this one lives inside the checkpoint). `llm_input_messages` is disposable — recomputed fresh every node run, trusted only for the current call, never for persistence.
- **Graph rewiring: `tools → summarize`, not `tools → agent`** — routing the tool-call loop back through the summarizer (rather than straight back to the agent) means the token budget gets re-checked on *every* loop iteration of a multi-tool-call turn, not just once per HTTP request. A tool result can be large enough on its own to matter mid-turn.
- **The checkpoint-scoping architectural fork** — `'manual'`/`'langmem_function'` need Lesson 5's per-turn UUID-scoped checkpoint (Postgres is the only source of truth; the checkpoint must never be trusted with memory, or it double-accumulates on top of the manually-assembled context). `'langmem_node'` needs the *opposite* — a stable `thread_id`, because the checkpoint itself **is** the source of truth here; there's no separate Postgres-assembled context to collide with. Same root tension (unbounded checkpoint growth), two variants with opposite beliefs about the checkpoint's role, hence two differently-shaped fixes. `RemoveMessage`/`SummarizationMiddleware` (LangChain core's `create_agent`, Lesson 8) is a real fourth option — it actually deletes old messages from state, rather than either variant's approach of leaving them and trimming only what's shown to the model.
- **`RunningSummary` reconstruction across requests is exact, not approximate, given this schema** — rebuilding `summarized_message_ids` as "every `Message.id <= covered_until_message_id`" is only safe because `messages` is append-only and never deleted (a Lesson 1 schema decision). A system that allowed deleting or reordering messages could not take this shortcut — which is exactly why LangMem's own dataclass stores the full set instead of trusting a single boundary value; it can't assume any particular schema is this well-behaved.
- **"Lost in the middle" is a real, separate concern from memory architecture** — investigating a "forgot my name" symptom surfaced that even with *zero* data loss (nothing trimmed, nothing summarized), a model can still fail to use information buried early in a long, undifferentiated raw message list. That's a documented LLM attention behavior, not a code defect — and it's part of the real-world case for aggressive, well-designed context management: shorter, curated context isn't just cheaper, it can measurably improve answer quality too.

### Important decisions & why
- **Two separate `_summarizer_model` instances** (`memory/langmem_summarizer.py` and `agent/graph.py`), not one shared instance — Variant A and Variant B are meant to be independently swappable strategies (6.4's per-thread dispatch), so they shouldn't share model state just because today's config happens to match.
- **`summarize_with_langmem_function()` revised mid-lesson (during 6.4), not at 6.1** — 6.1's original scope, matching the roadmap's literal wording, only asked it to call `summarize_messages()` and persist the returned `RunningSummary`. That silently discarded `result.messages` — the one thing `routes_chat.py` actually needed to send to the graph. Surfaced by actually wiring 6.4, the same way Lesson 5's bugs were surfaced by integration testing rather than a dedicated bug hunt. Revised to load the full thread history itself (matching Lesson 5's self-contained-query convention) and return `result.messages`.
- **Persistence in `summarize_with_langmem_function()` compares `last_summarized_message_id` boundaries** before writing a new `Summary` row, rather than persisting whenever `running_summary is not None` — the latter would write a duplicate row on every single turn, forever, once the first summary exists.
- **Added an optional `summary_mode` field to `ChatRequest`** (Kamran's design idea, refined together) — only honored at thread-creation time inside `_ensure_thread()`, immutable afterward. An existing thread's `summary_mode` mismatching the request's raises `HTTPException(409)` rather than silently ignoring it — matches the fail-fast philosophy already established with `pydantic-settings` in Lesson 1 (surface a testing mistake immediately, don't leave it to be discovered an hour later).
- **No DB-level `CHECK` constraint added on `conversation_threads.summary_mode`** — the new Pydantic `Literal` type validates at the API boundary, but direct SQL edits (used throughout this lesson's manual testing) still bypass that entirely. Flagged as a real, known gap, not fixed this lesson.
- **6.5 (debug endpoint `summary_mode` reporting) deliberately skipped** in favor of closing the lesson via the three concept explain-backs — a real gap it would have fixed was directly visible in 6.6's own evidence (see bugs below), left as a concrete target for later.

### Bugs hit and fixes
1. **`from certifi import contents`** — a stray, unrelated import (SSL certificate bundle library) in `langmem_summarizer.py`, almost certainly an editor-autocomplete artifact. Same category as Lesson 5's bug #5. Harmless as written (a real function, just unused), removed.
2. **`import select` instead of `from sqlalchemy import select`** in `load_running_summary()` (6.2) — not harmless like #1: this shadows the stdlib `select` module, and would have raised a `TypeError` the first time `load_running_summary()` actually ran (calling `select()` on a SQLAlchemy model as if it were a list of file descriptors). Caught via direct file review before marking 6.2 complete; fixed.
3. **`agent_node` still reading `state["messages"]` instead of `state.get("llm_input_messages") or state["messages"]`** (6.3) — `SummarizationNode` would have run and correctly updated state, but the LLM call itself would have kept receiving the full, uncompressed history regardless, silently defeating the entire point of Variant B. This is the same class of bug Lesson 5's notes specifically warned about: DB-level/state-level checks can look fine while the thing that actually matters — what gets sent to the model — is wrong. Caught via direct file review before marking 6.3 complete; fixed.
4. **Stale comment contradicting its own line** — a Lesson-3-era comment ("Deliberately NOT passing a checkpointer here...") was still sitting directly above `graph = builder.compile(checkpointer=checkpointer)`, which very much does pass one. Not functional, but confusing; cleaned up alongside fix #3.
5. **`summarize_with_langmem_function()` discarding `result.messages`** — see decisions above; a scope gap rather than a fresh bug, surfaced by 6.4's integration.
6. **Device-bridge staging cache bug recurred (same as Lesson 5's bug #6)** — `device_stage_files` reported fresh metadata (byte count, mtime) for a just-edited `langmem_summarizer.py`, but content read through the same staged path still served the pre-edit version. Same workaround applied immediately: direct file attachment to chat instead of stage-then-read.
7. **`get_debug_context()` isn't `summary_mode`-aware** — it grabs the newest `Summary` row for a thread regardless of `strategy`, and computes `raw_window` from the hardcoded `KEEP_RAW_COUNT`, independent of what LangMem actually decided to trim. Not currently triggered in practice (threads are mode-locked, one strategy per thread by design), but directly visible as an inconsistency in 6.6's own evidence (`raw_window_count: 3` vs. `final_context`'s 8 messages, for the same debug response, on a `'langmem_function'` thread). Left unfixed — exactly what the skipped 6.5 would have addressed.

### Commands used
No new `uv add` this lesson — `langmem` was already installed in Lesson 1. Testing was done via Postman/curl against `POST /chat` with varying `summary_mode` (first via direct `UPDATE conversation_threads SET summary_mode = ...` SQL, later via the new `summary_mode` request field), direct Postgres queries against `summaries`/`conversation_threads`, and Lesson 4's existing `GET /debug/threads/{thread_id}/checkpoint` — which turned out to be exactly the right tool for inspecting `'langmem_node'` state directly, no new endpoint needed to prove it worked. Temporary `print()` debug statements were added to `agent_node` in `agent/graph.py` to verify `state["messages"]` vs. `llm_input_messages` divergence live; intended to be removed once confirmed.

### Self-check / confirmation results
- **6.1–6.4 (implementation)**: each confirmed via direct review of the actual files on disk, not say-so — this caught the `certifi`/`import select` import issues and the `agent_node` regression before either was marked complete, plus the `summarize_with_langmem_function()` return-value gap surfaced while wiring 6.4.
- **6.5**: deliberately skipped, confirmed via direct question — Kamran chose to close out the lesson via the concept explain-backs instead of building the debug-endpoint extension.
- **6.6 confirmed live, all three `summary_mode`s**: `'manual'` via Lesson 5's own extensive verification (unchanged this lesson); `'langmem_function'` via a real `strategy='langmem'` row in `summaries` on `thread_langmem_func_1` (`covered_until_message_id=65`), with a later turn's `debug.summary` correctly showing that summary folded into the system message and used to answer a follow-up; `'langmem_node'` via temporary debug prints on `thread_langmem_node_1` showing `running_summary` correctly populated, and — across two separate HTTP requests roughly 90 seconds apart — `last_summarized_message_id`/`running_summary.summary` staying byte-for-byte identical when nothing new crossed the (lowered-for-testing) 1000-token threshold. Proves the "don't re-summarize unless something genuinely new happened" logic survives real checkpoint persistence across requests, not just in one process's memory.
- **6.7 confirmed** by the same `langmem_node` debug prints: `state["messages"]` grew 45 → 47 across two real requests (full, untrimmed, checkpointed history, append-only) while `llm_input_messages` stayed small (11 → 13) — direct empirical proof that `SummarizationNode` writes its trimmed view to a separate key and leaves `state["messages"]` genuinely untouched, exactly as designed in 6.3.
- **Investigated, not just patched**: a real "forgot my name" symptom from a ~20-exchange test conversation was traced to two candidate causes rather than assumed to be a bug — either summarization never triggered and the model simply attended poorly to information buried early in a long raw list ("lost in the middle," a known LLM behavior, not a defect), or summarization triggered but the fact was lost to lossy compression. Debug prints confirmed summarization genuinely was triggering correctly after lowering `max_tokens` to 1000; Kamran was satisfied with the mechanical evidence (accumulation + trimming + correct reuse all confirmed sound) without re-testing the exact name-recall question to full certainty.
- **6.8 confirmed after one correction**: initial answer captured the core distinction (manual Postgres-driven wiring vs. automatic checkpoint-driven wiring) but missed the output-destination difference — supplemented with "Variant A trims once, before graph invocation; Variant B trims fresh on every graph step," which is also *why* 6.3 wired `tools → summarize` rather than `tools → agent`. Confirmed understood afterward.
- **6.9 confirmed after a real correction**: initial answer said "No" (the durable-transcript guarantee doesn't hold for both variants), but its own explanation actually demonstrated that it does — `_save_message()` runs identically regardless of `summary_mode`. Corrected to: same guarantee in both, but a different mechanism produces it — a followed rule in Variant A (never writes derived content back to `messages`) vs. a structural impossibility in Variant B (`output_messages_key` names a key that isn't `"messages"`).
- **6.10 confirmed after filling a gap**: correctly guessed `RemoveMessage`/`SummarizationMiddleware`'s core idea from the name alone (actually deletes old messages from state, vs. just hiding them from the model). The "why are the two fixes different if solving the same problem" half wasn't initially addressed — filled in: the two variants disagree about what the checkpoint *is* — disposable plumbing that must never remember (Variant A, hence per-turn scoping) vs. the actual source of truth (Variant B, hence a stable `thread_id`). Same root tension, opposite beliefs, different-shaped fixes. Confirmed understood, all three, together.
