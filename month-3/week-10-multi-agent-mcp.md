# Week 10: Multi-Agent Systems + MCP

> **Month 3 -- Agents, MCP & Production Infra**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 9](./week-09-agent-fundamentals.md) | Next: [Week 11](./week-11-production-infra.md)

---

## Overview

This week covers two major topics: multi-agent architectures and the Model Context Protocol (MCP). You will learn when and how to decompose a task across multiple agents, implement multi-agent coordination with LangGraph, and build your own MCP server. MCP is a 2026 production reality -- understanding it is no longer optional.

---

## Lesson 1: Multi-Agent Patterns

**Sub-topics:**
- Orchestrator-worker pattern (central coordinator delegates to specialists)
- Debate pattern (agents argue different perspectives, synthesize)
- Delegation pattern (agents hand off subtasks to each other)
- Hierarchical pattern (manager agents supervise worker agents)
- When multi-agent adds value vs unnecessary complexity
- Communication: shared state vs message passing

**Key Concepts:**

Multi-agent systems decompose complex tasks by assigning specialized roles to different agents. The orchestrator-worker pattern is the most common: a supervisor agent receives the task, breaks it into subtasks, delegates each to a specialist agent (researcher, writer, reviewer, coder), and assembles the results. Each specialist has its own system prompt, tools, and focus area.

The debate pattern is valuable when you want multiple perspectives: two agents argue opposing viewpoints on a decision, and a third synthesizes the strongest arguments. This reduces the single-model bias problem. However, multi-agent systems add complexity (more LLM calls, harder debugging, coordination overhead). Use them only when the task genuinely benefits from specialization -- most tasks that feel like multi-agent problems can be solved with a single well-prompted agent and multiple tools.

**Interview Questions:**

