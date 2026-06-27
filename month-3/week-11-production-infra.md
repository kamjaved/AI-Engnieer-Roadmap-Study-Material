# Week 11: Production Infrastructure

> **Month 3 -- Agents, MCP & Production Infra**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 10](./week-10-multi-agent-mcp.md) | Next: [Week 12](./week-12-agentic-capstone.md)

---

## Overview

This week converts your AI projects from "works on my laptop" to production-ready services. You will learn Docker for AI apps, production FastAPI patterns, cloud deployment, CI/CD with GitHub Actions, and cost/latency optimization techniques. Your existing fullstack deployment experience transfers directly -- this week is about applying it to AI-specific challenges.

---

## Lesson 1: Docker for AI Apps

**Sub-topics:**
- Multi-stage builds (separate build and runtime stages)
- Python dependency management in Docker (uv, pip-compile)
- GPU considerations (NVIDIA runtime, CUDA base images)
- Image size optimization (slim bases, layer caching)
- Docker Compose for multi-service AI stacks (API + vector DB + Redis)
- Health checks for AI services

**Key Concepts:**

AI applications have unique Docker challenges: large dependencies (PyTorch, transformers), model files that bloat images, and optional GPU requirements. Multi-stage builds are essential: use a build stage to install dependencies and a slim runtime stage that copies only what is needed. Pin all dependencies with a lockfile (uv.lock or requirements.txt from pip-compile) for reproducible builds.

For development, Docker Compose ties your services together: a FastAPI app, a vector database (Chroma or pgvector), Redis for caching, and Langfuse for tracing. Define health checks that verify not just "the container is running" but "the model is loaded and can respond to queries." For GPU inference, use NVIDIA's CUDA base images and the nvidia-docker runtime, though for most GenAI applications that call external APIs, GPU is not needed in the container.

**Interview Questions:**

1. *How do you optimize Docker images for AI applications?*
   Use multi-stage builds to separate build dependencies from runtime. Use slim base images (python:3.11-slim). Pin dependencies with lockfiles. Leverage layer caching by installing dependencies before copying application code. Exclude model files from the image if using API-based inference. Target under 500MB for API-calling services.

2. *When do you need GPU support in a Docker container for AI?*
   Only when running local model inference (not API calls). If you call OpenAI/Anthropic APIs, you do not need GPU. If you run a local embedding model, reranker, or fine-tuned model, you need the NVIDIA runtime with CUDA base images.

---

## Lesson 2: FastAPI Production Setup

**Sub-topics:**
- SSE (Server-Sent Events) streaming for LLM responses
- Middleware: CORS, request logging, error handling, authentication
- Background tasks for async processing (ingestion, eval runs)
- Dependency injection for database connections and model clients
- Request/response validation with Pydantic
- Error handling patterns for LLM-specific failures (rate limits, timeouts, content filters)

**Key Concepts:**

FastAPI is the standard for Python AI APIs. For LLM applications, streaming is critical: use SSE to push tokens to the frontend as they are generated. Implement this with `StreamingResponse` and an async generator that yields tokens from the LLM. Your middleware stack should include: CORS (for frontend access), request ID generation (for Langfuse trace correlation), authentication (API key or JWT), rate limiting, and structured error handling.

LLM-specific error handling is often overlooked. You need to handle: rate limit errors (429) with exponential backoff, timeout errors when the LLM is slow, content filter rejections (the LLM refuses to answer), and unexpected output format (the LLM does not follow your structured output schema). Each of these should return a meaningful error response to the client rather than a generic 500.

**Interview Questions:**

1. *How do you implement streaming LLM responses in FastAPI?*
   Use an async generator function that yields tokens from the LLM client's streaming API. Wrap it in a `StreamingResponse` with `media_type="text/event-stream"`. Each yield sends an SSE event to the client. Include error handling in the generator for mid-stream failures.

2. *What LLM-specific errors must a production API handle?*
   Rate limiting (429, retry with backoff), timeouts (LLM slow or down), content filtering (model refuses the request), malformed output (model does not follow schema), context length exceeded (input too long), and cost budget exceeded. Each needs a specific error response and recovery strategy.

