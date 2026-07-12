from __future__ import annotations

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from app.core.config import get_settings

settings = get_settings()

# This pool is ONLY for the LangGraph checkpointer — never mix it with
# SQLAlchemy sessions. Two separate fleets, same warehouse (same DB).
checkpointer_pool = AsyncConnectionPool(
    conninfo=settings.psycopg_database_url,  # raw psycopg URL, not SQLAlchemy's postgresql+psycopg://
    max_size=20,  # ceiling: how many live connections this pool may hold
    min_size=5,  # floor: connections kept warm even when idle,
    # so the first request after a quiet period isn't
    # stuck paying connection-setup cost
    kwargs={
        # AsyncPostgresSaver reads rows with dict-style access (row["column"]),
        # not tuple-style (row[0]) — dict_row makes every connection return
        # rows shaped that way, at the driver level.
        "row_factory": dict_row,
        # autocommit=True is required by AsyncPostgresSaver's .setup() call
        # (Lesson 4.2) so schema-creation statements commit immediately,
        # not sit inside an open transaction waiting for a commit that
        # never comes from checkpointer-internal code.
        "autocommit": True,
    },
    open=False,  # do NOT let the pool open connections at construction time —
    # we open it explicitly in FastAPI's lifespan, so we control
    # exactly when connections start getting made, and can catch
    # a bad DATABASE_URL as a clean startup failure.
)

checkpointer = AsyncPostgresSaver(checkpointer_pool)
