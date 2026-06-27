# Week 15: Interview Preparation

> **Month 4 -- Fine-Tuning, Multimodal, Portfolio & Job Hunt**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 14](./week-14-multimodal-portfolio.md) | Next: [Week 16](./week-16-job-hunt.md)

---

## Overview

This week prepares you for the three interview pillars: AI system design, technical depth, and behavioral storytelling. You will practice 5 system design scenarios, build a technical cheat sheet, reframe your TCS/EY experience into compelling STAR stories, and develop a focused DSA strategy that passes the gate without grinding. This week is about practice, not learning new concepts.

---

## Lesson 1: AI System Design Framework

**Sub-topics:**
- The REED framework: Requirements, Estimation, Evaluation, Design
- Clarifying requirements (what, who, scale, latency, accuracy)
- Back-of-envelope estimation (tokens, cost, QPS, storage)
- Starting with eval criteria before architecture
- Iterating from simple to complex (naive first, then optimize)
- Communicating tradeoffs clearly

**Key Concepts:**

AI system design interviews test whether you can architect a GenAI system from requirements to deployment. Use the REED framework: (1) Requirements -- clarify the problem, users, scale, and constraints. (2) Estimation -- calculate tokens, API costs, storage, and QPS. (3) Evaluation -- define how you will measure success before designing the system. (4) Design -- build the architecture iteratively, starting simple and adding complexity.

The eval-first approach is your differentiator. Most candidates jump straight to architecture. You start with: "Before I design the system, let me define how we'll measure its success." Then name specific metrics: faithfulness >0.9, P95 latency <3s, cost per query <$0.05, user satisfaction >4/5. This signals production thinking and sets up your architecture decisions as metric-driven choices.

**Interview Questions:**

1. *Design an AI-powered customer support system.*
   Requirements: handle 10K tickets/day, 80% auto-resolution rate, <2s response time, multilingual. Eval: resolution accuracy, escalation rate, CSAT score, faithfulness. Architecture: query classifier (route to FAQ RAG vs agent), RAG for knowledge base queries with hybrid search + reranking, agent for multi-step resolution (check order status, initiate refund), human escalation for out-of-scope or low-confidence responses. Langfuse tracing, eval suite gating deployments.

2. *Design a code review agent.*
   Requirements: PR analysis for a 50-person eng team, catch bugs + style issues + security vulnerabilities. Eval: precision (false positive rate), recall (bugs missed), developer acceptance rate. Architecture: LangGraph agent with tools -- git diff parser, AST analyzer, security rule checker. Multi-pass: style check (fast, cheap model), logic review (strong model), security scan (specialized). Human-in-the-loop approval before posting comments. MCP server for GitHub integration.

3. *Design a RAG system for 100M documents.*
   Requirements: sub-second retrieval, 99.9% uptime, fresh index (daily updates). Eval: retrieval recall@10, answer faithfulness, cost per query. Architecture: tiered retrieval -- inverted index (BM25) for initial filtering, vector search on the filtered subset, cross-encoder reranking on top-50. Sharded vector DB (Pinecone or Qdrant cluster). Incremental indexing pipeline. Semantic cache for frequent queries. Model routing: simple lookups to small model, complex synthesis to large model.

---

## Lesson 2: Technical Interview Patterns

**Sub-topics:**
- Handling scale questions (from prototype to production)
- Explaining RAG architecture clearly (ingest, chunk, embed, retrieve, generate)
- Hallucination mitigation strategies (grounding, citations, guardrails)
- Eval methodology (golden dataset, RAGAS, LLM-as-judge, regression testing)
- Cost optimization (caching, model routing, prompt compression)
- When to use agents vs chains vs simple prompts

**Key Concepts:**

Technical questions in GenAI interviews follow patterns. "How do you handle hallucination?" -- answer with grounding (RAG with citations), guardrails (faithfulness checks on output), and measurement (RAGAS faithfulness metric in your eval suite). "How do you handle scale?" -- answer with caching (semantic cache for repeated queries), model routing (cheap models for simple tasks), and infrastructure (sharded vector DB, horizontal API scaling).

Always connect your answers to your projects. "I handled hallucination in my RAG capstone by implementing a faithfulness check using RAGAS -- here's what my scores looked like..." is far stronger than a theoretical answer. Your EVALS.md and DECISIONS.md are evidence that you actually do this, not just know about it.

