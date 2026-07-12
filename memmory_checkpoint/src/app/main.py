"""FastAPI application entrypoint.

Run with:
    uv run uvicorn app.main:app --reload --loop asyncio
"""

from __future__ import annotations

import asyncio
import sys

# This has to run before anything else touches asyncio — same Windows +
# psycopg3 issue you already fixed in seed.py, just showing up in a new
# place. Belt-and-suspenders: we set the policy here at import time AND
# pass --loop asyncio on the command line above. Recent uvicorn versions
# have a known bug where setting this policy alone (without the CLI flag)
# doesn't reliably stick once uvicorn starts its own server loop — so we
# do both, and between the two, one of them will actually take effect.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes_chat import router as chat_router
from app.api.routes_debug import router as debug_router
from app.db.base import Base
from app.db.checkpointer_pool import checkpointer, checkpointer_pool

# These six imports look "unused" to a linter — you never reference User or
# Sailing by name anywhere in this file. But importing them is what makes
# SQLAlchemy aware they exist at all: each model class registers itself onto
# Base.metadata the moment Python imports its module. Skip these imports and
# create_all() below would create zero tables, silently. The `noqa` comment
# tells ruff "yes, I know these look unused, leave it alone."
from app.db.models import (  # noqa: F401
    ConversationThread,
    LongTermMemory,
    Message,
    Sailing,
    Summary,
    User,
)
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Code before `yield` runs once at server startup; code after `yield`
    runs once at shutdown. This replaced FastAPI's older `@app.on_event("startup")`
    decorator — the old style let you register multiple separate startup/shutdown
    handlers with no guaranteed relationship between them, which got messy fast.
    One function, one clear "setup ... yield ... teardown" shape, is easier to
    reason about and is what FastAPI itself now recommends.
    """
    # Startup: create any tables that don't exist yet. create_all() checks
    # first and only creates what's missing, so this is safe to run on every
    # single server restart — it won't touch tables that already exist or
    # touch any data in them.
    #
    # This is a Lesson-1-only shortcut, and the roadmap is explicit about
    # that: real schema changes over time need Alembic migrations (full
    # roadmap, not this crash course) — create_all() only knows "does this
    # table exist," it has no concept of "alter this existing table."
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Open checkpointer pool: establishes min_size connections now so they're
    # ready to use. Without this, the first request hits the pool startup cost.
    await checkpointer_pool.open()

    # Set up checkpointer schema: idempotent, creates tables on first run,
    # near-instant no-op on every subsequent startup.
    await checkpointer.setup()

    yield  # <-- the app serves requests while execution is paused here

    # Shutdown: close checkpointer pool gracefully first
    await checkpointer_pool.close()

    # Then close every pooled connection cleanly instead of letting the
    # process exit and leave connections dangling on the Postgres side.
    await engine.dispose()


app = FastAPI(title="Cruise Crash Course", lifespan=lifespan)

app.include_router(chat_router)
app.include_router(debug_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
