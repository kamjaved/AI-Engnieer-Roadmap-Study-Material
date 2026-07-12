# api/routes_debug.py
from fastapi import APIRouter

from app.agent.graph import graph  # the compiled graph, checkpointer already attached

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