---

## Lesson 3: Cloud Deployment

**Sub-topics:**
- Railway: deployment from Dockerfile, env vars, auto-scaling
- Render: free tier limitations, background workers
- Fly.io: edge deployment, persistent volumes
- Choosing between platforms (cost, complexity, scaling)
- Custom domains and SSL
- Environment variable management for API keys

**Key Concepts:**

For portfolio projects and early production, Railway and Render offer the best developer experience with free or cheap tiers. Railway deploys directly from a Dockerfile with zero configuration -- push to GitHub and it builds and deploys. Render has a generous free tier but suspends inactive services (cold starts of 30-60 seconds).

The deployment flow: connect your GitHub repo to the platform, configure environment variables (LLM API keys, database URLs, Langfuse keys), set up a custom domain, and enable auto-deploy on push to main. For AI applications specifically, watch out for: cold start latency (pre-load models on startup, not on first request), memory limits (vector databases can be memory-hungry), and timeout limits (some platforms kill requests after 30 seconds, which may not be enough for agent loops).

**Interview Questions:**

1. *What are the key concerns when deploying an AI application to the cloud?*
   Cold start latency (pre-warm models), memory usage (vector stores, model weights), request timeouts (agent loops can take 30+ seconds), API key management (never in code), cost monitoring (LLM API costs can spike), and rate limiting (protect against abuse that runs up your API bill).

---

## Lesson 4: GitHub Actions CI/CD

**Sub-topics:**
- CI pipeline: lint, type check, unit tests, eval suite
- CD pipeline: build Docker image, deploy to cloud
- Running evals in CI (gate deployment on quality metrics)
- Secrets management in GitHub Actions
- Caching strategies for faster CI (dependency caching, Docker layer caching)
- Branch protection rules for AI projects

**Key Concepts:**

Your CI pipeline should run on every push: lint (ruff), type check (mypy), unit tests, and -- critically for AI projects -- your eval suite. Gate deployments on eval results: if faithfulness drops below 0.85 or any metric regresses more than 5%, the pipeline fails and deployment is blocked. This prevents shipping quality regressions.

The CD pipeline builds a Docker image, pushes it to a registry, and triggers a deployment on your cloud platform. Use GitHub Actions secrets for API keys (never hardcode them). Cache pip dependencies and Docker layers aggressively -- AI dependencies are large and slow to install.

**Interview Questions:**

1. *How do you integrate evals into CI/CD?*
   Add an eval step in GitHub Actions that runs your RAGAS eval suite against a golden dataset. Parse the results and compare against stored baseline scores. Fail the pipeline if any metric drops below the threshold. Store eval results as artifacts for historical tracking. This gates every deployment on quality.

2. *What should a CI pipeline for a GenAI application include?*
   Linting (ruff), type checking (mypy), unit tests for non-LLM code, integration tests for tool functions, the eval suite with quality thresholds, cost estimation for the eval run (it makes real LLM calls), and Docker image build verification.

---

## Lesson 5: Secrets Management, Twelve-Factor, and Security

**Sub-topics:**
- Twelve-Factor App principles applied to AI apps
- Environment variables for configuration
- Secret management: .env files, platform secrets, vaults
- Prompt injection defense (input sanitization, output validation)
- PII handling in logs and traces
- API key rotation and access control

**Key Concepts:**

The Twelve-Factor App methodology applies directly to AI services. Key principles: store config in environment variables (never in code), treat backing services (vector DB, Redis, LLM APIs) as attached resources, keep build/release/run stages separate, and export services via port binding. For AI apps specifically, add: manage prompt versions as config (not hardcoded), track eval baselines as release artifacts, and log every LLM interaction for debugging.

Security for AI applications has unique concerns. Prompt injection is the biggest threat: malicious users craft inputs that override your system prompt. Defense requires input sanitization (detect and filter injection patterns), output validation (verify the response follows expected format), and architectural patterns (do not include user input verbatim in system prompts). Also ensure PII is redacted from logs and Langfuse traces -- these are often overlooked vectors for data leakage.

