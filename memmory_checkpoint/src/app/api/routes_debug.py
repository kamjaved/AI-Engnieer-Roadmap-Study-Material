# api/routes_debug.py
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.graph import graph  # the compiled graph, checkpointer already attached
from app.db.models import Message, Summary
from app.db.session import get_db_session
from app.memory.manual_summarizer import SUMMARIZE_TRIGGER_COUNT

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/threads/{thread_id}/checkpoint")
async def get_thread_checkpoint(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    # Read-only load — no node runs, no model call happens here.
    snapshot = await graph.aget_state(config)

    # snapshot.values is your raw state dict — messages are LangChain message
    # objects (HumanMessage/AIMessage/ToolMessage), not plain dicts, so we
    # pull out just the fields we want for a clean JSON response.
    messages = snapshot.values.get("messages", [])

    return {
        "thread_id": thread_id,
        "next_node": snapshot.next,  # () if the graph run to completion
        "message_count": len(messages),
        "messages": [
            {"type": msg.type, "content": msg.content}  # msg.type: "human" / "ai" / "tool"
            for msg in messages
        ],
    }


@router.get("/threads/{thread_id}/summary")
async def get_thread_summary(thread_id: str, db: AsyncSession = Depends(get_db_session)):
    # Same "latest summary" lookup shape as maybe_summarize() / get_context_for_turn().
    latest_summary = await db.scalar(
        select(Summary).where(Summary.thread_id == thread_id).order_by(Summary.id.desc()).limit(1)
    )
    covered_until_id = latest_summary.covered_until_message_id if latest_summary else 0

    # Same "how many new raw messages since the bookmark" query maybe_summarize() runs.
    new_message_count = await db.scalar(
        select(func.count(Message.id)).where(
            Message.thread_id == thread_id, Message.id > covered_until_id
        )
    )

    return {
        "thread_id": thread_id,
        "latest_summary": (
            {
                "summary_text": latest_summary.summary_text,
                "covered_until_message_id": latest_summary.covered_until_message_id,
                "strategy": latest_summary.strategy,
                "created_at": latest_summary.created_at,
            }
            if latest_summary
            else None
        ),
        "raw_message_count_since_summary": new_message_count,
        # Mirrors maybe_summarize()'s own trigger condition exactly.
        "would_trigger_summary_on_next_turn": new_message_count > SUMMARIZE_TRIGGER_COUNT,
    }
