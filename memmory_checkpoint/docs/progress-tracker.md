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

## Lesson 5 — Manual Summarization From Scratch — ✅ COMPLETE (5.8–5.10 deliberately skipped)

*(Flagship lesson of the course, per the roadmap — build this by hand before Lesson 6's LangMem shortcut.)*

*Kamran explicitly chose to skip the three concept explain-backs (5.8–5.10) and close the lesson on implementation + Done-When checks alone — a deliberate call, confirmed via direct question, not an inferred completion. Flagging clearly here since these three specifically test understanding of mechanisms (`covered_until_message_id`'s ordering guarantee, why `maybe_summarize()` must run before `get_context_for_turn()`, checkpoint-vs-manual-context divergence) that Lesson 6 builds directly on top of.*

- [x] 5.1 `memory/manual_summarizer.py` written — `maybe_summarize(db, thread_id)`: if more than 10 messages exist since the last summary's `covered_until_message_id` (or since thread start if no summary exists yet), summarize all but the most recent 6 messages in one LLM call (rolling/updating the previous summary text, not just the new slice in isolation), persist a new row to `summaries` (`thread_id`, `summary_text`, `covered_until_message_id`, `strategy='manual'`)
- [x] 5.2 `get_context_for_turn(db, thread_id, current_message)` written — returns a system message (base prompt + latest summary text if one exists) + the most recent `KEEP_RAW_COUNT` raw messages from `messages` (excluding `current_message` itself, via an `id <` boundary) + the current user message as a `HumanMessage`
- [x] 5.3 `api/routes_chat.py` wired: `maybe_summarize()` called *before* `get_context_for_turn()` on every `POST /chat`, and the graph's input `messages` becomes the assembled context list — not just the single new `HumanMessage` like Lessons 3–4. Also fixed a discovered checkpointer-accumulation bug along the way: `graph.ainvoke()`'s `thread_id` is now scoped per-turn (`f"{thread_id}:{uuid.uuid4()}"`), not the app's stable `thread_id`, since `add_messages` only ever appends — reusing the stable id would have caused the checkpointer to re-accumulate full history on top of the manually-assembled context every turn, silently defeating summarization. Cross-turn memory is now Postgres's job exclusively (`messages`/`summaries`); the checkpointer is scoped back to its Lesson 2 role of single-turn execution-state recovery only. Side effect: `GET /debug/threads/{thread_id}/checkpoint` (Lesson 4) will now always show blank state for the stable `thread_id`, since nothing is ever checkpointed under that exact key anymore — expected, not a bug.
- [x] 5.4 `GET /debug/threads/{thread_id}/summary` added — returns the latest summary row, raw message count since it, and whether summarization would trigger on the next turn (reuses `SUMMARIZE_TRIGGER_COUNT` imported from `manual_summarizer.py`, not a re-typed copy)
- [x] 5.5 Done-When check #1 — verified live against `thread_summary_test`: trigger fired on the 4th exchange (7th raw message, id 46), `summaries` row created with `covered_until_message_id=43` — matches hand-traced expected math for `SUMMARIZE_TRIGGER_COUNT=6`/`KEEP_RAW_COUNT=3` exactly
- [x] 5.6 Done-When check #2: confirmed by the same test — `/debug/threads/{thread_id}/summary` reported `covered_until_message_id: 43` and `raw_message_count_since_summary: 6`, both matching the DB exactly
- [x] 5.7 Done-When check #3: verified live on `thread_summary_test` — "what was the very first thing I told you I wanted?" was answered correctly using only summarized content (message 42, no longer in raw context). Also caught and fixed a real bug along the way: when `maybe_summarize()` triggers on the SAME turn as the current message, its "keep raw" boundary was computed over a window including that current message, while `get_context_for_turn()`'s raw window excludes it (added separately) — causing a 1-message overlap where the boundary message got sent to the LLM both compressed (in the summary) and raw. Confirmed live (message 47 appeared in both). Fixed by excluding the current message from `maybe_summarize()`'s window before computing `to_summarize`, so both functions agree on the same boundary.
- [~] 5.8 SKIPPED (deliberate) — Concept explain-back: why `covered_until_message_id` exists — the ordering guarantee that stops re-summarizing the same messages every turn (wasted LLM calls, drifting summaries) or double-counting
- [~] 5.9 SKIPPED (deliberate) — Concept explain-back: why `maybe_summarize()` must run *before* `get_context_for_turn()`, never after
- [~] 5.10 SKIPPED (deliberate) — Concept explain-back: why the checkpointer's own state (Lesson 4) and this manually-assembled context can silently diverge if you're not deliberate about which one feeds the graph — and the two ways to reconcile them (feed the graph only the trimmed context built here, vs. actively pruning checkpointed `messages` with `RemoveMessage`, which is what Lesson 6's LangMem node does)

See `docs/lesson-notes.md` for the full writeup — added below.

---

## Lesson 6 — Framework-Native Summarization with LangMem — 🔄 IN PROGRESS (6.1–6.4 done)

*Note: the original 5.10 item text (inherited from the uploaded tracker) incorrectly described LangMem's `SummarizationNode` as using `RemoveMessage` to prune checkpointed messages. Corrected before this checklist was written: `SummarizationNode` writes its trimmed view to a separate `output_messages_key`, leaving `state["messages"]` untouched. `RemoveMessage(REMOVE_ALL_MESSAGES)` is actually the mechanism behind LangChain's separate `SummarizationMiddleware` (built into core `langchain` 1.0's `create_agent`) — a fourth option, deferred to Lesson 8, not part of Lesson 6.*

- [x] 6.1 `memory/langmem_summarizer.py` written — `summarize_with_langmem_function(db, thread_id, message_rows, running_summary)`: Variant A, function-style. Converts DB `Message` rows to LangChain messages with `id=str(row.id)` set (required so LangMem's own `RunningSummary.summarized_message_ids` tracking has something stable to key on — `get_context_for_turn()` never set `.id`, since Lesson 5's bookkeeping lived outside the messages entirely). Calls `langmem.short_term.summarize_messages(messages, running_summary=..., model=summarizer_model, max_tokens=3000, max_tokens_before_summary=3000, max_summary_tokens=512, token_counter=count_tokens_approximately)`, persists the returned `running_summary` to `summaries` with `strategy='langmem'` (`covered_until_message_id=int(result.running_summary.last_summarized_message_id)`, safe because we generated that string ourselves). Note: `max_tokens` is actually a *required* parameter in the real LangMem API — the original roadmap wording omitted it, caught by checking LangMem's source/API reference directly rather than trusting the doc summary. Also hit and fixed the recurring device-bridge staging cache bug from Lesson 5 (bug #6) — `device_stage_files` reported fresh metadata but served stale content on read; resolved via direct file attachment, same workaround as before.
- [x] 6.2 `load_running_summary(db, thread_id)` written in `memory/langmem_summarizer.py` — rebuilds LangMem's `RunningSummary` from the `summaries` table. Filters on `strategy == "langmem"` (the table is shared with Lesson 5's `'manual'` rows). Reconstructs `summarized_message_ids` as every `Message.id <= covered_until_message_id` for the thread — an exact reconstruction, not an approximation, because `messages` is append-only/never-deleted (Lesson 1's schema decision); confirmed via LangMem's actual source that `last_summarized_message_id` drives the real split-point lookup and `summarized_message_ids` is a safety-net duplicate-check, so this reconstruction is faithful to how the library actually uses both fields. Bug caught before marking complete: `import select` (stdlib) instead of `from sqlalchemy import select` — would have raised `TypeError` the first time `load_running_summary()` ran; fixed.
- [x] 6.3 `agent/graph.py` extended — Variant B: `langmem.short_term.SummarizationNode` added as a node before the agent node (`output_messages_key="llm_input_messages"`, `max_tokens=3000`, `max_summary_tokens=512`). Graph rewired `START → summarize → agent`, `tools → summarize` (loops back through the summarizer on every tool round trip, not straight to `agent` — keeps a multi-tool-call turn's token budget in check too, not just the first pass). `AgentState` grew `llm_input_messages` (trimmed view) and `context: dict[str, RunningSummary]` (LangMem's own bookkeeping slot). Bug caught before marking complete: `agent_node` was still reading `state["messages"]` (the full untouched history) instead of `state.get("llm_input_messages") or state["messages"]` — summarization would have run and updated state correctly, but the LLM call itself would have kept getting the uncompressed history regardless, silently defeating the entire point of Variant B. Fixed. Flagged (not yet resolved — that's 6.4's job): this graph now needs a STABLE checkpoint `thread_id` to do anything meaningful, which conflicts with Lesson 5's per-turn UUID scoping used by `'manual'`/`'langmem_function'` modes.
- [x] 6.4 `api/routes_chat.py` wired — `POST /chat` dispatches on `conversation_threads.summary_mode` (`'manual' | 'langmem_function' | 'langmem_node'`) to the matching implementation, same endpoint, three strategies. `'manual'`/`'langmem_function'` share an invocation shape (Postgres-assembled context, per-turn UUID-scoped checkpoint — same reasoning as Lesson 5); `'langmem_node'` uses a stable `thread_id` + only the new `HumanMessage`, letting the checkpoint itself carry cross-turn memory. Revised `summarize_with_langmem_function()` along the way (gap surfaced by actually wiring it in, not a fresh bug): now loads full thread history itself (matching Lesson 5's self-contained-query convention) and returns the trimmed `result.messages` instead of just `RunningSummary` — 6.1's original version discarded the one thing the caller actually needed. Persistence now compares `last_summarized_message_id` boundaries so a `summaries` row is only written when something genuinely new was summarized, not on every turn.
- [ ] 6.5 `GET /debug/threads/{thread_id}/summary` extended (not replaced) — now also reports which `summary_mode` is active.
- [ ] 6.6 Done-When check #1: switch one thread across all three `summary_mode` values, confirm correct summarization behavior in each.
- [ ] 6.7 Done-When check #2: prove `state["messages"]` stays genuinely untouched in `langmem_node` mode — direct empirical test of the correction above.
- [ ] 6.8 Concept explain-back: `summarize_messages` (function-style) vs. `SummarizationNode` (graph-node style) — what's mechanically different, not just "one's a function."
- [ ] 6.9 Concept explain-back: why neither LangMem variant replaces `messages` as the durable transcript — same principle as your manual version, different implementation.
- [ ] 6.10 Concept explain-back: the corrected version of the checkpoint-divergence question — separate output key vs. per-turn checkpoint scoping, and where `RemoveMessage`/`SummarizationMiddleware` actually fits (a fourth option, covered properly in Lesson 8, not Lesson 6).

---

## Lessons 7–8 — not yet detailed

Will be broken into per-file checklists (same granularity as Lesson 1, 3, 4, 5, and 6) as we actually reach each one. Deliberately not pre-planning these in detail now — the file list may shift slightly as earlier lessons surface things (the way Lesson 1 grew a 1.8b we didn't originally plan for), and a stale forward-looking checklist is worse than none.
