# Week 8: RAG Capstone (Project 2)

> **Month 2 -- RAG, Retrieval, Evals & Observability**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 7](./week-07-evals-observability.md) | Next: [Week 9](../month-3/week-09-agent-fundamentals.md)

---

## Overview

This is your second capstone -- a full production RAG system that demonstrates everything from Weeks 5-7. This project must be portfolio-ready: deployed, evaluated, observed, and documented. The deliverables include not just code but an EVALS.md showing your measurement methodology and a DECISIONS.md documenting every architectural choice.

---

## Lesson 1: Multi-Format Document Ingestion

**Sub-topics:**
- Unified ingestion pipeline for PDF, markdown, HTML, and plain text
- Document type detection and routing
- Metadata extraction and standardization across formats
- Handling large document collections (batching, progress tracking)
- Error handling and partial failure recovery

**Key Concepts:**

A production ingestion pipeline must handle any document your users throw at it. Build a format router: detect the file type, dispatch to the appropriate parser (PyMuPDF for PDFs, BeautifulSoup for HTML, markdown parser for .md), and normalize all output into a common schema: `{text, metadata: {source, page, section, format, date}}`. The common schema ensures your downstream chunking and embedding stages work identically regardless of source format.

Error handling is critical for production. A single malformed PDF should not crash the entire ingestion pipeline. Implement per-document try/catch with logging, and maintain a manifest of successfully processed vs failed documents. Users need to know what made it into the index.

**Interview Questions:**

1. *How do you design a document ingestion pipeline that handles multiple formats?*
   Use a format router that detects file types and dispatches to specialized parsers. Normalize output into a common schema with standardized metadata. Process documents in batches with per-document error handling. Maintain a manifest for tracking ingestion status.

2. *What happens when a document fails to parse in production?*
   Log the failure with document ID and error details, skip it, and continue processing. Maintain a failed-documents queue for retry or manual review. Never let a single bad document crash the pipeline or block other documents from being indexed.

---

## Lesson 2: Hybrid Search + Reranking + Citations

**Sub-topics:**
- Combining dense + sparse retrieval with RRF (from Week 5)
- Integrating cross-encoder reranking in the pipeline
- Citation extraction: mapping answer sentences to source chunks
- Citation formats: inline references, footnotes, source cards
- Deduplication of overlapping retrieved chunks

**Key Concepts:**

The retrieval stack for this capstone should be: BM25 + dense retrieval with RRF fusion, followed by cross-encoder reranking, followed by citation extraction. Citations are not just a nice feature -- they are a trust mechanism. Users need to verify that answers are grounded in real sources.

Citation extraction works by: (1) instructing the LLM to include [1], [2] style references in its answer, (2) mapping each reference to the source chunk's metadata (document name, page number, section), and (3) rendering these as clickable links or expandable source cards in the UI. For reliability, validate that the LLM's citations actually correspond to the provided chunks -- hallucinated citations are worse than no citations.

**Interview Questions:**

1. *How do you implement reliable citations in a RAG system?*
   Provide each retrieved chunk with a numbered reference in the prompt. Instruct the LLM to cite by number. Post-process the output to extract references and map them to source metadata. Validate that each cited number corresponds to a provided chunk. Display source cards with document name, page, and relevant excerpt.

---

## Lesson 3: React Streaming UI with Vercel AI SDK

**Sub-topics:**
- Vercel AI SDK overview (useChat hook, streaming responses)
- Server-Sent Events (SSE) from FastAPI backend
- Streaming token-by-token display
- Rendering citations alongside streaming answers
- Loading states, error handling, and retry UX
- Responsive design for the chat interface

**Key Concepts:**

Your React/TypeScript skills are a major advantage here. The Vercel AI SDK provides `useChat()` and `useCompletion()` hooks that handle streaming responses, message history, and error states out of the box. On the backend, your FastAPI endpoint yields tokens via Server-Sent Events (SSE).

The UX pattern: the user sends a query, a loading state shows retrieval is happening, then tokens stream in one-by-one. After the response completes, citation source cards appear below the answer. Each source card shows the document title, page/section, and a relevance score. Clicking a source card expands to show the relevant excerpt. This is the standard pattern used by Perplexity, ChatGPT with browsing, and other production RAG interfaces.

**Interview Questions:**

