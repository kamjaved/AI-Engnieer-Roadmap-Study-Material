import uuid
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.graph import graph
from app.db.models import ConversationThread, Message
from app.db.session import get_db_session
from app.memory.langmem_summarizer import load_running_summary, summarize_with_langmem_function
from app.memory.manual_summarizer import get_context_for_turn, get_debug_context, maybe_summarize

router = APIRouter()

SummaryMode = Literal["manual", "langmem_function", "langmem_node"]


class ChatRequest(BaseModel):
    user_id: int
    thread_id: str
    message: str
    summary_mode: SummaryMode | None = None


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


async def _ensure_thread(
    db: AsyncSession, thread_id: str, user_id: int, summary_mode: str | None = None
) -> None:
    """Create the conversation_threads row on first use. Without this,
    inserting into `messages` would violate the foreign key the moment a
    brand-new thread_id shows up — conversation_threads is the parent row.
    """
    existing = await db.get(ConversationThread, thread_id)
    if existing is None:
        db.add(
            ConversationThread(
                thread_id=thread_id,
                user_id=user_id,
                **({"summary_mode": summary_mode} if summary_mode else {}),
            )
        )
        await db.flush()  # so the FK below sees this row without a full commit yet
    elif summary_mode is not None and summary_mode != existing.summary_mode:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Thread {thread_id!r} already exists with summary_mode="
                f"{existing.summary_mode!r}; cannot change it to {summary_mode!r} "
                "via /chat. Use a new thread_id, or omit summary_mode to keep "
                "the existing one."
            ),
        )


async def _save_message(db: AsyncSession, thread_id: str, role: str, content: str) -> Message:
    # get_context_for_turn() needs current_message.id — and .id only gets
    # populated by the database after a flush (autoincrement PK), not at
    # the moment db.add() is called.
    message = Message(thread_id=thread_id, role=role, content=content)
    db.add(message)
    await db.flush()  # sends the INSERT, populates message.id — doesn't commit yet
    return message


#  --------------------------------------------------------------------------------------
#  --------------NEW CHAT VERSION SUPPORT MANUAL * LANGMEM SUMMARIZATION-----------------
#  --------------------------------------------------------------------------------------


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db_session)) -> ChatResponse:
    await _ensure_thread(db, req.thread_id, req.user_id, req.summary_mode)
    current_message = await _save_message(db, req.thread_id, role="user", content=req.message)
    await db.commit()

    thread = await db.get(ConversationThread, req.thread_id)
    summary_mode = thread.summary_mode

    # Only 'manual'/'langmem_function' assemble a context list we can
    # meaningfully debug-dump today. langmem_node's context assembly
    # happens INSIDE the graph — extending this properly is 6.5's job.
    debug_info = None

    if summary_mode == "manual":
        await maybe_summarize(db, req.thread_id)
        context = await get_context_for_turn(db, req.thread_id, current_message)
        debug_info = await get_debug_context(db, req.thread_id, current_message, context)
        invoke_thread_id = f"{req.thread_id}:{uuid.uuid4()}"
        graph_input = {"messages": context}

    elif summary_mode == "langmem_function":
        running_summary = await load_running_summary(db, req.thread_id)
        context = await summarize_with_langmem_function(db, req.thread_id, running_summary)
        debug_info = await get_debug_context(db, req.thread_id, current_message, context)
        invoke_thread_id = f"{req.thread_id}:{uuid.uuid4()}"
        graph_input = {"messages": context}

    elif summary_mode == "langmem_node":
        # The checkpoint IS the memory here — stable thread_id, only the
        # new message. add_messages + SummarizationNode do everything else.
        invoke_thread_id = req.thread_id
        graph_input = {"messages": [HumanMessage(content=req.message)]}

    else:
        raise ValueError(f"Unknown summary_mode {summary_mode!r} for thread {req.thread_id}")

    result = await graph.ainvoke(
        graph_input,
        config={"configurable": {"thread_id": invoke_thread_id}},
    )
    reply = result["messages"][-1]
    await _save_message(db, req.thread_id, role="assistant", content=reply.content)
    await db.commit()

    return ChatResponse(thread_id=req.thread_id, answer=reply.content, debug=debug_info)


#  -----------------------------------------------------------------------
#  --------------LEGACY ONLY SUPPORT MANUAL SUMMARIZATION-----------------
#  -----------------------------------------------------------------------
# @router.post("/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db_session)) -> ChatResponse:
#     await _ensure_thread(db, req.thread_id, req.user_id)
#     current_message = await _save_message(db, req.thread_id, role="user", content=req.message)
#     await db.commit()

#     await maybe_summarize(db, req.thread_id)
#     context = await get_context_for_turn(db, req.thread_id, current_message)

#     # Collect debug info: summary, raw window, final context
#     debug_info = await get_debug_context(db, req.thread_id, current_message, context)

#     result = await graph.ainvoke(
#         {"messages": context},
#         config={"configurable": {"thread_id": f"{req.thread_id}:{uuid.uuid4()}"}},
#     )
#     reply = result["messages"][-1]
#     await _save_message(db, req.thread_id, role="assistant", content=reply.content)
#     await db.commit()

#     return ChatResponse(thread_id=req.thread_id, answer=reply.content, debug=debug_info)
