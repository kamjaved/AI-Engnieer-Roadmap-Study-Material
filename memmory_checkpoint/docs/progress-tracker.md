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

## Lesson 4 — LangGraph Postgres Checkpointing & Thread Recovery — ✅ COMPLETE

- [x] 4.1 Pooled `AsyncConnectionPool` (psycopg3, from `psycopg_pool`) created at FastAPI startup, opened at startup and closed/disposed at shutdown — hit and fixed a SQLAlchemy-URL-vs-psycopg-URL mismatch along the way (see `docs/lesson-notes.md`)
- [x] 4.2 `AsyncPostgresSaver(pool)` instantiated, `.setup()` called once at startup (idempotent — creates the checkpointer's own tables) — confirmed via pgAdmin: 4 new tables created, all blank immediately after `.setup()`
- [x] 4.3 `agent/graph.py` recompiled with `checkpointer=checkpointer`
- [x] 4.4 `api/routes_chat.py` confirmed unchanged in behavior — already threaded `req.thread_id` into the invoke config from Lesson 3, so it needed zero changes to become correct
- [x] 4.5 `GET /debug/threads/{thread_id}/checkpoint` added — calls `graph.aget_state(config)`, returns the raw state — confirmed correct message counts for a valid thread, blank state for an invalid one
- [x] 4.6 Done-When check #1: chat, then a follow-up depending on turn 1, in the same `thread_id` — correct answer this time (memory works)
- [x] 4.7 Done-When check #2: stopped the FastAPI process outright, restarted it, continued the same `thread_id` — agent still had full context, zero code re-sending prior messages
- [x] 4.8 Compared `GET /debug/threads/{thread_id}/checkpoint` against the raw `messages` table for the same thread — found and explained a real count mismatch (6 rows vs. `message_count: 8`), correctly traced to one tool-call round trip the checkpointer captures but the route never persists to `messages`
- [x] 4.9 Concept explain-back: why the checkpointer needing its own separate tables (not `messages`) is deliberate design, not duplication — correctly identified the data-type/access-path differences, supplemented with the deeper separation-of-concerns and portability reasoning; also worked through the significance of `next_node`

See `docs/lesson-notes.md` for the full writeup of concepts, decisions, and bugs from this lesson.

---

## Lesson 5 — Manual Summarization From Scratch — 🔄 IN PROGRESS

*(Flagship lesson of the course, per the roadmap — build this by hand before Lesson 6's LangMem shortcut.)*

- [ ] 5.1 `memory/manual_summarizer.py` written — `maybe_summarize(db, thread_id)`: if more than 10 messages exist since the last summary's `covered_until_message_id` (or since thread start if no summary exists yet), summarize all but the most recent 6 messages in one LLM call, persist a new row to `summaries` (`thread_id`, `summary_text`, `covered_until_message_id`, `strategy='manual'`)
- [ ] 5.2 `get_context_for_turn(db, thread_id, current_message)` written — returns a system message (base prompt + latest summary text if one exists) + the most recent 6 raw messages from `messages` + the current user message as a `HumanMessage`
- [ ] 5.3 `api/routes_chat.py` wired: `maybe_summarize()` called *before* `get_context_for_turn()` on every `POST /chat`, and the graph's input `messages` becomes the assembled context list — not just the single new `HumanMessage` like Lessons 3–4
- [ ] 5.4 `GET /debug/threads/{thread_id}/summary` added — returns the latest summary row, raw message count since it, and whether summarization would trigger on the next turn
- [ ] 5.5 Done-When check #1: a 12+ message conversation confirms a `summaries` row was created after message 11
- [ ] 5.6 Done-When check #2: the debug endpoint shows the correct `covered_until_message_id`
- [ ] 5.7 Done-When check #3: asking about something from early in the conversation gets answered correctly using the injected summary, not the now-excluded raw early messages
- [ ] 5.8 Concept explain-back: why `covered_until_message_id` exists — the ordering guarantee that stops re-summarizing the same messages every turn (wasted LLM calls, drifting summaries) or double-counting
- [ ] 5.9 Concept explain-back: why `maybe_summarize()` must run *before* `get_context_for_turn()`, never after
- [ ] 5.10 Concept explain-back: why the checkpointer's own state (Lesson 4) and this manually-assembled context can silently diverge if you're not deliberate about which one feeds the graph — and the two ways to reconcile them (feed the graph only the trimmed context built here, vs. actively pruning checkpointed `messages` with `RemoveMessage`, which is what Lesson 6's LangMem node does)

See `docs/lesson-notes.md` for the full writeup once this lesson is confirmed done.

---

## Lessons 6–8 — not yet detailed

Will be broken into per-file checklists (same granularity as Lesson 1, 3, 4, and 5) as we actually reach each one. Deliberately not pre-planning these in detail now — the file list may shift slightly as earlier lessons surface things (the way Lesson 1 grew a 1.8b we didn't originally plan for), and a stale forward-looking checklist is worse than none.
