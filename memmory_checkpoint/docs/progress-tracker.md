# Progress Tracker — LangGraph Memory Crash Course

> Source of truth for what's actually done vs. pending. A box is checked **only** after Kamran has explicitly confirmed it — never inferred from context. If you're a fresh Claude session picking this up: trust this file over anything implied elsewhere, and don't mark anything complete without asking first.

---

## Lesson 1 — Prerequisites & Project Setup — ✅ COMPLETE

- [x] 1.1 Prerequisites confirmed (Python 3.13, `uv`, Postgres `langgraph_memmory` reachable on localhost:5432)
- [x] 1.2 Project initialized (`uv init`), folder skeleton created (`src/app/{core,db,agent,memory,api}`)
- [x] 1.3 Dependencies installed via `uv add` (`psycopg[binary,pool]` fix included from the start)
- [x] 1.4 `.env` complete (`DATABASE_URL`, `OPENAI_API_KEY`, `APP_ENV`)
- [x] 1.5 `pyproject.toml` cleaned up (removed stray `openai_sdk` workspace member; `mypy` `python_version` aligned to `"3.13"`)
- [x] 1.6 `.gitignore` created (before any `git init`)
- [x] 1.7 `core/config.py` written (pydantic-settings `BaseSettings`)
- [x] 1.8 `db/base.py` + `db/session.py` written
- [x] 1.8b Package install fixed — explicit `[build-system]` / hatchling `packages = ["src/app"]` added so `app.*` imports resolve consistently regardless of invocation method
- [x] 1.9 `db/models.py` written (6 tables: users, sailings, conversation_threads, messages, summaries, long_term_memories)
- [x] 1.10 `db/seed.py` written and run (plus bonus `db/create_tables.py` stopgap script)
- [x] 1.11 `main.py` written — `GET /health` returns 200 via `uv run uvicorn app.main:app --reload --loop asyncio`; all 6 tables + seed rows confirmed in `langgraph_memmory`

See `docs/lesson-notes.md` for the full writeup of concepts, decisions, and bugs from this lesson.

---

## Lesson 2 — The Memory Mental Model — ✅ COMPLETE

- [x] 2.1 Read and understand the 5 core terms: Context, Conversation history, Short-term memory, Long-term memory, Checkpoint
- [x] 2.2 Self-check: correctly identify which table(s) answer each of the 3 sample questions (full history / does-the-assistant-know-my-preference / resume-after-crash) — got Q1 and Q2 right immediately; Q3 needed one correction (see `docs/lesson-notes.md`)
- [x] 2.3 Can explain, unprompted and in your own words, the core relationship sentence ("`messages` is truth, `summaries` is compressed truth for one thread, `long_term_memories` is durable truth across threads, checkpoint is plumbing")

See `docs/lesson-notes.md` for the full writeup, including the one misconception worth remembering (conversation_threads vs. the checkpointer's own tables).

---

## Lesson 3 — Minimal Tool-Calling Agent + Raw Transcript Persistence — ✅ COMPLETE

- [x] 3.1 `agent/tools.py` written — one `@tool`-decorated `search_sailings(ship_name: str | None, month: str | None)` querying `sailings` via async SQLAlchemy session
- [x] 3.2 `agent/graph.py` written — `StateGraph` with `messages: Annotated[list[AnyMessage], add_messages]`, an `agent` node (ChatOpenAI bound to the tool), a `ToolNode`, conditional edge via `tools_condition` — compiled **without** a checkpointer
- [x] 3.3 `api/routes_chat.py` written — `POST /chat({user_id, thread_id, message})`: saves the user message to `messages` before invoking the graph, saves the assistant's reply to `messages` after
- [x] 3.4 Done-When check #1: two `POST /chat` calls in the same `thread_id` produce two rows each in `messages` — confirmed via live Postgres data view (see `docs/lesson-notes.md`)
- [x] 3.5 Done-When check #2: a follow-up question depending on the first turn demonstrates the agent has no memory of it — confirmed: "What was the fare on that one again?" got "Could you please specify which cruise or sailing you're referring to?"
- [x] 3.6 Concept explain-back: why `messages` having full history in Postgres didn't stop the agent from "forgetting" — conversation history and checkpointing are two independent persistence paths, and neither was bridging turn 1 into turn 2's input (this is expected behavior here, not a bug — closed in Lesson 4)

See `docs/lesson-notes.md` for the full writeup, including the checkpoint-granularity follow-up discussion (Lesson 4 preview).

---

## Lesson 4 — LangGraph Postgres Checkpointing & Thread Recovery — 🔄 IN PROGRESS

- [ ] 4.1 Pooled `AsyncConnectionPool` (psycopg3, from `psycopg_pool`) created at FastAPI startup, opened at startup and closed/disposed at shutdown
- [ ] 4.2 `AsyncPostgresSaver(pool)` instantiated, `.setup()` called once at startup (idempotent — creates the checkpointer's own tables)
- [ ] 4.3 `agent/graph.py` recompiled with `checkpointer=checkpointer`
- [ ] 4.4 `api/routes_chat.py` confirmed unchanged in behavior — still sends only the new `HumanMessage`, but this now becomes *correct* because the checkpointer reloads prior state before the reducer runs
- [ ] 4.5 `GET /debug/threads/{thread_id}/checkpoint` added — calls `graph.aget_state(config)`, returns the raw state
- [ ] 4.6 Done-When check #1: chat, then a follow-up depending on turn 1, in the same `thread_id` — correct answer this time (memory works)
- [ ] 4.7 Done-When check #2: stop the FastAPI process, restart it, continue the same `thread_id` — agent still has full context, zero code re-sending prior messages
- [ ] 4.8 Compare `GET /debug/threads/{thread_id}/checkpoint` against the raw `messages` table for the same thread — two structurally different representations of "the conversation so far"
- [ ] 4.9 Concept explain-back: why the checkpointer needing its own separate tables (not `messages`) is a deliberate design, not duplication — one is durable execution state (resumable mid-tool-call), the other is the audit-friendly transcript

See `docs/lesson-notes.md` for the full writeup once this lesson is confirmed done.

---

## Lessons 5–8 — not yet detailed

Will be broken into per-file checklists (same granularity as Lesson 1, 3, and 4) as we actually reach each one. Deliberately not pre-planning these in detail now — the file list may shift slightly as earlier lessons surface things (the way Lesson 1 grew a 1.8b we didn't originally plan for), and a stale forward-looking checklist is worse than none.
