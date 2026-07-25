from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from langchain.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import LongTermMemory
from app.db.session import async_session_factory

# The 5 fixed categories from the roadmap. 'ignore' is a real category,
# not a fallback/error case — most exchanges SHOULD classify as ignore.
# That's the whole point: this is a judgment filter, not a save-everything pipe.
MemoryCategory = Literal[
    "travel_preference",
    "communication_preference",
    "profile",
    "currency_preference",
    "ignore",
]
# Hardcoded for now, matching the roadmap's 7.1 scope exactly.
# Flagging honestly: a fixed confidence for every classification is a
# beginner-grade shortcut. Real production systems calibrate this per
# call (e.g. log-probs, or a second "how sure are you" pass) — deferred
# here on purpose, not missed.
DEFAULT_CONFIDENCE = Decimal("0.80")

_CLASSIFIER_SYSTEM_PROMPT = (
    "You classify one exchange from a cruise-booking chat assistant. Decide "
    "if it contains a durable fact about the USER that would still be true "
    "and useful in a completely different conversation, weeks from now.\n\n"
    "Categories:\n"
    "- travel_preference: cabin type, ship, itinerary style, etc.\n"
    "- communication_preference: how the user wants to be talked to "
    "(tone, brevity, language).\n"
    "- profile: stable facts about the user (name, home port, loyalty tier).\n"
    "- currency_preference: which currency they want prices shown in.\n"
    "- ignore: anything else — small talk, one-off questions, facts that "
    "only matter for THIS conversation.\n\n"
    "When category is not 'ignore', write `content` as a short, third-person "
    "statement stating the fact plainly, e.g. 'User prefers prices in INR.' "
    "When category is 'ignore', leave `content` as null."
)


class MemoryClassification(BaseModel):
    """What the classifier LLM call must return — validated, not parsed by hand."""

    category: MemoryCategory
    content: str | None = Field(
        default=None,
        description="Third-person durable fact, or null when category is 'ignore'.",
    )


@dataclass
class Exchange:
    """One user turn + the assistant's reply to it — the unit classify_and_store looks at.

    A dataclass, not two separate string params, because this "exchange" is
    a single conceptual thing the roadmap's own signature names as one arg —
    and because the classifier genuinely needs BOTH sides: the assistant's
    reply can be what confirms a preference ("Got it, I'll show INR from now
    on"), not just the user's raw message.
    """

    user_message: str
    assistant_message: str


_classifier_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0).with_structured_output(
    MemoryClassification
)


async def classify_and_store(
    db: AsyncSession, user_id: int, thread_id: str, exchange: Exchange
) -> LongTermMemory | None:

    result: MemoryClassification = await _classifier_model.ainvoke(
        [
            SystemMessage(content=_CLASSIFIER_SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"User: {exchange.user_message}\n"
                    # Keeping both assistant and user message
                    f"Assistant: {exchange.assistant_message}"
                )
            ),
        ]
    )

    # Guard both conditions — a model could theoretically return a non-ignore
    # category with content=None (schema allows it even if the prompt says
    # not to). Either way, nothing worth storing.
    if result.category == "ignore" or not result.content:
        return None

    memory = LongTermMemory(
        user_id=user_id,
        memory_type=result.category,  # matches the actual column name in models.py
        content=result.content,
        confidence=DEFAULT_CONFIDENCE,
        source_thread_id=thread_id,
        status="active",
    )

    db.add(memory)
    await db.commit()
    return memory


async def get_active_memories(db: AsyncSession, user_id: int) -> list[str]:
    """
    Every active long-term fact we know about this user, across ALL threads.

    No ORDER BY on confidence or recency here on purpose — this crash
    course loads everything active, unranked (see the tracker's own note
    on deferring pgvector/relevance-based retrieval to a later stage).
    At real volume this naive "load all" approach stops scaling — that's
    exactly the gap embedding-based retrieval exists to fill later.
    """
    rows = (
        await db.scalars(
            select(LongTermMemory.content).where(
                LongTermMemory.user_id == user_id,
                LongTermMemory.status == "active",
            )
        )
    ).all()
    return list(rows)


async def classify_and_store_background(user_id: int, thread_id: str, exchange: Exchange) -> None:
    """
    Entry point for FastAPI's BackgroundTasks.

    Opens its OWN session instead of reusing the request's — by the time a
    background task actually runs, FastAPI has already torn down the
    request's `Depends(get_db_session)` dependency (its `finally: session.close()`
    runs BEFORE background tasks execute, not after). Passing that session in
    here would touch an already-closed session. Verified against FastAPI's
    own docs on dependencies-with-yield, not assumed.
    """
    async with async_session_factory() as db:
        await classify_and_store(db, user_id, thread_id, exchange)


def format_memories_block(active_memories: list[str]) -> str:
    """
    Render active long-term memories as a system-prompt fragment.
    Shared by all three summary_mode paths.

    Returns "" (not a header with zero bullets) when there's nothing to
    say, so every caller can blindly concatenate: BASE_PROMPT + this,
    no `if active_memories:` check needed at every call site.
    """
    if not active_memories:
        return ""
    facts = "\n".join(f"- {m}" for m in active_memories)
    return f"\n\nRelevant facts about this user:\n{facts}"
