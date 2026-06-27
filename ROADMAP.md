# GenAI Engineer Study Roadmap

> **16-week structured plan to transition from Senior Fullstack Developer to Senior GenAI Engineer/Architect**

## Who This Is For

Kamran -- 7 years of frontend-heavy fullstack experience (TCS/EY consultancy), strong in React/TypeScript/Node, looking to make a deliberate transition into GenAI engineering. This plan assumes **10-15 hours per week** of dedicated study time, prioritizing depth over breadth and shipping over collecting frameworks.

**The goal:** By Week 16, have a portfolio of production-quality GenAI projects, deep understanding of RAG/agents/evals, and the ability to architect GenAI systems from scratch -- not just wire APIs together.

---

## Design Principles

1. **Evals-first mindset.** Every project includes evaluation criteria before building. If you cannot measure it, you cannot improve it.
2. **Ship monthly.** Each month culminates in a capstone project you can demo and add to your portfolio.
3. **Write tradeoffs, not just code.** Maintain a `DECISIONS.md` in every project documenting what you chose, what you rejected, and why.
4. **Avoid framework collecting.** Learn one tool deeply rather than five tools superficially. LangGraph is the primary orchestration framework; pick up others only when a capstone demands it.
5. **Current tech only.** Focus on patterns and tools that are production-relevant today. Skip historical context unless it clarifies a current concept.
6. **Python-first.** All GenAI work in Python. Your TypeScript/Node skills transfer to frontend integration and tooling -- not to core AI pipelines.

---

## Honest Self-Assessment

Complete this before starting. Revisit at Week 8 and Week 16.

### Strengths to Leverage

| Strength | How It Helps |
|---|---|
| Production fullstack experience | You already know deployment, CI/CD, monitoring, API design |
| TypeScript/React | Frontend for demos, chatbot UIs, dashboard prototypes |
| Consultancy background | Stakeholder communication, scoping, tradeoff articulation |
| System design intuition | Transfers directly to GenAI architecture decisions |

### Gaps to Close

| Gap | Priority | Addressed In |
|---|---|---|
| Python fluency for AI/ML | High | Week 2 |
| ML/DL fundamentals (transformers, embeddings) | High | Weeks 1, 4 |
| Prompt engineering depth | High | Week 3 |
| Evaluation methodology | High | Week 7 |
| MLOps / model serving | Medium | Week 11 |
| Fine-tuning | Medium | Week 13 |
| Research paper reading | Low | Continuous |

---

## Continuous Tracks (Run Alongside Weekly Topics)

These are not separate weeks -- they run in parallel, every week.

### System Design Track (2 hrs/week)

Pick one GenAI system each week and sketch its architecture on paper or in Excalidraw. Examples: ChatGPT-like app, document Q&A pipeline, code review agent, customer support bot, content moderation system. Write a 1-page design doc covering: components, data flow, failure modes, scaling considerations.

### Writing Track (1 hr/week)

Write one short post (LinkedIn, blog, or internal doc) per week about something you learned. This builds your public profile and forces you to clarify your understanding. Topics come naturally from whatever you studied that week.

### DECISIONS.md Practice

Every project gets a `DECISIONS.md` file. Format:

```
## [Decision Title]
**Date:** YYYY-MM-DD
**Context:** What problem were you solving?
**Options considered:** List 2-3 alternatives
**Decision:** What you chose
**Rationale:** Why
**Tradeoffs:** What you gave up
```

---

## Month 1: Foundations (Weeks 1-4)

*Goal: Build rock-solid fundamentals. Understand what LLMs actually do, get fluent in Python for AI, master prompt engineering, and grok embeddings.*

### Week 1: LLM Fundamentals
[./month-1/week-01-llm-fundamentals.md](./month-1/week-01-llm-fundamentals.md)

- [ ] How LLMs work: pretraining, the prediction loop, sampling strategies
- [ ] Transformer architecture: attention mechanism, encoder-decoder vs decoder-only
- [ ] Tokenization and BPE: how text becomes numbers
- [ ] Alignment: RLHF, instruction tuning, safety training
- [ ] Inference: temperature, top-p, top-k, context windows

