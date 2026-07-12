from fastapi import APIRouter, Depends
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.graph import graph
from app.db.models import ConversationThread, Message
from app.db.session import get_db_session

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: int
    thread_id: str
    message: str


class ChatResponse(BaseModel):
    thread_id: str
    answer: str


async def _ensure_thread(db: AsyncSession, thread_id: str, user_id: int) -> None:
    """Create the conversation_threads row on first use. Without this,
    inserting into `messages` would violate the foreign key the moment a
    brand-new thread_id shows up — conversation_threads is the parent row.
    """
    existing = await db.get(ConversationThread, thread_id)
    if existing is None:
        db.add(ConversationThread(thread_id=thread_id, user_id=user_id))
        await db.flush()  # so the FK below sees this row without a full commit yet


async def _save_message(db: AsyncSession, thread_id: str, role: str, content: str) -> None:
    db.add(Message(thread_id=thread_id, role=role, content=content))


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db_session)) -> ChatResponse:
    await _ensure_thread(db, req.thread_id, req.user_id)
    await _save_message(db, req.thread_id, role="user", content=req.message)
    await db.commit()  # commit BEFORE the (possibly slow) LLM call, not after —
    # so the user's message is durable even if the graph call fails or times out downstream.

    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=req.message)]},
        config={"configurable": {"thread_id": req.thread_id}},
    )
    reply = result["messages"][-1]
    await _save_message(db, req.thread_id, role="assistant", content=reply.content)
    await db.commit()

    return ChatResponse(thread_id=req.thread_id, answer=reply.content)
