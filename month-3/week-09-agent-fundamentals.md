# Week 9: Agent Fundamentals

> **Month 3 -- Agents, MCP & Production Infra**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 8](../month-2/week-08-rag-capstone.md) | Next: [Week 10](./week-10-multi-agent-mcp.md)

---

## Overview

This week marks the transition from retrieval systems to autonomous agents. You will learn what distinguishes an agent from a chain or chatbot, master the ReAct pattern, design effective tools, implement memory systems, and understand agent failure modes. By the end, you will have a working research agent that searches the web, synthesizes findings, and maintains session memory.

---

## Lesson 1: What Is an AI Agent

**Sub-topics:**
- Agent vs chain vs chatbot: the autonomy spectrum
- The observe-think-act loop
- Agents as goal-directed systems with tool access
- When agents are the right solution (and when they are overkill)
- Current limitations: reliability, cost, latency

**Key Concepts:**

A chatbot responds to messages. A chain follows a fixed sequence of operations. An agent makes autonomous decisions about what to do next. The defining characteristic of an agent is that the LLM decides the control flow -- which tools to call, in what order, and when to stop. This gives agents flexibility to handle novel situations but introduces unpredictability.

Agents are the right solution when: the task requires multiple steps that cannot be predetermined, different inputs need different tool sequences, or the task requires iterative refinement (try something, evaluate the result, adjust). Agents are overkill when: the workflow is predictable (use a chain), the task is a single LLM call (use a prompt), or reliability is more important than flexibility (agents can go off-rails).

**Interview Questions:**

1. *What distinguishes an AI agent from a simple LLM chain?*
   An agent has autonomous decision-making over control flow. The LLM chooses which tools to invoke and when to stop based on intermediate results, whereas a chain follows a fixed, predetermined sequence of operations.

2. *When would you NOT use an agent?*
   When the workflow is predictable and does not require dynamic tool selection, when reliability is critical (agents can loop or take unexpected paths), when the task is simple enough for a single LLM call, or when cost/latency constraints are tight (each agent step is an LLM call).

---

## Lesson 2: ReAct Pattern Deep Dive

**Sub-topics:**
- ReAct: Reasoning + Acting in an interleaved loop
- The thought-action-observation cycle
- Implementing ReAct from scratch (system prompt + tool loop)
- ReAct with LangGraph (tool node + conditional edge)
- Scratchpad and intermediate reasoning traces
- Iteration limits and exit conditions

**Key Concepts:**

ReAct interleaves reasoning and action. The LLM first thinks about what it needs to do (Thought), then chooses a tool to call (Action), then receives the result (Observation), and loops. This cycle continues until the LLM decides it has enough information to provide a final answer.

Implementing ReAct from scratch is straightforward: a system prompt that instructs the LLM to think step-by-step and use available tools, a loop that parses tool calls from the LLM output, executes them, and feeds results back, and a termination condition (the LLM returns a final answer without a tool call, or an iteration limit is hit). In LangGraph, this maps naturally: the LLM is one node, tool execution is another, and a conditional edge checks whether the LLM wants to call more tools or is done.

**Interview Questions:**

1. *Walk me through the ReAct loop step by step.*
   The LLM receives the user query and available tools. It generates a Thought (reasoning about what it needs), an Action (a specific tool call with parameters), receives an Observation (tool output), then generates another Thought based on the new information. This loops until the LLM decides it has enough information and outputs a final Answer instead of another Action.

2. *Why is ReAct better than just letting the LLM call tools without reasoning?*
   The explicit reasoning trace makes the agent's decisions interpretable and debuggable. You can see why it chose a particular tool and what it concluded from the result. It also improves decision quality -- forcing the model to reason before acting reduces impulsive or incorrect tool calls.

---

## Lesson 3: Tool Use Design

**Sub-topics:**
- Tool schema design (name, description, parameters)
- Writing tool descriptions that LLMs can use effectively
- Tool categories: web search, API calls, file operations, code execution
- Sandboxed code execution (E2B, Docker)
- Tool error handling and graceful degradation
- Tool result formatting (structured vs natural language)

**Key Concepts:**

The quality of your tool descriptions directly determines agent effectiveness. An LLM decides which tool to use based on the tool's name and description. Vague descriptions lead to wrong tool selection; overly complex parameter schemas lead to incorrect arguments. The best tool descriptions are concise, specific about what the tool does, explicit about input format, and clear about what the output looks like.

For code execution tools, sandboxing is non-negotiable. Services like E2B provide isolated containers where generated code runs safely. For web search, you need to handle rate limits, empty results, and irrelevant results gracefully. Every tool should return structured output (not raw HTML or massive JSON) that fits within the LLM's context window and is easy to reason about.

**Interview Questions:**

1. *How do you design tool descriptions for an LLM agent?*
   Keep descriptions concise and specific. State exactly what the tool does, what input format it expects, and what output it returns. Include usage examples in the description if the tool has complex parameters. Test with real queries to verify the LLM selects the right tool.

---

## Lesson 4: Memory Systems

**Sub-topics:**
- Conversation buffer memory (full history, windowed)
- Summary memory (LLM-generated conversation summaries)
- Episodic memory (storing and recalling specific past interactions)
- Procedural memory (learned skills and shortcuts)
- Long-term memory with vector stores
- Memory in LangGraph: state persistence and checkpointing

**Key Concepts:**

