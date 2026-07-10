"""One-off table creation script — run once before seeding, until Alembic is wired up.

Run it directly with:
    uv run python -m app.db.create_tables
"""

from __future__ import annotations

import asyncio
import sys

from app.db.base import Base
from app.db.models import (  # noqa: F401 — import registers models on Base.metadata
    ConversationThread,
    LongTermMemory,
    Message,
    Sailing,
    Summary,
    User,
)
from app.db.session import engine


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(create_tables())
