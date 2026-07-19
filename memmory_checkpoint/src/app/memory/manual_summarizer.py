from __future__ import annotations

from datetime import datetime

from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Message, Summary

# Magic numbers as named constants
SUMMARIZE_TRIGGER_COUNT = 6
KEEP_RAW_COUNT = 3

# System message that stays the same every turn (move to config later if needed)
BASE_SYSTEM_PROMPT = (
    "You are a helpful cruise-booking assistant. Use the tools available "
    "to you to answer questions about sailings. Be concise and accurate."
)

# DB stores role as string, LangChain needs actual message objects
_ROLE_TO_MESSAGE_CLASS = {
    "user": HumanMessage,
    "assistant": AIMessage,
}

# Cheap mini model for summarization (temperature=0 for reproducible compression)
_summarizer_llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


async def maybe_summarize(db: AsyncSession, thread_id: str) -> None:
    """
    If enough new raw messages have piled up since the last summary,
    compress them into an updated summary row. Otherwise, no-op.

    Must run BEFORE get_context_for_turn() on every /chat call (5.3) —
    we'll dig into exactly why in 5.9.
    """
    # Grab latest summary as bookmark for what we've already compressed
    latest_summary = await db.scalar(
        select(Summary).where(Summary.thread_id == thread_id).order_by(Summary.id.desc()).limit(1)
    )
    covered_until_id = latest_summary.covered_until_message_id if latest_summary else 0

    # Count new messages since that bookmark
    new_message_count = await db.scalar(
        select(func.count(Message.id)).where(
            Message.thread_id == thread_id, Message.id > covered_until_id
        )
    )

    if new_message_count <= SUMMARIZE_TRIGGER_COUNT:
        return

    # Grab new messages, oldest first
    new_messages = (
        await db.scalars(
            select(Message)
            .where(Message.thread_id == thread_id, Message.id > covered_until_id)
            .order_by(Message.id.asc())
        )
    ).all()

    # Don't double-count: exclude current turn's message + keep raw window uncompressed
    # (Bug fix: current message wasn't excluded before,
    # so it got folded into summary AND still appeared in raw window)
    messages_before_current = new_messages[:-1] if new_messages else []
    to_summarize = messages_before_current[:-KEEP_RAW_COUNT]
    if not to_summarize:
        return

    # Fold old summary into prompt so we update it, not replace it
    transcript = "\n".join(f"{m.role}: {m.content}" for m in to_summarize)
    if latest_summary:
        instruction = (
            "Current summary of the conversation so far:\n"
            f"{latest_summary.summary_text}\n\n"
            "New messages that happened after that summary. Update the "
            "summary to fold in any important new information, staying "
            "concise:\n\n"
            f"{transcript}"
        )
    else:
        instruction = (
            "Summarize this conversation concisely. Capture any facts, "
            "preferences, or decisions that later turns might need to "
            "refer back to:\n\n"
            f"{transcript}"
        )

    response = await _summarizer_llm.ainvoke(
        [
            SystemMessage(content="You are a precise, factual conversation summarizer."),
            HumanMessage(content=instruction),
        ]
    )

    # Save it with the bookmark pointing to the last message it covers
    db.add(
        Summary(
            thread_id=thread_id,
            summary_text=response.content,
            covered_until_message_id=to_summarize[-1].id,
            strategy="manual",
        )
    )
    await db.commit()


async def get_context_for_turn(
    db: AsyncSession, thread_id: str, current_message: Message
) -> list:
    """
    Build exactly what gets sent to the LLM this turn:
      [system message] + [up to KEEP_RAW_COUNT prior raw messages] + [this turn]

    `current_message` is the Message row already persisted for this turn.
    We use its `.id` as a boundary so the history query below can never
    pull it in twice.
    """
    # Grab latest summary
    latest_summary = await db.scalar(
        select(Summary).where(Summary.thread_id == thread_id).order_by(Summary.id.desc()).limit(1)
    )

    # Start with base system prompt, tack summary on if it exists
    system_text = BASE_SYSTEM_PROMPT
    if latest_summary:
        system_text += f"\n\nSummary of the conversation so far:\n{latest_summary.summary_text}"

    # Raw window: most recent KEEP_RAW_COUNT messages before this turn
    # (id < current avoids double-counting it)
    raw_window = (
        await db.scalars(
            select(Message)
            .where(Message.thread_id == thread_id, Message.id < current_message.id)
            .order_by(Message.id.desc())
            .limit(KEEP_RAW_COUNT)
        )
    ).all()
    raw_window = list(reversed(raw_window))

    # Build final context: system + prior messages + current message
    context: list = [SystemMessage(content=system_text)]
    for msg in raw_window:
        message_cls = _ROLE_TO_MESSAGE_CLASS.get(msg.role, HumanMessage)
        context.append(message_cls(content=msg.content))
    context.append(HumanMessage(content=current_message.content))

    return context


async def get_debug_context(
    db: AsyncSession, thread_id: str, current_message: Message, context: list
) -> dict:
    """
    Capture all debugging info about the context being sent to the LLM.
    Includes summary details, raw message window, and final assembled context.
    """
    # Get latest summary
    latest_summary = await db.scalar(
        select(Summary).where(Summary.thread_id == thread_id).order_by(Summary.id.desc()).limit(1)
    )

    # Format it for output if it exists
    summary_info = None
    if latest_summary:
        summary_info = {
            "summary_text": latest_summary.summary_text,
            "covered_until_message_id": latest_summary.covered_until_message_id,
            "strategy": latest_summary.strategy,
            "created_at": latest_summary.created_at.isoformat(),
        }

    # Grab the raw message window (same query as get_context_for_turn)
    raw_window_msgs = (
        await db.scalars(
            select(Message)
            .where(Message.thread_id == thread_id, Message.id < current_message.id)
            .order_by(Message.id.desc())
            .limit(KEEP_RAW_COUNT)
        )
    ).all()
    raw_window_msgs = list(reversed(raw_window_msgs))

    raw_window = [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
        }
        for msg in raw_window_msgs
    ]

    # Extract message type and content for the final context
    final_context = [{"type": msg.type, "content": msg.content} for msg in context]

    # Rough token count (1 token ≈ 4 chars)
    total_chars = sum(len(msg.get("content", "")) for msg in final_context)
    token_estimate = total_chars // 4

    # Gather all the stats
    metadata = {
        "system_prompt_length": len(context[0].content) if context else 0,
        "raw_window_count": len(raw_window),
        "total_messages_in_context": len(context),
        "total_chars": total_chars,
        "estimated_tokens": token_estimate,
    }

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "thread_id": thread_id,
        "current_message_id": current_message.id,
        "summary": summary_info,
        "raw_window": raw_window,
        "final_context": final_context,
        "metadata": metadata,
    }
