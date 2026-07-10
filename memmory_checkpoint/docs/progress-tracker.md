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

## Lesson 2 — The Memory Mental Model — NOT STARTED

- [ ] 2.1 Read and understand the 5 core terms: Context, Conversation history, Short-term memory, Long-term memory, Checkpoint
- [ ] 2.2 Self-check: correctly identify which table(s) answer each of the 3 sample questions (full history / does-the-assistant-know-my-preference / resume-after-crash)
- [ ] 2.3 Can explain, unprompted and in your own words, the core relationship sentence ("`messages` is truth, `summaries` is compressed truth for one thread, `long_term_memories` is durable truth across threads, checkpoint is plumbing")

This lesson is conceptual — no code, no new checklist items beyond these three.

---

## Lessons 3–8 — not yet detailed

Will be broken into per-file checklists (same granularity as Lesson 1) as we actually reach each one. Deliberately not pre-planning these in detail now — the file list may shift slightly as earlier lessons surface things (the way Lesson 1 grew a 1.8b we didn't originally plan for), and a stale forward-looking checklist is worse than none.