**Interview Questions:**

1. *How do you defend against prompt injection in production?*
   Layer multiple defenses: input sanitization (pattern matching for common injection phrases), separate user input from system instructions architecturally, output validation (verify format and content boundaries), LLM-based detection (use a classifier to flag suspicious inputs), and rate limiting per user. No single defense is sufficient; use defense in depth.

---

## Lesson 6: Rate Limiting, Caching, and Cost Optimization

**Sub-topics:**
- Rate limiting with Redis (token bucket, sliding window)
- Response caching: exact match and semantic cache
- Prompt caching (Anthropic and OpenAI prompt prefix caching)
- Model routing (use cheaper models for simple queries)
- Token optimization (shorter prompts, fewer retrieved chunks)
- Cost monitoring and alerting

**Key Concepts:**

AI application costs scale with usage in a way traditional apps do not -- every request makes paid API calls. Rate limiting protects your budget: use Redis-backed rate limiting (per user, per API key) to prevent abuse. A token bucket algorithm with 20 requests/minute for free users and 100/minute for paid is a common starting point.

For cost optimization, the biggest wins come from: prompt caching (Anthropic caches prompt prefixes, reducing cost for repeated system prompts by up to 90%), model routing (use GPT-4o-mini or Claude Haiku for simple classification/routing, and full models only for generation), semantic caching (return cached responses for similar queries), and reducing retrieved chunks (fewer chunks = fewer input tokens = lower cost). Track cost per query in Langfuse and set alerts for unexpected spikes.

**Interview Questions:**

1. *How do you optimize costs in a production GenAI application?*
   Prompt caching for repeated system prompts, model routing (cheaper models for simple tasks), semantic caching for frequent similar queries, reducing context window usage (fewer/smaller chunks), batching where possible, and setting per-user and per-query cost budgets. Monitor continuously with Langfuse or similar.

2. *Describe a model routing strategy for cost optimization.*
   Use a fast, cheap classifier (embedding similarity or small model) to categorize each query. Route simple factual lookups to GPT-4o-mini or Claude Haiku ($0.25/M tokens). Route complex reasoning, generation, or multi-step tasks to GPT-4o or Claude Sonnet ($3-5/M tokens). This can reduce average cost by 50-70% with minimal quality impact.

---

## Assignment: Dockerize, Deploy, and Harden

**Objective:** Dockerize your RAG app, deploy with CI/CD, add rate limiting and caching.

**Requirements:**
- Write a multi-stage Dockerfile for your Week 8 RAG capstone (or Week 9 agent)
- Create a Docker Compose file with: app + vector DB + Redis
- Set up GitHub Actions CI/CD: lint, type check, eval suite, deploy
- Gate deployment on eval scores (fail if any metric regresses >5%)
- Add Redis-backed rate limiting (configurable per user)
- Implement at least one caching strategy (exact match or semantic cache)
- Deploy to Railway or Render with environment variables managed properly

**Stretch goals:**
- Add model routing: use a cheap model for query classification, expensive model for generation
- Implement prompt caching with Anthropic's API
- Set up cost alerts that notify you when daily spend exceeds a threshold
- Add a health check endpoint that verifies LLM connectivity and vector DB status

---

## Summary Checklist

- [ ] Can write multi-stage Dockerfiles for AI applications
- [ ] Docker Compose running multi-service AI stack locally
- [ ] GitHub Actions CI/CD pipeline with eval gating
- [ ] Rate limiting implemented with Redis
- [ ] At least one caching strategy reducing costs
- [ ] Application deployed to Railway or Render with proper secrets management
- [ ] Understand prompt injection defense and PII handling
- [ ] Can articulate cost optimization strategies for GenAI apps
- [ ] Completed assignment: deployed, rate-limited, cached AI service with CI/CD
- [ ] System design sketch: scaling a RAG system to 1000 concurrent users
- [ ] Weekly writing: 1 post about production AI infrastructure or deployment lessons
