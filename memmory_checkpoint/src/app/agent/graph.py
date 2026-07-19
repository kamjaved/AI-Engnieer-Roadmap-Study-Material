from typing import Annotated

from langchain_core.messages import AnyMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langmem.short_term import RunningSummary, SummarizationNode
from typing_extensions import TypedDict

from app.agent.tools import search_sailings
from app.core.config import get_settings
from app.db.checkpointer_pool import checkpointer

settings = get_settings()


# This TypedDict is the graph's entire "shape of state" — the React analogy:
# think of it as the type of your reducer's state object. `Annotated[...,
# add_messages]` is what tells LangGraph "when a node returns {'messages':
# [...]}, APPEND to the existing list, don't replace it." Without that
# annotation, returning messages from a node would silently overwrite the
# whole conversation state instead of adding to it.
class AgentState(TypedDict):
    # user messages
    messages: Annotated[list[AnyMessage], add_messages]
    # trimmed view SummarizationNode writes, agent_node reads
    llm_input_messages: list[AnyMessage]
    # SummarizationNode's own bookkeeping slot — we never touch this directly
    context: dict[str, RunningSummary]


TOOLS = [search_sailings]
# bind_tools() attaches the JSON-schema description of each tool to the
# model's request payload — this is what lets the model's response contain
# a "tool_calls" field instead of (or alongside) plain text. The model still
# never executes anything; it just returns structured intent.
model = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key).bind_tools(TOOLS)

_summarizer_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

summarization_node = SummarizationNode(
    model=_summarizer_model,
    max_tokens=3000,
    max_summary_tokens=512,
    token_counter=count_tokens_approximately,
    output_messages_key="llm_input_messages",
)


async def agent_node(state: AgentState) -> dict:
    # Defensive fallback only — by construction (START -> summarize ->
    # agent) llm_input_messages is always populated by the time this runs.
    messages = state.get("llm_input_messages") or state["messages"]
    response = await model.ainvoke(messages)
    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("summarize", summarization_node)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(TOOLS))

builder.add_edge(START, "summarize")
builder.add_edge("summarize", "agent")
builder.add_conditional_edges("agent", tools_condition)
# loop back through summarize, not straight to agent
builder.add_edge("tools", "summarize")


graph = builder.compile(checkpointer=checkpointer)