**Deliverables:**
- [ ] Written summary: "How an LLM goes from prompt to response" (1-2 pages)
- [ ] Tokenizer exploration notebook (compare tiktoken across models)
- [ ] Architecture diagram: transformer data flow

---

### Week 2: Python for AI + Pydantic
[./month-1/week-02-python-for-ai.md](./month-1/week-02-python-for-ai.md)

- [ ] Python environment setup: uv, virtual environments, project structure
- [ ] Core libraries: typing, dataclasses, asyncio patterns
- [ ] Pydantic v2: models, validators, serialization (critical for structured LLM output)
- [ ] Jupyter/Colab workflow for experimentation
- [ ] Build, don't just learn: every concept gets a working script

**Deliverables:**
- [ ] Pydantic models for structured LLM responses (at least 3 schemas)
- [ ] Async API caller utility (reusable in future projects)
- [ ] Python project template with proper structure, linting, typing

---

### Week 3: LLM APIs + Prompt Engineering
[./month-1/week-03-llm-apis-prompt-engineering.md](./month-1/week-03-llm-apis-prompt-engineering.md)

- [ ] OpenAI and Anthropic APIs: chat completions, system prompts, tool use
- [ ] Prompt patterns: few-shot, chain-of-thought, structured output, role prompting
- [ ] Prompt testing: writing assertions against LLM output
- [ ] Cost and latency: token counting, model selection tradeoffs
- [ ] Streaming responses and error handling

**Deliverables:**
- [ ] Prompt library: 10+ tested prompts with documented performance
- [ ] CLI tool that takes a task description and runs it through multiple prompt strategies
- [ ] Cost calculator utility

---

### Week 4: Embeddings + Vector Search
[./month-1/week-04-embeddings-vector-search.md](./month-1/week-04-embeddings-vector-search.md)

- [ ] What embeddings are: geometric intuition, similarity metrics (cosine, dot product)
- [ ] Embedding models: OpenAI, Cohere, open-source (sentence-transformers)
- [ ] Vector databases: Pinecone, Chroma, pgvector -- when to use which
- [ ] Chunking strategies: fixed-size, semantic, recursive
- [ ] Hybrid search: combining dense and sparse retrieval

**Deliverables:**
- [ ] Semantic search engine over a personal document corpus
- [ ] Chunking comparison notebook (same corpus, different strategies, measured recall)
- [ ] DECISIONS.md: vector DB choice rationale

**Month 1 Capstone:** Mini RAG chatbot over your own documents (combines Weeks 1-4)

---

## Month 2: RAG + Evals (Weeks 5-8)

*Goal: Build production-quality RAG systems and learn to evaluate them rigorously.*

### Week 5: RAG Architecture
[./month-2/week-05-rag-architecture.md](./month-2/week-05-rag-architecture.md)

- [ ] RAG pipeline end-to-end: ingest, chunk, embed, store, retrieve, generate
- [ ] Retrieval patterns: naive, reranking, query expansion, HyDE
- [ ] Document processing: PDFs, HTML, structured data
- [ ] Metadata filtering and hybrid retrieval
- [ ] Common failure modes and how to debug them

**Deliverables:**
- [ ] Production RAG pipeline with configurable retrieval strategies
- [ ] Retrieval quality benchmark (precision/recall on test queries)

---

### Week 6: LangGraph + Advanced RAG
[./month-2/week-06-langgraph-advanced-rag.md](./month-2/week-06-langgraph-advanced-rag.md)

- [ ] LangGraph fundamentals: nodes, edges, state, conditional routing
- [ ] Corrective RAG: detect bad retrievals, self-correct
- [ ] Adaptive RAG: route queries to different retrieval strategies
- [ ] Multi-step reasoning chains with state management
- [ ] When to use a framework vs. when to build from scratch

**Deliverables:**
- [ ] Corrective RAG system with LangGraph (auto-detects and fixes bad retrievals)
- [ ] Architecture comparison: framework vs. hand-rolled pipeline

