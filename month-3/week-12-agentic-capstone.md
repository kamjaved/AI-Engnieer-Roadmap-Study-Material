# Week 12: Agentic Capstone (Project 3)

> **Month 3 -- Agents, MCP & Production Infra**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 11](./week-11-production-infra.md) | Next: [Week 13](../month-4/week-13-fine-tuning-advanced.md)

---

## Overview

This is your third capstone -- a deployed agentic system that showcases everything from Weeks 9-11. The system must use multiple tools (at least one via your own MCP server), be containerized with CI/CD, include observability and guardrails, and document cost-per-run with optimization. This is the project that proves you can build production AI systems, not just demos.

---

## Lesson 1: Agentic System Architecture

**Sub-topics:**
- Designing the agent's goal, tools, and boundaries
- Choosing between single-agent and multi-agent for your use case
- State schema design for complex workflows
- Error recovery and fallback strategies
- Architecture diagramming (component diagram, sequence diagram)

**Key Concepts:**

Start by defining the agent's purpose clearly: what task does it solve, what tools does it need, and what are its boundaries (what it should NOT do). Resist the temptation to build a "general purpose" agent -- scope it to a specific, demonstrable use case. Good capstone ideas: a research assistant that searches, summarizes, and saves to a knowledge base; a code review agent that analyzes PRs and suggests improvements; a customer support agent that queries a FAQ, escalates to human, and logs tickets.

Draw the architecture before writing code. Create a component diagram showing: the user interface, the agent orchestrator (LangGraph), each tool (with its MCP server or API), the memory system, the guardrail layer, and the observability stack (Langfuse). Then create a sequence diagram for the happy path and at least one error path.

**Interview Questions:**

1. *How do you scope an agentic system for production?*
   Define the specific task and success criteria. Enumerate the required tools and their capabilities. Set explicit boundaries (what the agent must not do). Design for the common case first, then handle edge cases. Build guardrails (iteration limits, cost budgets, input/output validation) into the architecture from the start, not as an afterthought.

2. *What goes into an ARCHITECTURE.md for an agentic system?*
   System overview and purpose, component diagram, data flow for the happy path, tool descriptions with when/why they are used, state schema, error handling strategy, guardrail configuration, cost analysis, scaling considerations, and known limitations.

---

## Lesson 2: Multi-Tool Agent with MCP Integration

**Sub-topics:**
- Connecting 2+ tools (at least 1 via MCP server)
- Tool selection optimization (clear descriptions, minimal overlap)
- Handling tool failures gracefully (retry, fallback, skip)
- Tool result parsing and validation
- MCP server deployment for remote access

**Key Concepts:**

Your agent must use at least 2 tools, with at least 1 exposed via your own MCP server. The other tool(s) can be direct integrations (web search API, database queries, code execution). The key challenge is tool orchestration: ensuring the agent selects the right tool for each step, handles failures without crashing, and produces coherent results even when a tool returns unexpected output.

Tool descriptions must be precise enough that the LLM reliably picks the right tool but not so specific that it misses valid use cases. Test tool selection empirically: run 20+ diverse queries and verify the agent chooses correctly. When it does not, refine the tool descriptions rather than adding more complex routing logic.

**Interview Questions:**

1. *How do you debug an agent that selects the wrong tool?*
   First, check the tool descriptions -- are they clear and distinctive? Second, examine the agent's reasoning trace (Thought step in ReAct) to understand why it made the selection. Third, test with simplified versions of the query to isolate the confusion. Usually the fix is improving tool descriptions rather than adding routing logic.

---

## Lesson 3: Containerization and CI/CD

**Sub-topics:**
- Dockerfile for the agentic system (multi-service)
- Docker Compose: agent API + MCP server + Redis + vector DB
- GitHub Actions: lint, test, eval, build, deploy
- Eval gating for agent systems (task completion metrics)
- Deployment to Railway/Render

**Key Concepts:**

Containerizing an agentic system is more complex than a simple RAG app because you have multiple services: the agent API, your MCP server, and any backing services. Docker Compose orchestrates these locally. For production, deploy each service separately or use a single container with a process manager (supervisord) for simplicity.

Agent evals are different from RAG evals. Instead of measuring retrieval quality, you measure task completion: given a task, did the agent complete it correctly? Define 15-20 test tasks with expected outcomes. Run them as part of CI and gate deployment on completion rate. Also track: average steps to completion, cost per task, and failure modes.

**Interview Questions:**

1. *How do you evaluate an agentic system for CI/CD gating?*
   Define task completion test cases: input tasks with expected outcomes. Measure completion rate (did the agent achieve the goal?), efficiency (how many steps/LLM calls?), cost per task, and guardrail violations (did it exceed iteration limits or attempt disallowed actions?). Gate deployment on completion rate > threshold (e.g., 85%).

---

## Lesson 4: Guardrails and Safety

**Sub-topics:**
- Input guardrails: prompt injection detection, topic restriction
- Output guardrails: format validation, PII filtering, toxicity detection
- Behavioral guardrails: iteration limits, cost budgets, action restrictions
- Implementing guardrails as LangGraph nodes
- Logging guardrail triggers for analysis
- NeMo Guardrails and Guardrails AI (library overview)

**Key Concepts:**

Production agents need three layers of guardrails. Input guardrails run before the agent processes a request: detect prompt injection, verify the request is within scope, and sanitize inputs. Behavioral guardrails run during execution: cap iterations, track cost, restrict which tools can be used on which data, and require human approval for high-stakes actions. Output guardrails run after the agent generates a response: validate format, check for PII leakage, and filter inappropriate content.