**Interview Questions:**

1. *How do you reduce hallucination in a production RAG system?*
   Multiple layers: high-quality retrieval (hybrid search + reranking to ensure relevant context), explicit grounding instructions in the prompt ("answer only from provided context"), citation requirement (forces the model to reference specific sources), faithfulness evaluation (RAGAS metric in CI/CD), and output guardrails (LLM-as-judge checking for unsupported claims). In my RAG capstone, this approach achieved 0.92 faithfulness on a 30-question eval suite.

2. *Walk me through how you would debug a RAG system that gives wrong answers.*
   Use Langfuse to trace the failing query end-to-end. Check: (1) Was the query routed correctly? (2) Were the retrieved documents relevant? (Look at similarity scores.) (3) Did the reranker help or hurt? (4) Was the prompt appropriate for this query type? (5) Did the LLM follow the prompt instructions? Identify which stage failed and fix that component. Add the failing query to the eval suite to prevent regression.

---

## Lesson 3: System Design Practice Scenarios

**Sub-topics:**
- Scenario 1: AI customer support system (10K tickets/day)
- Scenario 2: Code review agent (50-person team, GitHub integration)
- Scenario 3: Legal document Q&A (compliance, accuracy critical)
- Scenario 4: RAG at 100M documents (scale, freshness, cost)
- Scenario 5: Real-time recommendation engine (low latency, personalization)
- Practice format: 30 minutes per scenario, speak out loud

**Key Concepts:**

Practice these out loud. System design is a communication exercise as much as a technical one. Set a 30-minute timer. Spend 5 minutes on requirements and estimation, 5 minutes on eval criteria, 15 minutes on architecture (start simple, iterate), and 5 minutes on tradeoffs and scaling. Record yourself or practice with a peer.

For each scenario, identify the unique constraints: customer support needs multi-turn conversation and escalation paths; legal Q&A needs extreme accuracy and audit trails; 100M-doc RAG needs tiered retrieval and incremental indexing; real-time recommendations need sub-100ms latency and personalization. The architecture should be driven by these constraints, not by a one-size-fits-all template.

**Interview Questions:**

1. *Design a legal document Q&A system where accuracy is critical.*
   Requirements: 50K legal documents, lawyers as users, zero tolerance for hallucination, full audit trail. Eval: faithfulness >0.98, answer with exact section citations, recall of relevant clauses. Architecture: hierarchical chunking preserving document structure (section > subsection > paragraph). Hybrid search with heavy reranking. Generation prompt: "If the answer is not in the provided context, say so explicitly." Mandatory citation with section numbers. Human-in-the-loop review for high-stakes queries. Full audit trail via Langfuse. No answer is better than a wrong answer.

---

## Lesson 4: Behavioral Stories in STAR Format

**Sub-topics:**
- STAR format: Situation, Task, Action, Result
- Reframing TCS/EY consultancy work for GenAI roles
- Key stories: ownership, technical decision-making, handling ambiguity, conflict resolution, learning something new
- Quantifying results (even approximately)
- Connecting past experience to GenAI engineering

**Key Concepts:**

Your TCS and EY experience is a strength, but you need to reframe it. Interviewers are not asking "Were you good at your last job?" -- they are asking "Will you be good at this GenAI engineering role?" Every behavioral story should demonstrate a trait that transfers: making technical decisions with incomplete information, shipping under pressure, navigating stakeholder disagreements, learning new technology quickly, or owning a project end-to-end.

Write 5 STAR stories and practice them until they flow naturally (under 2 minutes each). Example reframe: "At EY, I led the frontend migration from Angular to React for a client's dashboard" becomes a story about evaluating tradeoffs (why React?), managing migration risk (incremental rollout), measuring success (load time improvement, developer velocity), and handling stakeholder pushback -- all skills directly applicable to GenAI system decisions.

**Interview Questions:**

1. *Tell me about a time you had to make a technical decision with incomplete information.*
   [Use one of your 5 STAR stories. Structure: Situation (what was the project/context), Task (what decision needed to be made), Action (how you gathered information, evaluated options, made the call), Result (what happened, what you learned). Keep under 2 minutes.]

2. *Tell me about a time you shipped something under pressure.*
   [Another STAR story. Emphasize: how you prioritized, what you cut, how you maintained quality under time constraints, and what the outcome was. Connect to GenAI: "This same prioritization skill is how I approached my RAG capstone -- I shipped a working system with evals before adding advanced features."]