---

### Week 7: Evals + Observability
[./month-2/week-07-evals-observability.md](./month-2/week-07-evals-observability.md)

- [ ] Why evals matter: the case for measuring everything
- [ ] Ragas framework: faithfulness, answer relevancy, context precision/recall
- [ ] Langfuse: tracing, scoring, prompt management, cost tracking
- [ ] Building custom evals: task-specific metrics, LLM-as-judge patterns
- [ ] Regression testing for prompts and pipelines

**Deliverables:**
- [ ] Eval suite for your RAG pipeline (Ragas + custom metrics)
- [ ] Langfuse integration with trace visualization
- [ ] Eval dashboard showing quality trends over iterations

---

### Week 8: RAG Capstone
[./month-2/week-08-rag-capstone.md](./month-2/week-08-rag-capstone.md)

- [ ] Full production RAG system: real dataset, real users (even if just you)
- [ ] Complete eval pipeline with Ragas and Langfuse
- [ ] Frontend UI (leverage your React skills)
- [ ] DECISIONS.md with all architectural choices documented

**Deliverables:**
- [ ] Deployed RAG application with eval dashboard
- [ ] Technical writeup / blog post
- [ ] Portfolio-ready demo

---

## Month 3: Agents + Production (Weeks 9-12)

*Goal: Build autonomous agents, understand MCP, and learn production deployment.*

### Week 9: Agent Fundamentals
[./month-3/week-09-agent-fundamentals.md](./month-3/week-09-agent-fundamentals.md)

- [ ] What agents are: the ReAct loop, tool use, planning
- [ ] Tool/function calling: OpenAI and Anthropic patterns
- [ ] Agent memory: short-term (conversation), long-term (vector store)
- [ ] Error handling and graceful degradation
- [ ] Safety: guardrails, output validation, human-in-the-loop

**Deliverables:**
- [ ] Research agent that searches, synthesizes, and cites sources
- [ ] Tool library: file I/O, web search, calculator, code execution

---

### Week 10: Multi-Agent Systems + MCP
[./month-3/week-10-multi-agent-mcp.md](./month-3/week-10-multi-agent-mcp.md)

- [ ] Multi-agent patterns: supervisor, collaborative, hierarchical
- [ ] Building multi-agent systems with LangGraph (not CrewAI)
- [ ] Model Context Protocol (MCP): architecture, servers, clients, tool exposure
- [ ] Building MCP servers and integrating with Claude/other clients
- [ ] When multi-agent is overkill vs. when it is necessary

**Deliverables:**
- [ ] Multi-agent system (e.g., research + writing + review agents)
- [ ] Custom MCP server exposing your own tools
- [ ] DECISIONS.md: single-agent vs. multi-agent tradeoff analysis

---

### Week 11: Production Infrastructure
[./month-3/week-11-production-infra.md](./month-3/week-11-production-infra.md)

- [ ] Deployment: FastAPI/LitServe, Docker, cloud options (AWS/GCP)
- [ ] Caching strategies: semantic cache, prompt cache
- [ ] Rate limiting, cost controls, token budgets
- [ ] Monitoring and alerting for LLM applications
- [ ] Security: prompt injection defense, PII handling, access control

**Deliverables:**
- [ ] Dockerized GenAI API with health checks, logging, rate limiting
- [ ] Cost monitoring dashboard
- [ ] Security checklist for LLM applications

---

### Week 12: Agentic Capstone
[./month-3/week-12-agentic-capstone.md](./month-3/week-12-agentic-capstone.md)

- [ ] Full agentic system: multi-agent with MCP integration
- [ ] Production deployment with monitoring
- [ ] Complete eval suite
- [ ] DECISIONS.md documenting all choices

**Deliverables:**
- [ ] Deployed multi-agent application
- [ ] Technical blog post / demo video
- [ ] Portfolio-ready project

---

## Month 4: Specialization + Job Hunt (Weeks 13-16)