1. *When is a multi-agent system justified over a single agent?*
   When the task requires genuinely different expertise that cannot be captured in one system prompt, when subtasks are independent and can run in parallel, or when you need adversarial checking (one agent verifies another's work). A single agent with multiple tools is simpler and cheaper for most use cases.

2. *What are the coordination challenges in multi-agent systems?*
   State consistency (agents can have conflicting views of shared state), communication overhead (each handoff is an LLM call), error propagation (one agent's mistake compounds downstream), debugging difficulty (tracing issues across agents), and cost multiplication (N agents means roughly N times the LLM calls).

3. *Describe the orchestrator-worker pattern.*
   A supervisor agent receives the task and creates a plan. It delegates subtasks to specialized worker agents (researcher, coder, reviewer, etc.), each with their own tools and system prompt. The supervisor collects results, resolves conflicts, and assembles the final output. In LangGraph, the supervisor is the main graph with worker agents as subgraphs.

---

## Lesson 2: LangGraph for Multi-Agent Coordination

**Sub-topics:**
- Modeling agents as LangGraph subgraphs
- Shared state schema across agents
- Supervisor node with conditional routing to agents
- Parallel agent execution
- Human-in-the-loop approval gates
- Breakpoints and debugging multi-agent flows

**Key Concepts:**

LangGraph models multi-agent systems naturally. Each agent is a subgraph with its own nodes (LLM, tools) and internal state. The supervisor is the outer graph that routes tasks to agent subgraphs based on the current state. Shared state flows between agents -- the researcher agent writes its findings to state, and the writer agent reads them.

Human-in-the-loop is implemented as a special node that pauses the graph and waits for human input. In LangGraph, you use `interrupt_before` or `interrupt_after` on specific nodes. This is critical for production agents that take consequential actions -- a financial agent should always get human approval before executing a trade. The graph persists its state during the interrupt, so the human can review and approve asynchronously.

**Interview Questions:**

1. *How do you implement human-in-the-loop approval in LangGraph?*
   Use `interrupt_before` on the node that takes the consequential action. LangGraph pauses execution, persists the graph state (including the proposed action), and waits for external input. The human reviews the proposed action via a UI, approves or rejects, and the graph resumes from the checkpoint. This enables async approval workflows without losing context.

---

## Lesson 3: MCP (Model Context Protocol) Deep Dive

**Sub-topics:**
- What MCP is and the problem it solves
- The MCP specification: architecture overview
- Why MCP matters in 2026 (standardized tool integration)
- MCP vs custom API integrations (tradeoffs)
- The MCP ecosystem: existing servers, registries, adoption

**Key Concepts:**

Model Context Protocol is a standardized protocol for connecting AI models to external tools and data sources. Before MCP, every AI application had to build custom integrations for each tool -- a Slack integration, a GitHub integration, a database integration, each with its own code. MCP standardizes this: tool providers build one MCP server, and any MCP-compatible AI application can use it.

The analogy is USB for AI tools. Just as USB standardized hardware connections so any device works with any computer, MCP standardizes tool connections so any tool works with any AI application. In 2026, MCP is production infrastructure: Claude, GPT, and other models all support MCP clients, and there are hundreds of MCP servers for popular services. Understanding MCP is essential for building and integrating AI systems.

**Interview Questions:**

1. *What problem does MCP solve?*
   It eliminates the N*M integration problem. Without MCP, N AI applications each need custom integrations for M tools, resulting in N*M integration code. With MCP, each tool builds one server and each AI app builds one client, reducing to N+M implementations.

2. *How does MCP compare to custom API integrations?*
   MCP provides a standardized protocol with automatic tool discovery, type safety, and a growing ecosystem. Custom integrations offer more control and can be more efficient for specific use cases. MCP trades some flexibility for dramatically reduced integration effort and broader compatibility.

---

## Lesson 4: MCP Architecture

**Sub-topics:**
- Client-server model
- Transport layer: stdio, SSE, HTTP
- Tool primitives: tools, resources, prompts
- Tool discovery and schema negotiation
- Authentication and security considerations
- Session lifecycle

**Key Concepts:**

MCP follows a client-server architecture. The MCP client lives inside the AI application (e.g., Claude Desktop, your LangGraph agent). The MCP server wraps an external tool or data source and exposes it via the MCP protocol. Communication happens over a transport layer -- stdio for local servers (the server runs as a subprocess), SSE for remote servers (HTTP-based streaming), and streamable HTTP for production deployments.

MCP defines three primitives: **Tools** (actions the model can invoke, like "send_email" or "query_database"), **Resources** (data the model can read, like files or database schemas), and **Prompts** (pre-built prompt templates the server offers). When a client connects to a server, it discovers available tools, resources, and prompts through a handshake. The client then presents these to the LLM, which can invoke them during its reasoning loop.

**Interview Questions:**

1. *What are MCP's three primitives and how do they differ?*
   Tools are executable actions with parameters (search, create, update). Resources are read-only data sources (files, schemas, configs). Prompts are reusable prompt templates provided by the server. Tools change state, resources provide context, and prompts standardize interaction patterns.

---

## Lesson 5: Building an MCP Server

**Sub-topics:**
- Setting up an MCP server project (Python SDK)
- Defining tools with schemas and handlers
- Defining resources (static and dynamic)
- Testing your server locally with MCP Inspector
- Connecting to Claude Desktop or your own agent
- Error handling and logging in MCP servers

**Key Concepts:**

Building an MCP server in Python is straightforward with the `mcp` SDK. You define your tools using decorators: `@server.tool()` marks a function as an MCP tool, with the function's docstring and type hints becoming the tool schema. The SDK handles protocol negotiation, message serialization, and transport automatically.

A minimal MCP server: create a `Server` instance, define tools with typed parameters and docstrings, implement the handler functions, and run with the appropriate transport (stdio for local testing, SSE for remote). Test with MCP Inspector (a browser-based tool that connects to your server and lets you invoke tools manually). Once working, connect it to Claude Desktop by adding the server config to `claude_desktop_config.json`, or integrate it into your LangGraph agent via the MCP client library.

**Interview Questions:**

1. *Walk me through building a simple MCP server.*
   Install the MCP Python SDK. Create a Server instance. Define tools using the `@server.tool()` decorator with typed parameters and clear docstrings. Implement the handler logic. Test locally with MCP Inspector. Deploy for production with SSE transport. Connect clients by pointing them to your server's endpoint.

2. *How do you test an MCP server during development?*
   Use MCP Inspector, a browser-based testing tool that connects to your server, shows available tools/resources/prompts, and lets you invoke them interactively. For automated testing, use the MCP client library to write integration tests that connect to your server and validate tool responses.

---

## Lesson 6: MCP Tools vs Resources vs Prompts

**Sub-topics:**
- When to use tools vs resources vs prompts
- Designing tool schemas for LLM consumption
- Resource templates and dynamic resources
- Prompt templates with arguments
- Composing multiple MCP servers in one agent

**Key Concepts:**

The distinction matters for design. Use **tools** when the LLM needs to take an action or retrieve dynamic data: querying a database, sending a notification, creating a record. Use **resources** when you want to provide static or semi-static context: database schemas, configuration files, documentation pages. Resources are read-only and can be pre-loaded into the LLM's context.

Use **prompts** when you want to standardize how users or agents interact with your service. A prompt template might be "summarize_ticket" with a `ticket_id` argument, which fetches the ticket and returns a pre-formatted prompt for summarization. Prompts encode domain expertise about how to best use the tools and resources your server provides.

**Interview Questions:**

1. *When would you expose something as a resource vs a tool in MCP?*
   Use a resource for data the LLM should have as context (schemas, docs, configs) -- it is read-only and can be pre-loaded. Use a tool when the LLM needs to perform an action or query dynamic data. If the data changes per request or has side effects, it is a tool. If it is reference material, it is a resource.

---

## Assignment: Build an MCP Server + Agent Integration

**Objective:** Build a small MCP server exposing a useful tool, then integrate it with an agent.

**Requirements:**
- Build an MCP server in Python that exposes at least 1 tool and 1 resource
  - Example tool ideas: query a local SQLite database, manage a todo list, search your notes, interact with a public API
- Test with MCP Inspector
- Connect the server to your Week 9 research agent (or a new agent) via the MCP client library
- The agent should be able to discover and use your MCP tool autonomously
- Document the server's tool schemas in the README

**Stretch goals:**
- Build a second MCP server for a different service and compose both in one agent
- Add authentication to your MCP server
- Deploy the server with SSE transport so it can be accessed remotely
- Connect your server to Claude Desktop as well as your custom agent

---

## Summary Checklist

- [ ] Can explain multi-agent patterns and when each is appropriate
- [ ] Implemented a multi-agent workflow in LangGraph with supervisor routing
- [ ] Understand human-in-the-loop approval gates and their implementation
- [ ] Can explain MCP architecture, primitives, and transport layers
- [ ] Built a working MCP server with at least 1 tool and 1 resource
- [ ] Integrated MCP server with an agent that uses the tool autonomously
- [ ] Tested with MCP Inspector
- [ ] Completed assignment: MCP server + agent integration
- [ ] System design sketch: multi-agent system for code review (planner, reviewer, tester agents)
- [ ] Weekly writing: 1 post about MCP, multi-agent patterns, or agent coordination challenges
