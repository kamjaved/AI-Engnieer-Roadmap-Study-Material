from __future__ import annotations

from langchain_core.tools import tool
from sqlalchemy import select

from app.db.models import Sailing
from app.db.session import async_session_factory

# @tool turns a plain function into something an LLM can "call". Under the
# hood this is just a JSON schema generated from your type hints + docstring
# — the model never executes Python; it returns a message saying "call
# search_sailings with these args", and ToolNode (Lesson graph.py) is what
# actually runs this function and feeds the result back in.
#
# The docstring below is NOT documentation for humans — it's the only thing
# the LLM sees to decide (a) whether to call this tool at all, and (b) what
# to pass as arguments. Vague docstrings = the model guessing wrong.


@tool
async def search_sailings(
    ship_name: str | None = None,
    month: str | None = None,
) -> str:
    """Search available cruise sailings, optionally filtered by ship name
    and/or departure month (e.g. "2026-08"). Returns a short list of
    matching sailings with ship name, ports, date, and fare. Use this
    whenever the user asks about cruises, ships, prices, or dates.
    """
    # Tools own their own DB session — they are NOT FastAPI routes, so
    # there's no Depends(get_db_session) to inject one for you. Opening
    # and closing the session inside the tool keeps this function usable
    # from the API, from a test, or from a CLI script identically.
    async with async_session_factory() as db:
        query = select(Sailing)
        if ship_name:
            query = query.where(Sailing.ship_name.ilike(f"%{ship_name}%"))
        if month:
            query = query.where(func_month_matches(Sailing.departure_date, month))

        result = await db.execute(query.limit(5))
        sailings = result.scalars().all()

    if not sailings:
        return "No Matching sailing Found."
    # Returned as a plain string — the model reads this as a ToolMessage
    # and decides what to say next. Keep it short; every token here is
    # tokens the model has to re-read on its next turn.
    lines = [
        f"{s.ship_name}: {s.departure_port} -> {s.arrival_port}, "
        f"departs {s.departure_date}, {s.adult_fare} {s.currency}"
        for s in sailings
    ]
    return "\n".join(lines)


def func_month_matches(column, month: str):
    """Small helper so the query above stays readable. Matches on the
    'YYYY-MM' prefix of an ISO date string — good enough for a 5-row
    seed table not ideal for production because casting a date to a string can
    prevent the database from using indexes efficiently
    """
    from sqlalchemy import String, cast

    return cast(column, String).like(f"{month}%")