1. *How do you stream LLM responses to a frontend?*
   The backend uses Server-Sent Events (SSE) or WebSockets to push tokens as they are generated. The frontend uses a streaming client (like Vercel AI SDK's useChat hook) to render tokens incrementally. This gives the user immediate feedback instead of waiting for the full response.

---

## Lesson 4: RAGAS Eval Dashboard

**Sub-topics:**
- Automating eval runs on code changes
- Visualizing metric trends (faithfulness, relevancy, precision, recall)
- Per-category breakdown (factual vs multi-hop vs unanswerable)
- Comparison view: before/after a pipeline change
- Alert thresholds for metric degradation

**Key Concepts:**

Your eval harness from Week 7 becomes a continuous quality monitor. After every pipeline change, run the 30-question eval suite and log results. Build a simple Streamlit dashboard (or notebook) that shows: overall scores per metric, scores broken down by question category, and a time-series view showing how metrics change across iterations.

The comparison view is particularly valuable: when you change the chunking strategy or swap the reranker, you can see exactly which questions improved and which regressed. This turns optimization from guesswork into a data-driven process. Set alert thresholds -- if faithfulness drops below 0.85 or any metric drops more than 5% from the previous run, flag it for investigation before deploying.

**Interview Questions:**

1. *How do you prevent quality regression in a RAG system?*
   Run a standardized eval suite after every change. Track metrics over time in a dashboard. Set alert thresholds for metric drops. Use per-category breakdowns to catch regressions that are masked by overall averages. Gate deployments on eval scores meeting minimum thresholds.

---

## Lesson 5: Langfuse Tracing in Production

**Sub-topics:**
- Instrumenting every pipeline stage with @observe()
- Custom scores: attaching eval scores to traces
- Cost tracking: per-query, per-user, per-day
- Identifying failure patterns from production traces
- Prompt versioning: linking prompt changes to quality changes

**Key Concepts:**

In production, Langfuse serves as your flight recorder. Every query gets a trace ID. Under that trace, you can see: which route the query took, what documents were retrieved (with scores), what the reranker changed, the exact prompt sent to the LLM, the raw response, latency per stage, and total cost. When a user reports a bad answer, you look up their trace and see exactly what went wrong.

Attaching eval scores to traces creates a powerful feedback loop. You can filter traces by low faithfulness scores and analyze what those queries have in common -- maybe they all involve a specific topic where your corpus is thin, or they all went through a particular routing path. This turns your observability system into a diagnostic tool.

**Interview Questions:**

1. *How does Langfuse help you debug a production RAG system?*
   Each query gets a full trace showing inputs and outputs at every pipeline stage. When a user reports a bad answer, you find their trace and inspect: were the retrieved documents relevant? Did the reranker help? Was the prompt appropriate? Was the LLM hallucinating despite good context? This pinpoints exactly which stage failed.

---

## Lesson 6: Deployment and Ship Checklist

**Sub-topics:**
- Deploying FastAPI backend (Railway or Render free tier)
- Deploying React frontend (Vercel)
- Environment variables and secrets management
- Health checks and basic monitoring
- Writing EVALS.md (methodology, metrics, baseline scores, known limitations)
- Writing DECISIONS.md (all architectural choices documented)

**Key Concepts:**

Shipping means more than "it works on localhost." Your capstone must be publicly accessible with a working URL. Deploy the FastAPI backend to Railway or Render (both have free tiers). Deploy the React frontend to Vercel. Connect them with proper CORS configuration and environment variables for API keys.

EVALS.md is your quality report card. Document: what metrics you track, your golden dataset composition, current baseline scores, known weaknesses (e.g., "multi-hop questions score 15% lower than factual queries"), and your improvement plan. DECISIONS.md captures every architectural choice: why you chose hybrid search over pure dense, why you picked a particular chunk size, why you chose Cohere Rerank over an open-source cross-encoder.

**Interview Questions:**

1. *What documentation should accompany a production RAG system?*
   EVALS.md (metrics, dataset, baseline scores, known weaknesses), DECISIONS.md (architectural choices with rationale), a README with setup instructions and architecture diagram, API documentation, and a runbook for common failure modes.

---

## Assignment: Full RAG System Capstone

**Objective:** Ship a complete, production-grade RAG system with eval harness, observability, and documentation.

**Must-ship deliverables:**
- Multi-format document ingestion (at least PDF + markdown)
- Hybrid search (dense + BM25) with cross-encoder reranking
- Citations in generated answers with source cards
- React streaming UI using Vercel AI SDK
- RAGAS eval suite (30+ questions, 4 core metrics)
- Langfuse tracing on all pipeline stages
- Deployed backend (Railway/Render) + frontend (Vercel)
- EVALS.md with methodology, baseline scores, and known limitations
- DECISIONS.md with all architectural choices

**Stretch goals:**
- Eval dashboard (Streamlit) showing metric trends
- Prompt versioning with A/B comparison
- Cost-per-query monitoring
- User feedback collection (thumbs up/down integrated into traces)

---

## Summary Checklist

- [ ] Multi-format ingestion pipeline working for 2+ formats
- [ ] Hybrid search + reranking producing measurably better results than naive retrieval
- [ ] Citations working reliably with source cards in the UI
- [ ] Streaming responses rendering in the React frontend
- [ ] RAGAS eval suite running with 30+ questions and 4 metrics
- [ ] Langfuse tracing capturing every pipeline stage
- [ ] Backend deployed and accessible at a public URL
- [ ] Frontend deployed and connected to backend
- [ ] EVALS.md written with methodology, scores, and honest assessment of weaknesses
- [ ] DECISIONS.md written with every architectural choice documented
- [ ] Portfolio-ready: someone can visit the URL, try it, and be impressed
- [ ] System design sketch: RAG system at 100x scale -- what changes?
- [ ] Weekly writing: 1 post about what you built, what you learned, or a specific technical challenge