*Goal: Add advanced skills (fine-tuning, multimodal), prepare for interviews, and start the job search.*

### Week 13: Fine-Tuning + Advanced Topics
[./month-4/week-13-fine-tuning-advanced.md](./month-4/week-13-fine-tuning-advanced.md)

- [ ] When to fine-tune vs. prompt engineer vs. RAG
- [ ] QLoRA: parameter-efficient fine-tuning on consumer hardware
- [ ] Dataset preparation and quality
- [ ] Evaluation of fine-tuned models
- [ ] Hugging Face ecosystem: Transformers, PEFT, datasets

**Deliverables:**
- [ ] Fine-tuned model for a specific task (e.g., domain-specific classifier)
- [ ] Comparison: base model vs. fine-tuned vs. RAG for same task
- [ ] DECISIONS.md: fine-tuning decision framework

---

### Week 14: Multimodal + Portfolio Polish
[./month-4/week-14-multimodal-portfolio.md](./month-4/week-14-multimodal-portfolio.md)

- [ ] Vision models: GPT-4V, Claude vision, open-source options
- [ ] Multimodal RAG: images + text retrieval and generation
- [ ] Audio/speech: Whisper, TTS APIs
- [ ] Portfolio review: clean up all projects, READMEs, demos
- [ ] GitHub profile optimization

**Deliverables:**
- [ ] Multimodal project (e.g., image + text Q&A system)
- [ ] Polished portfolio with 4 capstone projects
- [ ] Updated GitHub profile and README

---

### Week 15: Interview Preparation
[./month-4/week-15-interview-prep.md](./month-4/week-15-interview-prep.md)

- [ ] GenAI system design interview patterns
- [ ] Common technical questions and answers
- [ ] Behavioral stories mapped to GenAI projects
- [ ] Mock interviews (peer or AI-assisted)
- [ ] Salary research and negotiation preparation

**Deliverables:**
- [ ] System design answer templates for 5 common GenAI scenarios
- [ ] Technical cheat sheet: key concepts, metrics, tradeoffs
- [ ] 5 STAR-format stories from your GenAI projects

---

### Week 16: Job Hunt Launch
[./month-4/week-16-job-hunt.md](./month-4/week-16-job-hunt.md)

- [ ] Resume tailored to GenAI Engineer / Architect roles
- [ ] LinkedIn optimization with GenAI content
- [ ] Target company list with role-specific application strategy
- [ ] Networking: communities, meetups, open-source contributions
- [ ] Continued learning plan post-roadmap

**Deliverables:**
- [ ] Tailored resume and cover letter templates
- [ ] 10+ targeted applications submitted
- [ ] 30-day post-roadmap learning plan

---

## Capstone Projects Summary

| Month | Project | Key Skills Demonstrated | Evals Included |
|---|---|---|---|
| 1 | Mini RAG Chatbot | Embeddings, vector search, LLM APIs, prompt engineering | Basic retrieval metrics |
| 2 | Production RAG System | Advanced RAG, LangGraph, Ragas, Langfuse, React frontend | Full Ragas + Langfuse suite |
| 3 | Multi-Agent + MCP System | Agent design, multi-agent orchestration, MCP, deployment | Agent task completion evals |
| 4 | Portfolio (4 projects polished) | Fine-tuning, multimodal, system design, production readiness | Per-project eval suites |

---

## Self-Assessment Rubric

Rate yourself 1-5 at Week 0, Week 8, and Week 16. Be honest -- this is for you, not an interviewer.