In LangGraph, implement guardrails as nodes in the graph. An input guardrail node runs before the agent loop. A cost-tracking node runs after each tool call. An output guardrail node runs before the final response is returned. Log every guardrail trigger to Langfuse so you can analyze patterns: are legitimate queries being blocked? Are adversarial queries getting through?

**Interview Questions:**

1. *Describe a three-layer guardrail architecture for a production agent.*
   Input layer: prompt injection detection, scope validation, input sanitization. Execution layer: iteration limits, cost budgets, tool restrictions, human-in-the-loop for high-stakes actions. Output layer: format validation, PII detection and redaction, toxicity filtering, source citation verification. Log all guardrail events for monitoring and tuning.

---

## Lesson 5: Cost Analysis and Optimization

**Sub-topics:**
- Measuring cost per agent run (LLM calls + tool costs)
- Cost breakdown by component (planning, tool use, generation)
- Optimization: model routing, prompt caching, early termination
- Setting cost budgets per query
- Reporting: cost dashboards, per-user tracking
- ROI framing: cost of agent vs cost of human for the same task

**Key Concepts:**

Agent systems are expensive because each step is an LLM call, and agents can take many steps. A single agent run might involve: 1 planning call, 3-5 tool selection calls, 1 synthesis call, and 1 guardrail check -- that is 6-8 LLM calls per query. At $3/M tokens for a strong model, a complex agent run can cost $0.05-0.50.

Document the cost per run in your DECISIONS.md. Break it down: what percentage is planning, tool selection, generation, and guardrails? Then optimize: use a cheap model for tool selection (Haiku/Mini), cache repeated planning patterns, terminate early when the agent has enough information, and batch tool calls where possible. Frame the cost against the alternative: if the agent replaces 15 minutes of human work, even $0.50/run is extremely cost-effective.

**Interview Questions:**

1. *How do you measure and optimize agent costs?*
   Track cost per run with Langfuse, broken down by component (LLM calls, tool costs). Identify the most expensive steps. Optimize with model routing (cheap models for classification, expensive for generation), prompt caching, early termination, and tool call batching. Set per-query cost budgets to prevent runaway costs. Compare against human-task-cost for ROI justification.

---

## Lesson 6: Documentation and Ship Checklist

**Sub-topics:**
- ARCHITECTURE.md: system design, component diagram, data flow
- DECISIONS.md: every choice with rationale and tradeoffs
- README: setup, usage, demo, architecture overview
- Cost analysis section: per-run cost, optimization applied, ROI framing
- Known limitations and future improvements
- Demo preparation: what to show, in what order

**Key Concepts:**

Your capstone documentation should be strong enough to serve as a work sample in interviews. ARCHITECTURE.md is the crown jewel: it should read like a design document that a senior engineer would respect. Include the system overview, component diagram, data flow for the happy path and error path, scaling considerations, security model, and cost analysis.

DECISIONS.md captures every non-obvious choice: Why LangGraph over raw Python? Why this MCP server architecture? Why this model for tool selection? Each decision should have context, options considered, decision made, rationale, and tradeoffs. This document demonstrates the engineering judgment that separates senior from junior.

**Interview Questions:**

1. *How do you demonstrate engineering judgment in a portfolio project?*
   Write a DECISIONS.md that documents every non-trivial choice with options considered, rationale, and tradeoffs acknowledged. Include an ARCHITECTURE.md with system design at current scale and discussion of what changes at 10x scale. Show cost analysis with optimization. Acknowledge limitations honestly.

---

## Assignment: Deployed Agentic System Capstone

**Objective:** Ship a production-ready agentic system that demonstrates agent fundamentals, MCP integration, and production infrastructure.

**Must-ship deliverables:**
- Multi-step agent using LangGraph with at least 2 tools
- At least 1 tool exposed via your own MCP server
- Containerized with Docker (Dockerfile + docker-compose.yml)
- GitHub Actions CI/CD with eval gating (15+ test tasks)
- Langfuse tracing on every agent step
- Input/output guardrails (prompt injection defense + output validation)
- Documented cost-per-run with optimization applied
- Deployed to Railway or Render
- ARCHITECTURE.md with component diagram and data flow
- DECISIONS.md with all architectural choices

**Stretch goals:**
- Multi-agent system (supervisor + 2 specialists)
- Human-in-the-loop approval gate for high-stakes actions
- Cost dashboard showing per-query and per-user costs
- Demo video (2-3 minutes) showing the system in action
- Blog post about building a production agent system

---

## Summary Checklist

- [ ] Agent architecture designed and diagrammed before coding
- [ ] Multi-step agent working with 2+ tools in LangGraph
- [ ] MCP server built, tested, and integrated with the agent
- [ ] Dockerized with docker-compose for local development
- [ ] GitHub Actions CI/CD with agent eval gating
- [ ] Langfuse tracing capturing every agent decision
- [ ] Input and output guardrails implemented and tested
- [ ] Cost-per-run documented with breakdown and optimization applied
- [ ] Deployed and accessible at a public URL
- [ ] ARCHITECTURE.md written with diagrams and scaling discussion
- [ ] DECISIONS.md written with every choice documented
- [ ] Portfolio-ready: impressive demo, clean code, strong documentation
- [ ] System design sketch: scaling this agent to 10K daily active users
- [ ] Weekly writing: 1 post about building, deploying, or optimizing your agentic system
