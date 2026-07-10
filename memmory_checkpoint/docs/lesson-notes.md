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
*(to be filled in once the lesson is complete)*