| Skill | Week 0 | Week 8 | Week 16 |
|---|---|---|---|
| Explain how transformers work to a non-technical PM | _ / 5 | _ / 5 | _ / 5 |
| Build a RAG pipeline from scratch (no framework) | _ / 5 | _ / 5 | _ / 5 |
| Evaluate a RAG system with quantitative metrics | _ / 5 | _ / 5 | _ / 5 |
| Design a GenAI system architecture on a whiteboard | _ / 5 | _ / 5 | _ / 5 |
| Debug a retrieval failure in production | _ / 5 | _ / 5 | _ / 5 |
| Build and deploy an agent with tool use | _ / 5 | _ / 5 | _ / 5 |
| Write a DECISIONS.md that a senior engineer would respect | _ / 5 | _ / 5 | _ / 5 |
| Explain tradeoffs: fine-tuning vs. RAG vs. prompt engineering | _ / 5 | _ / 5 | _ / 5 |
| Ship a GenAI project end-to-end (idea to deployed demo) | _ / 5 | _ / 5 | _ / 5 |
| Read and extract key ideas from an AI research paper | _ / 5 | _ / 5 | _ / 5 |

---

## Anti-Patterns to Avoid

These are traps that derail GenAI learning. Revisit this list when you feel stuck.

1. **Framework tourism.** Trying LangChain, LlamaIndex, CrewAI, AutoGen, and Semantic Kernel in the same month. Pick one (LangGraph), go deep, then branch out only when a real project demands it.

2. **Tutorial purgatory.** Watching 40 hours of YouTube without building anything. Every concept gets a working script within 24 hours of learning it.

3. **Skipping evals.** Building a "cool demo" without any way to measure if it actually works. Evals are not optional -- they are the difference between a toy and a product.

4. **Premature optimization.** Spending a week on caching and deployment before your retrieval quality is good. Fix the AI first, then optimize the infrastructure.

5. **Ignoring fundamentals.** Jumping to agents without understanding embeddings, or to fine-tuning without understanding prompting. The stack builds on itself.

6. **Collecting certificates instead of projects.** A portfolio of shipped projects beats a wall of certificates. Employers hire builders.

7. **Building in isolation.** Not writing about what you learn, not sharing projects, not getting feedback. The writing track and DECISIONS.md practice exist to prevent this.

8. **Chasing every new release.** A new model drops every week. Stay focused on your current week's topic. Note interesting releases in a "to explore later" list.

---

## Merge Notes

This roadmap was created by merging two complementary approaches:

- **Roadmap A:** Strategy-focused, emphasizing evals, shipping cadence, DECISIONS.md practice, and professional habits
- **Roadmap B:** Lesson-granular, with detailed technical topics per week and comprehensive LLM fundamentals

### Added from Roadmap A
- Evals track with Ragas and Langfuse (Week 7 is a dedicated evals week; B had no evals coverage)
- Continuous system design track (2 hrs/week architectural sketching)
- Continuous writing track (1 hr/week public writing)
- DECISIONS.md practice in every project
- Self-assessment rubric for progress tracking
- Anti-patterns section to avoid common traps
- Design principles (evals-first, ship monthly, write tradeoffs)

### Added from Roadmap A (Topics)
- MCP (Model Context Protocol) as a major Month 3 topic (Week 10)

### Kept from Roadmap B
- Detailed LLM fundamentals: transformer architecture, tokenization/BPE, embeddings, alignment, inference parameters
- Dedicated Python for AI week (Week 2) with Pydantic
- Fine-tuning coverage with QLoRA (moved to Week 13)
- Multimodal coverage: vision models, audio, multimodal RAG (moved to Week 14)
- Granular topic breakdowns within each week

### Removed from Roadmap B
- **CrewAI** -- replaced by building lightweight multi-agent systems directly with LangGraph. CrewAI adds abstraction without proportional value at this learning stage.
- **LiteLLM** -- minor utility tool. Learn it if a project needs it, but not worth dedicated study time.
- **NumPy deep-dive** -- trimmed to minimal coverage. Just enough linear algebra intuition for understanding embeddings (cosine similarity, dot products), covered within Week 4.

### Restructured
- Week 2 is now Python for AI + Pydantic (from B) merged with A's "build don't just learn" ethos -- every concept gets a working script
- Week 7 is now a dedicated Evals + Observability week (from A; B had no standalone evals coverage)
- Fine-tuning moved from earlier in B to Week 13 (after production fundamentals are solid)
- Multimodal moved from earlier in B to Week 14 (specialization after core skills)
