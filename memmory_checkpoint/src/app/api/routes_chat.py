import uuid
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.graph import graph
from app.db.models import ConversationThread, Message
from app.db.session import get_db_session
from app.memory.manual_summarizer import get_context_for_turn, get_debug_context, maybe_summarize

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: int
    thread_id: str
    message: str


class DebugContext(BaseModel):
    """Captures the exact context sent to the LLM for debugging."""

    timestamp: datetime
    thread_id: str
    current_message_id: int

    # Summary info (if exists)
    summary: dict | None  # {summary_text, covered_until_message_id, strategy, created_at}

    # Raw message window (KEEP_RAW_COUNT newest before current turn)
    raw_window: list[dict]  # [{id, role, content, created_at}, ...]

    # Final assembled context sent to LLM
    final_context: list[dict]  # [{type, content}, ...]

    # Metadata for debugging
    metadata: dict  # {system_prompt_length, total_tokens_estimate, raw_window_count}


class ChatResponse(BaseModel):
    thread_id: str
    answer: str
    debug: DebugContext | None = None


async def _ensure_thread(db: AsyncSession, thread_id: str, user_id: int) -> None:
    """Create the conversation_threads row on first use. Without this,
    inserting into `messages` would violate the foreign key the moment a
    brand-new thread_id shows up — conversation_threads is the parent row.
    """
    existing = await db.get(ConversationThread, thread_id)
    if existing is None:
        db.add(ConversationThread(thread_id=thread_id, user_id=user_id))
        await db.flush()  # so the FK below sees this row without a full commit yet


async def _save_message(db: AsyncSession, thread_id: str, role: str, content: str) -> Message:
    # get_context_for_turn() needs current_message.id — and .id only gets
    # populated by the database after a flush (autoincrement PK), not at
    # the moment db.add() is called.
    message = Message(thread_id=thread_id, role=role, content=content)
    db.add(message)
    await db.flush()  # sends the INSERT, populates message.id — doesn't commit yet
    return message


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db_session)) -> ChatResponse:
    await _ensure_thread(db, req.thread_id, req.user_id)
    current_message = await _save_message(db, req.thread_id, role="user", content=req.message)
    await db.commit()

    await maybe_summarize(db, req.thread_id)
    context = await get_context_for_turn(db, req.thread_id, current_message)

    # Collect debug info: summary, raw window, final context
    debug_info = await get_debug_context(db, req.thread_id, current_message, context)

    result = await graph.ainvoke(
        {"messages": context},
        config={"configurable": {"thread_id": f"{req.thread_id}:{uuid.uuid4()}"}},
    )
    reply = result["messages"][-1]
    await _save_message(db, req.thread_id, role="assistant", content=reply.content)
    await db.commit()

    return ChatResponse(thread_id=req.thread_id, answer=reply.content, debug=debug_info)
