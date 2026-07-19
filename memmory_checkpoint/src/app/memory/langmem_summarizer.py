"""
Variant A: LangMem's function-style summarizer (langmem.short_term.summarize_messages).

Same job as manual_summarizer.py's maybe_summarize(), but the trigger
condition and the "fold old summary + new messages" logic are LangMem's,
not ours. We just call it and persist whatever it hands back.
"""

from __future__ import annotations

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain_openai import ChatOpenAI
from langmem.short_term import RunningSummary, summarize_messages
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Message, Summary

# Token-budget constants, not message-count ones — this is the main
# mechanical difference from manual_summarizer.py's SUMMARIZE_TRIGGER_COUNT.
MAX_TOKENS = 1500  # hard ceiling on the returned message list
MAX_TOKENS_BEFORE_SUMMARY = 1500  # crossing this triggers a summarization pass
MAX_SUMMARY_TOKENS = 256  # budget reserved for the summary text itself

# same model & temp  as manual_summarizer.py
_summarizer_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# Same role->class mapping as manual_summarizer.py — reused, not re-invented.
_ROLE_TO_MESSAGE_CLASS = {
    "user": HumanMessage,
    "assistant": AIMessage,
}


def _to_langchain_messages(rows: list[Message]) -> list[AnyMessage]:
    """
    Convert our DB rows into LangChain messages WITH `.id` set.

    This is the detail from the explanation above: LangMem's own progress
    tracking (RunningSummary.summarized_message_ids) is keyed off each
    message object's `.id`. Skip this and LangMem has nothing stable to
    track between calls — it'll look like every message is new, every time.
    """
    return [
        _ROLE_TO_MESSAGE_CLASS.get(row.role, HumanMessage)(content=row.content, id=str(row.id))
        for row in rows
    ]


async def summarize_with_langmem_function(
    db: AsyncSession,
    thread_id: str,
    running_summary: RunningSummary | None,
) -> RunningSummary | None:
    """
    Call LangMem's summarize_messages() over the FULL thread history,
    persist a new summary row only if something genuinely new got folded
    in, and return the trimmed message list ready to hand to the graph.

    Loads the full history itself — not just "new" messages the way
    Lesson 5's maybe_summarize() does. LangMem finds its own split point
    by searching for last_summarized_message_id inside whatever list you
    give it (see 6.2's note), so a pre-filtered slice would break that.
    """
    rows = (
        await db.scalars(
            select(Message).where(Message.thread_id == thread_id).order_by(Message.id.asc())
        )
    ).all()
    messages = _to_langchain_messages(rows)

    result = summarize_messages(
        messages,
        running_summary=running_summary,
        model=_summarizer_model,
        max_tokens=MAX_TOKENS,
        max_tokens_before_summary=MAX_TOKENS_BEFORE_SUMMARY,
        max_summary_tokens=MAX_SUMMARY_TOKENS,
        token_counter=count_tokens_approximately,
    )

    # Persist only if something NEW was actually summarized this call —
    # compare boundaries, not just "is running_summary set". Without this
    # check we'd write a duplicate summaries row on every single turn,
    # forever, the moment the first summary exists.
    is_new_summary = result.running_summary is not None and (
        running_summary is None
        or result.running_summary.last_summarized_message_id
        != running_summary.last_summarized_message_id
    )
    if is_new_summary:
        db.add(
            Summary(
                thread_id=thread_id,
                summary_text=result.running_summary.summary,
                covered_until_message_id=int(result.running_summary.last_summarized_message_id),
                strategy="langmem",
            )
        )
    await db.commit()

    return result.messages


async def load_running_summary(db: AsyncSession, thread_id: str) -> RunningSummary | None:
    """
    Rebuild LangMem's RunningSummary from what's persisted in `summaries`.

    Call this at the start of every /chat request, before
    summarize_with_langmem_function(), so LangMem knows what it already
    covered last time instead of starting from scratch every request.
    """
    latest = await db.scalar(
        select(Summary)
        .where(Summary.thread_id == thread_id, Summary.strategy == "langmem")
        .order_by(Summary.id.desc())
        .limit(1)
    )
    if latest is None:
        return None

    # Exact reconstruction, not a guess — safe ONLY because `messages` is
    # append-only and never deleted (Lesson 1's schema decision). If this
    # app ever allowed deleting messages, this line would need to change.
    summarized_ids = await db.scalars(
        select(Message.id).where(
            Message.thread_id == thread_id,
            Message.id <= latest.covered_until_message_id,
        )
    )

    return RunningSummary(
        summary=latest.summary_text,
        summarized_message_ids={str(mid) for mid in summarized_ids},
        last_summarized_message_id=str(latest.covered_until_message_id),
    )
