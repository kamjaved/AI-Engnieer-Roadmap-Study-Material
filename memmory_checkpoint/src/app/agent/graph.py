from typing import Annotated

from langchain_core.messages import AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from app.agent.tools import search_sailings
from app.core.config import get_settings

settings = get_settings()


# This TypedDict is the graph's entire "shape of state" — the React analogy:
# think of it as the type of your reducer's state object. `Annotated[...,
# add_messages]` is what tells LangGraph "when a node returns {'messages':
# [...]}, APPEND to the existing list, don't replace it." Without that
# annotation, returning messages from a node would silently overwrite the
# whole conversation state instead of adding to it.
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


TOOLS = [search_sailings]
# bind_tools() attaches the JSON-schema description of each tool to the
# model's request payload — this is what lets the model's response contain
# a "tool_calls" field instead of (or alongside) plain text. The model still
# never executes anything; it just returns structured intent.
model = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key).bind_tools(TOOLS)


async def agent_node(state: AgentState) -> dict:
    """The one node that talks to the LLM. Reads the full messages list,
    returns a dict with a NEW list under 'messages' — the add_messages
    reducer appends it, it doesn't replace state['messages'].
    """
    response = await model.ainvoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(TOOLS))

builder.add_edge(START, "agent")

# tools_condition inspects the LAST message in state["messages"]: if it has
# tool_calls, route to the "tools" node; if not, route to END. This is the
# conditional edge — LangGraph's equivalent of an if/else in your reducer
# dispatch logic, except it's declared as graph structure instead of buried
# inside a function body.
builder.add_conditional_edges("agent", tools_condition)

# After tools run, ALWAYS go back to the agent so the model can read the
# tool's result and produce a real reply. This is a normal (unconditional)
# edge — no decision needed here, it's always this direction.
builder.add_edge("tools", "agent")

# Deliberately NOT passing a checkpointer here — that's Lesson 4. Every
# .ainvoke() call below starts from an empty `messages` list unless you
# pass full history in yourself, which you are not doing yet either.
graph = builder.compile()