Agents need memory at multiple timescales. Conversation buffer memory stores the full chat history within a session -- simple but grows without bound. Windowed buffer keeps only the last N messages. Summary memory solves the growth problem by periodically summarizing older messages, keeping the context window manageable while retaining key information.

For agents that need to remember across sessions, long-term memory stores user preferences, past decisions, and learned context in a vector store. Episodic memory goes further: it stores structured records of past interactions (what the user asked, what the agent did, what worked) that can be retrieved when similar situations arise. LangGraph supports memory through checkpointing: you can save and restore the full graph state, enabling pause-resume workflows and persistent agents.

**Interview Questions:**

1. *How do you handle memory when conversation history exceeds the context window?*
   Use a sliding window for recent messages (full detail) combined with an LLM-generated summary of older messages. Alternatively, use a vector store to retrieve relevant past exchanges based on the current query. The choice depends on whether recency or relevance matters more for your use case.

2. *What is episodic memory in the context of AI agents?*
   Episodic memory stores structured records of past agent interactions: the task, tools used, approach taken, and outcome. When a similar task arises, the agent retrieves relevant episodes to inform its strategy, effectively learning from past experience without fine-tuning.

---

## Lesson 5: Planning Strategies

**Sub-topics:**
- Single-step planning (ReAct default: one tool call at a time)
- Multi-step planning (LLM generates a full plan, then executes)
- Plan-and-execute pattern (separate planner and executor)
- Tree-of-thought (explore multiple reasoning branches)
- Plan revision (update the plan based on intermediate results)
- Tradeoffs: planning overhead vs execution efficiency

**Key Concepts:**

Single-step planning (the basic ReAct loop) decides one action at a time. This is simple and adaptive but can be myopic -- the agent might take a suboptimal path because it did not think ahead. Multi-step planning asks the LLM to generate a complete plan upfront, then executes each step. This is more efficient but brittle -- if step 3 fails, the entire plan may need revision.

The plan-and-execute pattern is a practical middle ground: a "planner" LLM generates the plan, a separate "executor" LLM carries out each step, and after each step the planner can revise the remaining plan based on what was learned. This separation of concerns makes the system more robust and easier to debug.

**Interview Questions:**

1. *Compare single-step and multi-step planning in agents.*
   Single-step (ReAct) decides one action at a time based on accumulated observations -- it is adaptive but can be inefficient. Multi-step planning generates a full plan upfront -- it is more efficient but less adaptive to surprises. Plan-and-execute combines both: plan upfront, but revise after each step.

---

## Lesson 6: Agent Failure Modes & Guardrails

**Sub-topics:**
- Infinite loops (agent keeps calling tools without converging)
- Tool misuse (wrong tool, wrong parameters)
- Hallucinated tool calls (calling tools that do not exist)
- Scope creep (agent doing more than asked)
- Cost explosion (too many LLM calls in a loop)
- Guardrails: iteration limits, cost budgets, output validation
- Input guardrails: prompt injection detection, topic restriction
- Output guardrails: PII detection, toxicity filtering, format validation

**Key Concepts:**

Agents fail in predictable ways. Infinite loops happen when the agent cannot find what it needs but keeps trying the same approach. Tool misuse happens when tool descriptions are ambiguous. Cost explosion happens when the agent takes too many steps on a complex query. Every production agent needs guardrails: a maximum iteration count (typically 5-15), a cost budget per query, tool call validation (check parameters before execution), and output validation (ensure the final answer meets quality criteria).

Input guardrails protect against adversarial use: detect prompt injection attempts, restrict the agent to its intended domain, and validate that tool parameters do not contain malicious payloads. Output guardrails ensure quality: check for PII leakage, validate response format, and filter toxic content. In LangGraph, guardrails are nodes in the graph that run before and after the agent loop.

**Interview Questions:**

1. *What guardrails would you put on a production agent?*
   Iteration limit (prevent infinite loops), cost budget per query, tool parameter validation, input sanitization (prompt injection detection), output validation (PII filtering, format checks, toxicity screening), timeout per tool call, and comprehensive logging of every agent decision for debugging.

---

## Assignment: Research Agent

**Objective:** Build a research agent that searches the web, synthesizes findings, and maintains session memory.

**Requirements:**
- Implement ReAct pattern using LangGraph (nodes: LLM, tool_executor, synthesizer)
- Tools: web search (Tavily or SerpAPI), URL content extraction, note-taking (internal scratchpad)
- Session memory: conversation buffer with summary for long sessions
- Guardrails: max 10 iterations, cost tracking per query, input validation
- The agent should: accept a research question, search multiple sources, cross-reference findings, and produce a structured summary with citations
- Output format: structured markdown with sections, key findings, and source URLs

**Stretch goals:**
- Add a code execution tool (E2B sandbox) for data analysis tasks
- Implement plan-and-execute: generate a research plan, execute it, revise if needed
- Add episodic memory: store past research sessions for context in future queries
- Langfuse tracing on every agent step

---

## Summary Checklist

- [ ] Can explain the difference between agents, chains, and chatbots
- [ ] Implemented ReAct pattern from scratch and with LangGraph
- [ ] Designed effective tool schemas with clear descriptions
- [ ] Understand memory systems at multiple timescales
- [ ] Can articulate tradeoffs between planning strategies
- [ ] Know the common agent failure modes and how to guard against them
- [ ] Completed assignment: research agent with web search, synthesis, and memory
- [ ] System design sketch: customer support agent with escalation to human
- [ ] Weekly writing: 1 post about agent design patterns or failure modes
