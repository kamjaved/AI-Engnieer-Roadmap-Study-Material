"""Seed script — populates users & sailings so Lesson 3's search_sailings
tool has something real to query.

Run it directly with:
    uv run python -m app.db.seed

Why a separate script instead of running this inside main.py's startup?
Seeding is a one-time (or safely-repeatable) action, not something that
should re-run every time you restart the FastAPI server — same reason you
don't run `npm install` on every page load in a Node app. Setup and runtime
are different concerns, and mixing them is a common beginner habit worth
unlearning early.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.db.models import Sailing, User
from app.db.session import async_session_factory


async def seed() -> None:
    # async_session_factory() hands us a Session — think of it as a fresh
    # scratchpad for this one script run. Nothing below touches Postgres
    # until we explicitly call commit().
    async with async_session_factory() as session:
        # --- Idempotency check ---------------------------------------------
        # Good habit to build now: seed scripts should be safe to run twice.
        # Without this check, running the script again would insert Kamran
        # and Sarah a *second* time (new ids, duplicate names) instead of
        # leaving things alone.
        #
        # select(User) is SQLAlchemy's query builder — the Python-object
        # equivalent of writing "SELECT * FROM users" by hand, except your
        # IDE and mypy can catch a typo'd column name before you ever run it.
        existing_users = await session.execute(select(User))
        if existing_users.scalars().first() is not None:
            print("Seed data already exists — skipping (seeding is meant to run once).")
            return

        # --- Create the two users ------------------------------------------
        # Right now `kamran` and `sarah` are just plain Python objects sitting
        # in memory. This is the core ORM mental model: work with normal
        # Python objects, let SQLAlchemy handle the SQL translation later.
        kamran = User(name="Kamran")
        sarah = User(name="Sarah")

        # session.add_all(...) stages both objects — still zero SQL sent yet.
        session.add_all([kamran, sarah])

        # flush() sends the pending INSERTs to Postgres *within the current
        # transaction* — mainly so the database can hand us back the
        # auto-generated `id` values — without fully committing yet.
        # Think "show your work so far," not "make it permanent" (that's
        # commit's job, below).
        await session.flush()

        # --- Five sailings across 2+ ships, 2+ months in 2026 --------------
        sailings = [
            Sailing(
                ship_name="Ocean Explorer",
                departure_port="Miami",
                arrival_port="Nassau",
                departure_date=date(2026, 3, 14),
                adult_fare=Decimal("499.00"),
                currency="USD",
            ),
            Sailing(
                ship_name="Ocean Explorer",
                departure_port="Miami",
                arrival_port="Cozumel",
                departure_date=date(2026, 4, 2),
                adult_fare=Decimal("649.00"),
                currency="USD",
            ),
            Sailing(
                ship_name="Northern Star",
                departure_port="Southampton",
                arrival_port="Bergen",
                departure_date=date(2026, 6, 10),
                adult_fare=Decimal("899.00"),
                currency="GBP",
            ),
            Sailing(
                ship_name="Northern Star",
                departure_port="Southampton",
                arrival_port="Reykjavik",
                departure_date=date(2026, 7, 21),
                adult_fare=Decimal("1099.00"),
                currency="GBP",
            ),
            Sailing(
                ship_name="Pacific Voyager",
                departure_port="Singapore",
                arrival_port="Phuket",
                departure_date=date(2026, 9, 5),
                adult_fare=Decimal("399.00"),
                currency="USD",
            ),
        ]
        session.add_all(sailings)

        # commit() is the actual "save button" — everything staged since the
        # session opened (2 users + 5 sailings = 7 rows) is written to
        # Postgres atomically: either all 7 land, or none do if something
        # fails partway.
        await session.commit()

        print(f"Seeded {len(sailings) + 2} rows: 2 users, {len(sailings)} sailings.")


if __name__ == "__main__":
    # psycopg3's async mode requires a SelectorEventLoop; Windows defaults
    # asyncio.run() to ProactorEventLoop, which raises InterfaceError on connect.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # config.py and session.py only *define* async functions — something has
    # to actually start an event loop to run one. asyncio.run() is that
    # entry point, same role as `if __name__ == "__main__": app.run()` in Flask.
    asyncio.run(seed())