---

## Lesson 5: DSA Refresh Strategy

**Sub-topics:**
- The reality: DSA is a gate, not a differentiator for GenAI roles
- NeetCode 150 as the focused path (not LeetCode grinding)
- Priority patterns: arrays/hashing, trees/graphs, dynamic programming basics
- Python-specific tricks (defaultdict, heapq, itertools)
- Time management: 2-3 problems per day, 30 minutes max each
- When to look at the solution (15 minutes stuck = look)

**Key Concepts:**

DSA interviews are a gate-keeping mechanism, not the core evaluation for GenAI roles. Your goal is to pass, not to excel. Use NeetCode 150 as your focused problem set -- it covers the patterns that appear most frequently. Prioritize: arrays and hashing (easiest wins), two pointers and sliding window, trees and graphs (BFS/DFS), and basic dynamic programming.

Spend 30 minutes per problem maximum. If you are stuck for 15 minutes, look at the solution, understand it, then solve it again from scratch the next day. Do 2-3 problems per day during this week. Your GenAI knowledge and portfolio are your differentiators -- DSA just needs to be "good enough" to not eliminate you.

**Interview Questions:**

1. *[No interview questions for this lesson -- the interview questions ARE the practice problems. Spend time solving NeetCode 150 problems instead.]*

---

## Lesson 6: Resume and LinkedIn Optimization

**Sub-topics:**
- Resume structure for "Full-Stack AI Engineer" positioning
- Quantifying GenAI project impact (eval scores, cost savings, performance metrics)
- Keywords for ATS: RAG, LangGraph, evals, RAGAS, Langfuse, MCP, fine-tuning
- LinkedIn headline and summary for GenAI positioning
- LinkedIn content strategy: post about what you built each week
- Portfolio link placement (GitHub, live demos)

**Key Concepts:**

Your resume should position you as a "Full-Stack AI Engineer" who ships production systems, not a "developer learning AI." Lead with your capstone projects: "Built a production RAG system with hybrid retrieval, RAGAS eval suite (0.92 faithfulness), Langfuse tracing, and React streaming UI. Deployed with CI/CD eval gating." This is concrete, measurable, and impressive.

For your TCS/EY experience, emphasize transferable skills: production deployment, system design, client-facing technical communication, and cross-functional collaboration. Add GenAI-specific keywords throughout for ATS: RAG, embeddings, vector search, LangGraph, evals, RAGAS, observability, Langfuse, MCP, fine-tuning, agents, prompt engineering.

**Interview Questions:**

1. *[No interview questions -- this is an execution lesson. Focus on writing your resume, optimizing your LinkedIn, and getting feedback.]*

---

## Assignment: Practice and Prepare

**Objective:** Practice 3 system design problems, write 5 STAR stories, and complete 1 mock interview.

**Requirements:**
- Practice 3 of the 5 system design scenarios out loud (30 min each, recorded or with a peer)
- Write 5 STAR stories covering: ownership, technical decision-making, conflict resolution, learning fast, shipping under pressure
- Complete 1 mock interview (peer, AI-assisted via Interviewing.io or Pramp, or self-recorded)
- Update resume with GenAI positioning and quantified project results
- Start NeetCode 150 (aim for 15-20 problems this week)

**Stretch goals:**
- Practice all 5 system design scenarios
- Do 2 mock interviews (1 system design, 1 behavioral)
- Get resume reviewed by a peer in the industry
- Record and review yourself answering: "Tell me about your RAG project"

---

## Summary Checklist

- [ ] Can use the REED framework for AI system design interviews
- [ ] Practiced 3+ system design scenarios out loud with timer
- [ ] 5 STAR stories written and practiced (under 2 minutes each)
- [ ] Technical answers connected to your actual capstone projects
- [ ] Resume updated for "Full-Stack AI Engineer" positioning
- [ ] LinkedIn profile optimized with GenAI keywords and project links
- [ ] Completed at least 1 mock interview
- [ ] Started NeetCode 150 (15+ problems done)
- [ ] Know the DSA patterns most likely to appear in your interviews
- [ ] System design sketch: practice scenario #4 or #5 from scratch
- [ ] Weekly writing: 1 LinkedIn post sharing something you built or learned
