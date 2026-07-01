# Month 2 — GenAI Engineer Roadmap

**Goal:** Build production-grade RAG systems, master LangGraph orchestration, implement rigorous evals, and ship a portfolio-ready capstone with full observability.
**Duration:** 4 Weeks | 22 Lessons

---

## Overview

| Week   | Theme                        | Lessons   |
| ------ | ---------------------------- | --------- |
| Week 5 | RAG Architecture Patterns    | 5.1 – 5.5 |
| Week 6 | LangGraph & Advanced RAG     | 6.1 – 6.5 |
| Week 7 | Evals & Observability        | 7.1 – 7.6 |
| Week 8 | RAG Capstone                 | 8.1 – 8.6 |

---

## Label Info

- 🔴 Essential / Must Know
- 🟡 Important / Good to Know
- 🟢 Optional / Nice to Have

---

# Week 5 — RAG Architecture Patterns

**Estimated Time:** ~10–12 hours
**Goal:** Transition from basic retrieval to production RAG. Learn the full spectrum of RAG patterns, master chunking strategies with measurable tradeoffs, implement hybrid search, build real-world document pipelines, and understand re-ranking as a quality multiplier.

---

## Lesson 5.1: RAG Architecture Patterns 🔴 Essential

### Objective

Understand the four RAG architecture patterns — Naive, Advanced, Modular, and Agentic — and know which to apply for a given use case.

### Topics Covered

1. Naive RAG 🔴
2. Advanced RAG 🔴
3. Modular RAG 🟡
4. Agentic RAG 🔴
5. GraphRAG (Knowledge-Graph-Based Retrieval) 🟡
6. Choosing the Right Pattern 🔴

### Subtopics

1. Naive RAG 🔴
   - Linear pipeline: chunk → embed → retrieve top-k → generate
   - Limitations: query-document mismatch, noisy context, no synthesis across sources
   - When it breaks: ambiguous queries, multi-hop reasoning, large corpora
2. Advanced RAG 🔴
   - Pre-retrieval: query rewriting, query expansion
   - Post-retrieval: re-ranking, answer verification, citation extraction
   - Solves the quality ceiling of a single-pass pipeline
3. Modular RAG 🟡
   - Each stage is a swappable component: retriever, reranker, generator
   - Mix dense + sparse retrieval; swap rerankers without rewriting the pipeline
   - Enables independent benchmarking and optimization per stage
4. Agentic RAG 🔴
   - LLM decides when and how to retrieve (iterative retrieval)
   - Can search again with a refined query, skip retrieval, or combine multiple sources
   - Required for diverse queries and multi-hop reasoning
5. GraphRAG 🟡
   - Replaces (or augments) the flat vector index with a knowledge graph of entities and relationships
   - Ingestion extracts entities + relationships into a graph; retrieval is graph traversal, not just similarity search
   - Solves a failure mode vector search cannot: "these chunks are similar" vs "these entities are causally/structurally related"
   - Best for: multi-hop questions over interconnected data (org charts, legal precedent chains, supply chains, codebases)
   - Cost: ingestion is far more expensive (entity/relation extraction per document); only adopt when relationship queries are a real, measured part of your query distribution
6. Choosing the Right Pattern 🔴
   - Naive: simple corpus, straightforward factual queries, prototype phase
   - Advanced: production, quality matters, queries are varied
   - Modular: team is optimizing individual components separately
   - Agentic: queries require dynamic decision-making about retrieval strategy
   - GraphRAG: queries require reasoning over relationships between entities, not just topical similarity
   - In production, these are not mutually exclusive — Adaptive RAG (Lesson 6.3) routes each query to the cheapest pattern that can answer it

---

### Key Concepts That Need to Understand During This Lesson

- Naive RAG failure modes: context pollution, hallucination from insufficient context, single-pass limitation
- Advanced RAG's two-stage improvement: before and after retrieval
- Modular RAG as the architecture for teams that A/B test pipeline components
- Agentic RAG as the foundation for any system where the LLM drives the retrieval loop
- GraphRAG as the answer when the failure mode is relational, not topical — vector search can't tell you two entities are connected, only that two chunks are similar
- The progression: Naive → Advanced → Modular → Agentic/GraphRAG reflects increasing engineering maturity, but each step also adds cost and complexity — only climb the ladder as far as your measured failure modes require

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between Naive RAG and Advanced RAG?
2. What are the failure modes of Naive RAG?
3. When would you choose Agentic RAG over a static pipeline?

**Intermediate Questions**

1. Design a RAG system for a customer support tool serving 50K queries/day. Which pattern do you start with and how does it evolve?
2. How does Modular RAG enable independent optimization of pipeline components?
3. What is the risk of using Agentic RAG in a latency-sensitive production system?
4. A user asks "How are these three vendors connected to our supply chain disruptions?" Why does standard vector RAG struggle with this, and how does GraphRAG address it?

---

## Lesson 5.2: Chunking Strategies Deep Dive 🔴 Essential

### Objective

Master the full range of chunking strategies, understand their tradeoffs, and know how to measure which is best for a given corpus.

### Topics Covered

1. Fixed-Size Chunking 🔴
2. Recursive Chunking 🔴
3. Semantic Chunking 🟡
4. Parent-Child Chunking 🔴
5. Hierarchical Chunking 🟡
6. Contextual Retrieval (Anthropic) 🔴
7. Chunk Size Tradeoffs 🔴

### Subtopics

1. Fixed-Size Chunking 🔴
   - Character or token count with configurable overlap
   - Simple but breaks semantic boundaries mid-thought
   - Example: 512 tokens, 128-token overlap
2. Recursive Chunking 🔴
   - Splits on natural structure: paragraphs → sentences → characters
   - Respects document boundaries before falling back to fixed-size
   - Production default: 400–600 tokens, 10–15% overlap
3. Semantic Chunking 🟡
   - Uses embedding similarity between consecutive sentences to detect topic shifts
   - Creates chunks that are topically coherent
   - More expensive to compute; useful when document structure is poor
4. Parent-Child Chunking 🔴
   - Embed small child chunks (e.g., 200 tokens) for precise retrieval
   - When a child matches, return its parent chunk (e.g., 1000 tokens) to the LLM
   - Solves the retrieval-precision vs generation-context tension
5. Hierarchical Chunking 🟡
   - Document > Section > Paragraph levels with metadata at each level
   - Filter by section header or doc structure before vector search
   - Useful when documents have strong semantic hierarchy (legal docs, technical manuals)
6. Contextual Retrieval 🔴
   - Anthropic technique (Sept 2024): before embedding, prepend a short LLM-generated context blurb to each chunk explaining where it sits in the larger document
   - Example: prepend "This chunk is from Q3 2024's earnings report, discussing ACME Corp's revenue growth" before the raw chunk text
   - Apply the same contextualization to the BM25 index, not just the embedding — Anthropic reports this combination (contextual embeddings + contextual BM25) cuts retrieval failures by roughly 49%
   - Cost: one extra LLM call per chunk at ingestion time; mitigate with prompt caching (the whole document is the cached prefix, only the chunk-specific instruction varies)
   - Use when: chunks lose critical context when isolated (e.g., "the company's revenue grew 3% over the previous quarter" with no company name in the chunk itself)
7. Chunk Size Tradeoffs 🔴
   - Small chunks: higher retrieval precision, less generation context
   - Large chunks: more context for generation, diluted embedding signal
   - Large chunks also consume more context window and cost more
   - Rule: start with recursive at 512 tokens; measure Precision@5 before tuning

---

### Key Concepts That Need to Understand During This Lesson

- Chunking is the single highest-impact decision in a RAG pipeline
- Semantic boundaries matter more than token count boundaries
- Parent-child chunking as the production solution to the precision/context tradeoff
- Why large chunks hurt retrieval: embedding becomes a poor signal for a multi-topic chunk
- Contextual Retrieval as the 2026 high-ROI upgrade to any chunking strategy: it doesn't replace fixed/recursive/semantic chunking, it makes whichever one you pick more accurate by re-attaching document-level context before embedding
- Always measure: implement 3 strategies, evaluate on a golden set, pick the winner

---

### Hands-on Exercises

- Implement fixed-size (512 tokens, 128 overlap), recursive (by paragraph/sentence), and semantic chunking on the same corpus
- Create 15 test queries with known relevant passages; measure Precision@5 and Recall@5 for each strategy
- Write a DECISIONS.md entry for which strategy won and why

### Assignment

📄 Assignment File: `assignments/w05-a1-chunking-strategy-comparison.md`

Short description: Build 3 chunking strategies, embed with the same model, measure retrieval precision on a 15-question golden set, document your decision.

---

### Interview Preparation

**Beginner Questions**

1. Why not just use large chunks to give the LLM more context?
2. Explain the parent-child chunking strategy.
3. What is recursive chunking and how does it differ from fixed-size?

**Intermediate Questions**

1. Compare fixed-size, recursive, and semantic chunking. When would you use each?
2. You are building RAG over legal contracts (highly structured). Which chunking strategy do you choose?
3. How would you measure whether your chunking strategy is actually good?
4. What is Anthropic's Contextual Retrieval technique, and why does it help even a well-tuned recursive chunking pipeline?

---

## Lesson 5.3: Hybrid Search 🔴 Essential

### Objective

Understand why dense retrieval alone is insufficient, how BM25 complements it, and how to combine both with Reciprocal Rank Fusion.

### Topics Covered

1. Dense Retrieval Strengths and Weaknesses 🔴
2. Sparse Retrieval — BM25 / TF-IDF 🔴
3. Reciprocal Rank Fusion (RRF) 🔴
4. When Hybrid Outperforms Pure Dense 🔴
5. Implementation (rank_bm25 + vector DB) 🟡

### Subtopics

1. Dense Retrieval 🔴
   - Strengths: semantic similarity, understands synonyms and paraphrases
   - Weaknesses: struggles with exact keywords, rare terms, structured identifiers
   - Example failure: searching for error code `ERR_CONNECTION_RESET`
2. Sparse Retrieval — BM25 🔴
   - Exact lexical matching with term frequency weighting
   - Handles: product codes, error messages, domain-specific jargon, proper nouns
   - No embeddings required; fast and zero-shot applicable
3. Reciprocal Rank Fusion (RRF) 🔴
   - Merge dense and sparse result lists by rank position
   - Formula: RRF score = Σ 1/(k + rank_i) where k=60 is standard
   - Weights items higher if they rank well in multiple lists
4. When Hybrid Wins 🔴
   - Heterogeneous corpora where some queries are keyword-heavy
   - Typical improvement: 5–15% recall gain over either approach alone
   - Start: 70% vector / 30% keyword blend
5. Implementation 🟡
   - `rank_bm25` library for BM25 scoring
   - Run both retrievers in parallel; merge with RRF
   - pgvector supports hybrid natively; ChromaDB does not

---

### Key Concepts That Need to Understand During This Lesson

- Dense and sparse are complementary, not competing
- BM25 as the zero-shot baseline that dense retrieval must beat
- RRF as the standard merge algorithm (no tunable weights needed to start)
- Hybrid as the production default: it consistently outperforms either alone
- When to tune the vector/keyword ratio: measure on your eval set, don't guess

---

### Interview Preparation

**Beginner Questions**

1. What is BM25 and how does it differ from vector similarity search?
2. When does BM25 outperform dense retrieval?
3. What is Reciprocal Rank Fusion?

**Intermediate Questions**

1. Design a hybrid search system. How do you determine the balance between vector and keyword search?
2. A user searches for a specific API error code. Why does pure dense retrieval fail and how does hybrid fix it?
3. How would you implement hybrid search with pgvector in production?

---

## Lesson 5.4: Document Processing Pipelines 🟡 Important

### Objective

Build robust ingestion pipelines that handle real-world document formats: PDFs with tables, HTML, markdown, and mixed-format corpora.

### Topics Covered

1. PDF Extraction (PyMuPDF, pdfplumber, Unstructured) 🟡
2. Markdown and HTML Parsing 🟡
3. Table Extraction and Structured Data 🟡
4. Image and Diagram Handling 🟢
5. Metadata Extraction 🔴
6. Handling Messy Real-World Documents 🟡

### Subtopics

1. PDF Extraction 🟡
   - PyMuPDF: fast, good for clean PDFs
   - pdfplumber: better table detection
   - Unstructured: best for multi-format ingestion; detects element types (titles, text, tables, images)
   - Common issues: headers/footers polluting text, cross-page tables
2. Markdown and HTML Parsing 🟡
   - Markdown: preserve heading hierarchy as metadata
   - HTML: BeautifulSoup to extract visible text, strip nav/footer boilerplate
   - Preserve section titles as chunk metadata
3. Table Extraction 🟡
   - Serialize as markdown for general Q&A
   - Extract as structured JSON for programmatic lookups
   - Use vision model description for complex tables with merged cells
4. Image and Diagram Handling 🟢
   - OCR (tesseract) for text-in-images
   - GPT-4o / Claude vision to generate natural language description for embedding
   - Store image path in metadata; embed the description
5. Metadata Extraction 🔴
   - Required fields: source, page/section, date, document type, access_control
   - Metadata enables pre-filtering before vector search
   - Critical for citation generation and debugging
6. Handling Messy Documents 🟡
   - Per-document try/catch with logging — one bad PDF must not crash the pipeline
   - Maintain a manifest of successfully processed vs failed documents
   - Failed-document queue for retry or manual review

---

### Key Concepts That Need to Understand During This Lesson

- Common schema: `{text, metadata: {source, page, section, format, date}}` regardless of input format
- Metadata as the prerequisite for filtering, citations, and debugging
- Unstructured as the go-to library for production multi-format ingestion
- Error isolation: treat each document as an independent unit; never let one failure block others
- Table handling strategy depends on query patterns: markdown for prose questions, JSON for lookups

---

### Interview Preparation

**Beginner Questions**

1. How do you handle tables in a RAG pipeline?
2. What metadata should every chunk carry?
3. What happens when a document fails to parse in production?

**Intermediate Questions**

1. Design a document ingestion pipeline that handles PDF, HTML, and markdown from multiple sources.
2. How would you handle a 500-page PDF with tables and embedded images?
3. How do you design a schema that keeps metadata consistent across 5 different document formats?

---

## Lesson 5.5: Re-ranking Introduction 🔴 Essential

### Objective

Understand why initial retrieval is approximate, how cross-encoder re-ranking improves precision, and when the latency cost is justified.

### Topics Covered

1. Why Initial Retrieval is Approximate 🔴
2. Cross-Encoder Re-ranking 🔴
3. Cohere Rerank API 🔴
4. Open-Source Cross-Encoders 🟡
5. Cost and Latency Tradeoffs 🔴

### Subtopics

1. Why Initial Retrieval is Approximate 🔴
   - Bi-encoders encode query and document independently, then compare
   - Fast (pre-computed document vectors) but loses nuance
   - No token-level interaction between query and document
2. Cross-Encoder Re-ranking 🔴
   - Query and candidate document processed together in one forward pass
   - Full token-level interaction → far more accurate relevance score
   - Cannot scale to millions of docs (O(n) per query); used only on shortlists
3. Cohere Rerank API 🔴
   - Hosted cross-encoder: `co.rerank(query=..., documents=[...], model="rerank-v3.5")`
   - Rerank v3.5 (current as of 2026) replaced the separate English/multilingual v3.0 models with one multilingual model covering 100+ languages
   - Returns relevance scores sorted descending
   - Easy integration; adds ~100–300ms latency
4. Open-Source Cross-Encoders 🟡
   - `cross-encoder/ms-marco-MiniLM-L-6-v2` via sentence-transformers
   - Self-hosted, no per-call cost, higher operational complexity
   - Voyage AI's `rerank-2.5` is a notable hosted alternative to Cohere with domain-tuned variants (code, finance, legal); evaluate both on your golden set rather than assuming either wins
5. Cost and Latency Tradeoffs 🔴
   - Two-stage pattern: bi-encoder retrieves top-50 or top-100; cross-encoder re-ranks to top-5
   - Measure: does re-ranking improve MRR enough to justify latency?
   - Skip re-ranking for latency-critical paths (<200ms budget); use for async or low-latency-tolerance paths

---

### Key Concepts That Need to Understand During This Lesson

- Bi-encoder vs cross-encoder: the efficiency/accuracy tradeoff
- Two-stage pipeline as the production standard: fast retrieval → precise re-ranking
- Cohere Rerank as the fastest path to production cross-encoder capability
- Re-ranking does not retrieve new documents — it reorders the existing shortlist
- Always measure: run your eval set with and without re-ranking to confirm improvement

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between a bi-encoder and a cross-encoder?
2. Why can't you run a cross-encoder over your entire document corpus?
3. What is Cohere Rerank and when would you use it?

**Intermediate Questions**

1. Why use a two-stage retrieval pipeline instead of just a more accurate retriever?
2. You have a 200ms latency budget for a search endpoint. Should you add re-ranking? How do you decide?
3. Compare Cohere Rerank with an open-source cross-encoder. When would you choose each?

---

## Week 5 Summary Checklist

- [ ] Can explain all 4 RAG architecture patterns and when to use each
- [ ] Can explain GraphRAG and when relational queries justify its added ingestion cost
- [ ] Implemented 3+ chunking strategies with measurable Precision@5 and Recall@5
- [ ] Understand Contextual Retrieval and why it improves any chunking strategy it's layered onto
- [ ] Understand parent-child chunking and when it beats recursive chunking
- [ ] Implemented hybrid search: BM25 + dense + RRF fusion
- [ ] Built a document processing pipeline for at least 2 formats (PDF + markdown)
- [ ] Understand cross-encoder re-ranking and the two-stage retrieval pattern
- [ ] Completed chunking comparison assignment with DECISIONS.md
- [ ] Can sketch the full RAG pipeline for a 10K-document knowledge base

---

# Week 6 — LangGraph & Advanced RAG

**Estimated Time:** ~10–12 hours
**Goal:** Master LangGraph as your primary orchestration framework. Build stateful, conditional workflows. Implement advanced RAG patterns that go beyond simple vector lookup.

---

## Lesson 6.1: LangChain Expression Language (LCEL) Fundamentals 🟡 Important

### Objective

Understand LCEL's pipe syntax, know when it helps, and know when to reach for LangGraph instead.

### Topics Covered

1. LCEL Pipe Syntax and Runnables 🟡
2. RunnablePassthrough, RunnableLambda, RunnableParallel 🟡
3. Streaming with LCEL Chains 🟡
4. Binding Tools and Output Parsers 🟡
5. When LCEL Helps vs When It Adds Abstraction 🟡

### Subtopics

1. LCEL Pipe Syntax 🟡
   - Python pipe operator `|` chains Runnables
   - Simple RAG chain: `retriever | format_docs | prompt | llm | output_parser`
   - Each stage transforms the data flowing through
2. Core Runnables 🟡
   - `RunnablePassthrough`: passes input unchanged; used to inject original query alongside retrieved docs
   - `RunnableLambda`: wraps any Python function as a Runnable
   - `RunnableParallel`: runs multiple branches simultaneously
3. Streaming with LCEL 🟡
   - Streaming is automatic for any chain ending with an LLM
   - Use `.stream()` instead of `.invoke()` for token-by-token output
   - Works with `StreamingResponse` in FastAPI
4. Binding Tools and Output Parsers 🟡
   - `.bind_tools()` attaches tool schemas to an LLM call
   - Output parsers: `StrOutputParser`, `JsonOutputParser`, Pydantic parsers
5. LCEL vs Raw Python 🟡
   - LCEL value: composable, streamable, async-compatible automatically
   - LCEL cost: abstraction overhead, harder to debug with complex branching
   - Rule: use LCEL for linear chains; use LangGraph for anything with branching or cycles

---

### Key Concepts That Need to Understand During This Lesson

- LCEL as syntactic sugar for composable, streamable LLM pipelines
- The Runnable interface as the common contract across all LCEL components
- Why `RunnableParallel` matters: run retrieval and other steps concurrently
- LCEL's streaming support is automatic — no extra code needed
- Knowing when NOT to use LCEL is as important as knowing how

---

### Interview Preparation

**Beginner Questions**

1. What problem does LCEL solve?
2. What is the difference between `.invoke()` and `.stream()` in LCEL?
3. What is `RunnablePassthrough` and when would you use it?

**Intermediate Questions**

1. When would you use raw Python functions instead of LCEL?
2. How does `RunnableParallel` improve RAG pipeline performance?
3. You have a chain that needs to send the original query and retrieved docs to the LLM together. How do you wire that in LCEL?

---

## Lesson 6.2: LangGraph for Stateful Workflows 🔴 Essential

### Objective

Build stateful, conditional, cyclical AI workflows using LangGraph's graph model.

### Topics Covered

1. Graph Concepts: Nodes, Edges, Conditional Edges 🔴
2. State Management with TypedDict or Pydantic 🔴
3. Conditional Routing Based on State 🔴
4. Cycles and Iterative Processing 🔴
5. Checkpointing and Persistence 🟡
6. LangGraph vs LCEL: When to Reach for Which 🔴

### Subtopics

1. Graph Concepts 🔴
   - Nodes: processing steps (retrieve, grade, generate, rewrite)
   - Edges: unconditional transitions between nodes
   - Conditional edges: inspect state → route to different next nodes
   - Entry point and terminal nodes define the graph boundaries
2. State Management 🔴
   - State is a TypedDict (or Pydantic model) carrying all data through the graph
   - Each node receives the full state, returns a partial update
   - LangGraph merges partial updates automatically
   - Common state fields: `query`, `retrieved_docs`, `quality_score`, `answer`, `iteration_count`
3. Conditional Routing 🔴
   - Conditional edge maps a state value to the next node name
   - Example: if `quality_score < 0.5` → "rewrite_query"; else → "generate_answer"
   - Graph structure is self-documenting: readable as a flowchart
4. Cycles and Iterative Processing 🔴
   - LangGraph supports cycles; a node can route back to an earlier node
   - Critical for corrective RAG: bad retrieval → rewrite → retrieve again
   - Always implement iteration count guard to prevent infinite loops
5. Checkpointing and Persistence 🟡
   - `MemorySaver`: in-memory state between graph invocations
   - Postgres/Redis backends: persist state across restarts
   - Required for human-in-the-loop approval gates
6. LangGraph vs LCEL 🔴
   - LCEL: linear, no branching, simple pipelines
   - LangGraph: branching, cycles, state tracking, human-in-the-loop
   - Decision rule: if your pipeline needs an `if` or a loop, use LangGraph

---

### Key Concepts That Need to Understand During This Lesson

- State as the shared data structure — the backbone of any LangGraph workflow
- Conditional edges as the mechanism for all branching and retry logic
- Cycles as the feature that enables corrective and iterative patterns
- Graph structure as documentation: the topology describes the business logic
- Checkpointing as the foundation for multi-turn agents and human approval gates

---

### Hands-on Exercises

- Build a LangGraph workflow with a retrieve node, quality-grade node, and conditional edge routing to either "generate" or "rewrite-and-retry"
- Visualize the graph with `graph.get_graph().draw_mermaid()`
- Add an iteration count guard to prevent infinite retry loops

### Assignment

📄 Assignment File: `assignments/w06-a1-langgraph-advanced-rag.md`

Short description: Build an advanced RAG pipeline using LangGraph with query routing, corrective re-query, and re-ranking. Visualize the graph.

---

### Interview Preparation

**Beginner Questions**

1. How does LangGraph differ from a simple LCEL chain?
2. What is the role of state in LangGraph?
3. What are conditional edges and how do you use them?

**Intermediate Questions**

1. When should you use LangGraph over LCEL?
2. Design a corrective RAG workflow in LangGraph. What nodes and edges do you need?
3. How does checkpointing enable human-in-the-loop workflows?

---

## Lesson 6.3: Advanced RAG Patterns 🔴 Essential

### Objective

Implement query-level and retrieval-level optimizations that materially improve RAG quality over a baseline pipeline.

### Topics Covered

1. Query Expansion 🔴
2. HyDE (Hypothetical Document Embeddings) 🔴
3. Multi-Query Retrieval 🔴
4. Step-Back Prompting 🟡
5. Corrective RAG 🔴
6. Adaptive RAG 🔴
7. Self-RAG 🟢

### Subtopics

1. Query Expansion 🔴
   - Generate 3–5 reformulations of the original query
   - Search with all variants; deduplicate results before feeding to LLM
   - Addresses vocabulary gap between user language and document language
2. HyDE 🔴
   - Ask the LLM to generate a hypothetical answer without any retrieval
   - Embed the hypothetical answer and use it as the search query
   - Why it works: hypothetical answer is in "document language," bridges the query-document gap
   - Best for: short or vague queries, specialized domains
3. Multi-Query Retrieval 🔴
   - Generate multiple parallel queries, retrieve separately, deduplicate
   - Each query explores a different angle of the same question
   - Improves recall at the cost of extra LLM and retrieval calls
4. Step-Back Prompting 🟡
   - Abstract the specific question into a more general one first
   - Example: "What caused the 2008 crisis?" → "What are the general causes of financial crises?"
   - Retrieves broader context; helps with complex reasoning questions
5. Corrective RAG 🔴
   - After retrieval, a grading step (LLM-as-judge) evaluates document relevance
   - If grade is low: rewrite query → retry retrieval → or escalate to web search
   - Natural fit for LangGraph conditional edges
   - Prevents hallucination from forcing generation on irrelevant context
6. Adaptive RAG 🔴
   - Classify query type first, then route to different retrieval strategies
   - Factual lookup → precise dense retrieval; conceptual → broader retrieval
   - Multi-hop → iterative retrieval loop; relational → GraphRAG (Lesson 5.1)
   - This is the emerging 2026 production default: start at the simplest pattern that answers a query, escalate only when the classifier signals it's needed — keeps cost low for easy queries while reserving the expensive patterns (agentic, GraphRAG) for queries that truly require them
7. Self-RAG 🟢
   - LLM grades its own retrieval and generation quality
   - Generates special tokens to reflect on whether retrieval is needed
   - Higher accuracy but complex to implement; know the concept

---

### Key Concepts That Need to Understand During This Lesson

- Query expansion and HyDE are the two highest-ROI advanced RAG patterns
- HyDE works because documents and hypothetical answers share more vocabulary than queries and documents
- Corrective RAG as a mandatory addition to any production system that cannot afford hallucination
- Multi-query retrieval trades latency and cost for recall improvement
- Adaptive RAG is the production default in 2026: a complexity classifier routes each query to the cheapest pattern that can answer it, escalating to agentic or graph-based retrieval only when justified
- Self-RAG is research-level; know it conceptually, do not implement in Month 2

---

### Interview Preparation

**Beginner Questions**

1. What is HyDE and when does it help?
2. What is query expansion?
3. How does Corrective RAG prevent hallucination?

**Intermediate Questions**

1. Explain HyDE in detail. What is the core insight that makes it work?
2. Design a corrective RAG system in LangGraph. Walk through the nodes and conditional edges.
3. Compare query expansion, HyDE, and multi-query retrieval. When would you choose each?

---

## Lesson 6.4: Query Routing 🟡 Important

### Objective

Classify incoming queries by intent and route them to the optimal retrieval strategy.

### Topics Covered

1. Semantic Routing — Classify Intent, Route to Pipeline 🟡
2. Routing by Data Source 🟡
3. LLM-Based vs Embedding-Based Routing 🟡
4. Fallback Strategies When Routing Fails 🟡
5. Implementation with LangGraph Conditional Edges 🟡

### Subtopics

1. Semantic Routing 🟡
   - Classify query intent: factual lookup, conceptual explanation, multi-hop reasoning, unanswerable
   - Each category routes to a different downstream node
   - Not all queries should go through the same pipeline
2. Routing by Data Source 🟡
   - Different retrievers for different document types
   - Example: financial queries → financial doc store; technical queries → code + API docs store
   - Reduces noise by narrowing the search space
3. LLM-Based vs Embedding-Based Routing 🟡
   - LLM-based: classify with a chat completion call; flexible but +latency +cost
   - Embedding-based: compare query embedding to category exemplars; fast but needs pre-defined categories
   - Hybrid: embedding-based for known categories, LLM fallback for ambiguous cases
4. Fallback Strategies 🟡
   - If routing confidence is low, default to the broadest retrieval strategy
   - Log all routing decisions — misclassifications are a debugging goldmine
5. LangGraph Implementation 🟡
   - Router is a node that outputs a route classification
   - Conditional edge maps route to downstream node
   - Fallback edge routes to a default node on unknown classification

---

### Key Concepts That Need to Understand During This Lesson

- Query routing as the entry point for query-type-specific optimization
- Embedding-based routing as the low-latency production default
- Routing decisions must be logged: misclassification patterns reveal system weaknesses
- The fallback matters: a broken router that returns garbage is worse than no router
- In LangGraph, routing is just a conditional edge — same pattern as corrective RAG

---

### Interview Preparation

**Beginner Questions**

1. Why route queries instead of using one pipeline for everything?
2. What is the difference between LLM-based and embedding-based routing?
3. What is a fallback strategy in query routing?

**Intermediate Questions**

1. Design a query routing system for a RAG product that serves both technical and business users. What categories do you define and how do you classify?
2. Embedding-based routing is faster but less flexible. When does LLM-based routing justify the extra latency?
3. How do you test your routing system and identify misclassifications?

---

## Lesson 6.5: Caching Strategies 🟡 Important

### Objective

Implement caching layers that reduce cost and latency across the RAG pipeline without sacrificing answer freshness.

### Topics Covered

1. Exact Match Caching 🟡
2. Semantic Caching 🟡
3. Embedding Cache 🔴
4. LLM Response Caching 🟡
5. Cache Invalidation When Documents Update 🟡
6. Cost Savings Calculation 🟡

### Subtopics

1. Exact Match Caching 🟡
   - Hash the query string; store query → response in Redis
   - Simple, zero false positives
   - Misses: paraphrased questions that should get the same answer
2. Semantic Caching 🟡
   - Embed each query; check if a cached query exists within cosine similarity threshold (e.g., > 0.95)
   - Returns the cached response for semantically equivalent paraphrases
   - Appropriate when: high traffic, stable corpus, many users ask similar questions
   - Not appropriate when: answers are personalized or highly time-sensitive
3. Embedding Cache 🔴
   - Cache pre-computed document embeddings in the vector DB
   - If the corpus does not change, never re-embed the same document twice
   - Biggest single caching opportunity in most RAG systems
4. LLM Response Caching 🟡
   - Cache key: prompt + model + params (temperature=0 required for determinism)
   - Works well for FAQ-style RAG; fails for personalized or time-sensitive queries
   - Invalidation trigger: underlying documents or prompt templates change
5. Cache Invalidation 🟡
   - Document update → invalidate all chunks derived from that document
   - Maintain chunk-to-source mapping for targeted invalidation
   - Full index rebuild required if embedding model changes
6. Cost Savings Calculation 🟡
   - Estimate hit rate from query log analysis
   - Savings = hit_rate × queries_per_day × cost_per_LLM_call
   - Include embedding cache savings separately (often largest)

---

### Key Concepts That Need to Understand During This Lesson

- Embedding cache is the first and highest-impact caching layer in any RAG system
- Semantic caching is powerful but requires threshold tuning to avoid false positives
- Cache invalidation is the hard part — think about it at design time, not after production issues
- Cost savings must be measured, not estimated from intuition
- Caching and freshness are in tension: the higher the hit rate, the staler the responses can become

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between exact match and semantic caching?
2. Why is the embedding cache often the highest-impact caching layer?
3. What triggers cache invalidation in a RAG system?

**Intermediate Questions**

1. Design a caching strategy for a RAG system serving 100K queries/day with a corpus that updates weekly.
2. What is semantic caching and when is it appropriate? When is it NOT appropriate?
3. How do you handle cache invalidation when your embedding model changes?

---

## Week 6 Summary Checklist

- [ ] Can write LCEL chains and know when LangGraph is the better tool
- [ ] Built a LangGraph workflow with nodes, edges, conditional routing, cycles, and state
- [ ] Implemented at least 3 advanced RAG patterns (query expansion, HyDE, corrective)
- [ ] Can explain Adaptive RAG routing and why it's the 2026 production default for managing cost across query complexity
- [ ] Query routing working with 2+ routes to different retrieval strategies
- [ ] Understand all 5 caching layers and their cost/latency impact
- [ ] Completed LangGraph pipeline assignment with routing and re-ranking
- [ ] Visualized graph with draw_mermaid()
- [ ] Can sketch a multi-strategy RAG system for a heterogeneous corpus


---

# Week 7 — Evals & Observability

**Estimated Time:** ~10–12 hours
**Goal:** Build a rigorous eval harness and production observability stack. Evals are the #1 hiring signal for GenAI engineers in 2026 — this week turns you from someone who builds demos into someone who builds products.

---

## Lesson 7.1: Why Evals Matter 🔴 Essential

### Objective

Understand why evals are the defining differentiator between a demo and a production system, and why they are the strongest hiring signal in 2026 GenAI engineering.

### Topics Covered

1. The 2026 Hiring Signal 🔴
2. Vibes-Based vs Metrics-Driven Development 🔴
3. Evals as Guardrails, Regression Tests, and Improvement Drivers 🔴
4. Eval-Driven Development 🔴
5. Real-World Failures from Missing Evals 🟡

### Subtopics

1. The 2026 Hiring Signal 🔴
   - The first thing interviewers ask: "How do you evaluate your systems?"
   - Candidates who cannot answer this have not shipped production AI
   - Eval fluency signals the gap between demo-builders and production engineers
2. Vibes-Based vs Metrics-Driven 🔴
   - Vibes-based: "it feels better" after a prompt change — no way to know if it regressed
   - Metrics-driven: baseline scorecard → change → measure again → ship only if improved
   - Without metrics: you cannot detect when a reranker helps retrieval but hurts faithfulness
3. Evals as Guardrails, Regression Tests, and Improvement Drivers 🔴
   - Guardrails: define what "good" means before writing code
   - Regression tests: catch when a code or prompt change breaks something
   - Improvement drivers: metrics reveal which component to fix next
4. Eval-Driven Development 🔴
   - Cycle: define golden QA pairs + metrics → measure baseline → change → measure → ship if improved
   - Evals are written before features, not after
   - Golden dataset is a living artifact: expand it as you discover new failure modes
5. Real-World Failure Examples 🟡
   - Prompt change that improved faithfulness but hurt relevancy — caught only by evals
   - New embedding model that helped technical queries but hurt conversational ones
   - Reranker adding 300ms latency without detectable quality improvement

---

### Key Concepts That Need to Understand During This Lesson

- Evals are not a phase at the end of development — they are the foundation
- The eval-driven cycle is the workflow senior GenAI engineers use daily
- Offline evals gate deployments; online evals catch what offline missed
- A golden dataset is a first-class engineering artifact, not a one-time exercise
- If you cannot measure it, you cannot improve it — and you cannot prove it works

---

### Interview Preparation

**Beginner Questions**

1. How do you evaluate a RAG system?
2. What is the difference between offline and online evals?
3. Why are evals described as the #1 hiring signal for GenAI engineers?

**Intermediate Questions**

1. Walk me through your eval-driven development process for a RAG system.
2. How do you build a golden evaluation dataset? What makes it representative?
3. A prompt change improved one metric but degraded another. How do you decide whether to ship?

---

## Lesson 7.2: Eval Types 🔴 Essential

### Objective

Understand the three layers of a mature eval system and how they work together to catch different classes of problems.

### Topics Covered

1. Offline Evals (Pre-Deployment, Golden Dataset) 🔴
2. Online Evals (Production Feedback Signals) 🔴
3. Regression Evals 🔴
4. A/B Testing for GenAI 🟡
5. Component-Level vs End-to-End Evals 🔴

### Subtopics

1. Offline Evals 🔴
   - Run on a fixed golden dataset before deployment
   - Gate deployments: do not ship if offline metrics degrade
   - Fast, cheap, deterministic — run on every code change
2. Online Evals 🔴
   - Measure live user interactions: thumbs up/down, time-to-resolution, follow-up question rate
   - Catch failure modes the golden dataset did not cover
   - Requires instrumentation in production (Langfuse, LangSmith)
3. Regression Evals 🔴
   - Full eval suite run after every pipeline change
   - Automated: trigger on CI/CD pipeline or pre-deployment hook
   - Alert if any metric drops > 5% from baseline
4. A/B Testing for GenAI 🟡
   - Route a percentage of traffic to the new prompt/model/pipeline variant
   - Compare metrics between control and treatment groups
   - Statistical significance required before declaring a winner
5. Component-Level vs End-to-End 🔴
   - Component: test retrieval precision, reranker effectiveness, prompt quality independently
   - End-to-end: given a question, is the final answer correct and well-cited?
   - Critical insight: improving a component can degrade the overall system — always run E2E after component changes
   - Component evals diagnose WHERE the problem is; E2E evals confirm the fix worked

---

### Key Concepts That Need to Understand During This Lesson

- Three-layer eval system: component + end-to-end + regression
- Offline evals gate deployments; online evals catch production drift
- Component improvements can cause unexpected E2E regressions — always measure both
- Regression evals must be automated, not run manually
- A/B testing is the gold standard for measuring impact on real users

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between offline and online evals?
2. Why run component-level evals in addition to end-to-end?
3. What is a regression eval?

**Intermediate Questions**

1. How do you automate regression detection in a production RAG system?
2. You improved retrieval precision by 20% but end-to-end faithfulness dropped 10%. What happened and how do you investigate?
3. Design an A/B testing framework for comparing two prompt variants in production.

---

## Lesson 7.3: Building Eval Datasets and Metrics 🔴 Essential

### Objective

Build a diverse, representative golden dataset and understand the four core RAG metrics.

### Topics Covered

1. Golden QA Pairs — Structure, Diversity, Edge Cases 🔴
2. Synthetic Dataset Generation 🟡
3. Retrieval Metrics: Precision@k, Recall@k, MRR, NDCG 🔴
4. Generation Metrics: Faithfulness, Relevancy, Correctness, Harmfulness 🔴
5. Custom Metrics for Domain-Specific Requirements 🟡
6. Statistical Significance 🟡

### Subtopics

1. Golden QA Pairs 🔴
   - Minimum 30–50 diverse questions representing real user queries
   - Each entry: question + expected answer + relevant source passages
   - Question types: factual, multi-chunk synthesis, unanswerable, adversarial, paraphrased
   - Domain expert validation required before using as ground truth
2. Synthetic Dataset Generation 🟡
   - Use LLM to generate questions from your corpus: `Given this passage, generate 3 questions a user might ask`
   - Cheap to scale; validate quality with human spot-check
   - Useful for bootstrapping when no user data exists yet
3. Retrieval Metrics 🔴
   - **Precision@k**: fraction of top-k results that are relevant (are the retrieved docs good?)
   - **Recall@k**: fraction of all relevant docs found in top-k (did we miss anything?)
   - **MRR (Mean Reciprocal Rank)**: rank of the first relevant result (how fast do we surface the right doc?)
   - **NDCG**: are more relevant results ranked higher than less relevant? (quality-weighted ranking)
4. Generation Metrics 🔴
   - **Faithfulness**: is the answer grounded in retrieved context? (hallucination detection)
   - **Answer Relevancy**: does the answer actually address the question?
   - **Answer Correctness**: is the answer factually right compared to ground truth?
   - **Harmfulness**: does the answer contain toxic, biased, or harmful content? (safety eval)
5. Custom Metrics 🟡
   - Citation accuracy: did the LLM cite the correct source chunks?
   - Tone/style: is the answer appropriate for the target audience?
   - Completeness: does the answer cover all aspects of the question?
6. Statistical Significance 🟡
   - Small eval sets produce noisy results — a 2% metric change on 20 questions is not real
   - Use bootstrap confidence intervals or run multiple eval passes and average
   - Minimum 50 questions for reliable comparison; 200+ for fine-grained model decisions

---

### Key Concepts That Need to Understand During This Lesson

- Faithfulness is the most critical metric: it detects hallucination
- Include unanswerable questions: a system that always attempts an answer will hallucinate on these
- The four core RAGAS metrics together give a comprehensive view of retrieval + generation quality
- Your golden dataset is a product artifact: version-control it and expand it continually
- MRR is the most actionable retrieval metric for debugging rank ordering problems

---

### Interview Preparation

**Beginner Questions**

1. What does faithfulness measure and why is it critical?
2. How do you handle questions with no answer in the corpus in your eval set?
3. What is MRR and what does a low MRR tell you?

**Intermediate Questions**

1. Design a golden eval dataset for a RAG system over a technical documentation corpus. What question types do you include?
2. Distinguish Precision@k from Recall@k. When would you prioritize one over the other?
3. How do you use synthetic question generation to bootstrap an eval dataset?

---

## Lesson 7.4: RAGAS Framework 🔴 Essential

### Objective

Run RAGAS evaluations, interpret the four core metrics, and understand the framework's limitations.

### Topics Covered

1. RAGAS Architecture and Philosophy 🔴
2. Core Metrics: Faithfulness, Answer Relevancy, Context Precision, Context Recall 🔴
3. Running RAGAS on Your Dataset 🔴
4. Interpreting RAGAS Scores 🔴
5. RAGAS Limitations 🟡
6. Alternatives: DeepEval, Custom Eval Scripts 🟡

### Subtopics

1. RAGAS Architecture 🔴
   - LLM-as-judge under the hood: constructs specific prompts per metric
   - Input schema: `(question, answer, contexts, ground_truth)` tuples per sample
   - Output: per-sample scores + aggregated dataset-level scores
2. Core Metrics 🔴
   - **Faithfulness**: extracts claims from generated answer; checks each claim against retrieved context; score = supported_claims / total_claims
   - **Answer Relevancy**: measures how directly the answer addresses the question (ignores factual accuracy)
   - **Context Precision**: are the retrieved documents relevant to the question? (retrieval quality)
   - **Context Recall**: were all necessary documents retrieved? (retrieval completeness)
3. Running RAGAS 🔴
   - Install: `pip install ragas`
   - Build a `Dataset` with required columns
   - Call `evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])`
   - Returns a `Result` object with scores per sample and mean
4. Interpreting Scores 🔴
   - Scores range 0–1 (higher is better)
   - Faithfulness < 0.8: significant hallucination risk
   - Context Recall < 0.7: retrieval is missing relevant documents
   - Use per-sample scores to identify the hardest questions for your system
5. RAGAS Limitations 🟡
   - Depends on LLM quality for judging — model choice affects results
   - Costs money per eval run (LLM calls per sample per metric)
   - Score variance between runs: average 3 runs for close decisions
   - May not capture domain-specific quality dimensions
6. Alternatives 🟡
   - DeepEval: pytest-style framework with 14+ metrics (RAGAS-compatible plus agent, chatbot, and safety metrics); built for CI/CD quality gates that block a merge on regression
   - DeepEval has grown into the broader choice for 2026 — use it when you need eval coverage beyond RAG (agents, multi-turn chat, tool-call correctness) inside a standard pytest pipeline
   - Custom eval scripts: full control, required for domain-specific metrics
   - Human eval: gold standard, not scalable alone

---

### Key Concepts That Need to Understand During This Lesson

- RAGAS as the standard starting point for RAG system evaluation
- Faithfulness = hallucination detector; it is the metric you cannot afford to neglect
- Context Precision and Recall give separate signals: bad retrieval can manifest as either
- Run RAGAS after every pipeline change; compare against your baseline scorecard
- RAGAS is a tool, not a complete eval strategy — pair it with DeepEval or custom metrics once your system includes agents, multi-turn chat, or needs CI/CD-gated regression tests

---

### Interview Preparation

**Beginner Questions**

1. What is RAGAS and what does it measure?
2. How does RAGAS measure faithfulness?
3. What input does RAGAS require to evaluate a RAG system?

**Intermediate Questions**

1. RAGAS context recall is 0.60 for your system. What does this tell you and how do you investigate?
2. What are the limitations of using RAGAS as your only evaluation framework?
3. How do you integrate RAGAS into a CI/CD pipeline to catch regressions before deployment?

---

## Lesson 7.5: LLM-as-Judge Pattern 🔴 Essential

### Objective

Design reliable LLM-as-judge evaluations with detailed rubrics, understand bias sources, and know when to prefer human evaluation.

### Topics Covered

1. Using an LLM to Evaluate LLM Output 🔴
2. Designing Judge Prompts — Rubrics, Scoring Criteria, Examples 🔴
3. Pairwise Comparison vs Absolute Scoring 🔴
4. Reducing Judge Bias 🔴
5. When LLM-as-Judge vs Human Eval vs Programmatic Metrics 🔴

### Subtopics

1. LLM-as-Judge Overview 🔴
   - Separate LLM call (ideally stronger model: GPT-4o or Claude Sonnet) evaluates the generated response
   - Provide: question, retrieved context, generated answer, evaluation rubric
   - Returns: score + justification
   - Scales better than human eval; more nuanced than programmatic metrics
2. Designing Judge Prompts 🔴
   - Vague rubrics produce inconsistent scores — define every level explicitly
   - Example rubric for faithfulness:
     - 5 = all claims supported by context with citations
     - 3 = mostly correct, missing one key point
     - 1 = contains hallucinated claims not in context
   - Include examples of each score level (few-shot judge)
3. Pairwise Comparison vs Absolute Scoring 🔴
   - Absolute: "Rate this answer 1–5" — useful for trend tracking
   - Pairwise: "Is answer A better than answer B?" — more reliable for direct comparison
   - Use pairwise for high-stakes decisions: prompt variants, model swaps
   - Absolute scoring is cheaper and easier to aggregate over time
4. Reducing Judge Bias 🔴
   - Position bias: LLMs prefer the first option in pairwise comparisons — randomize order
   - Verbosity bias: longer answers score higher even if less accurate — rubric should penalize padding
   - Self-preference bias: a model rates its own outputs higher — always use a different model as judge
   - Average across multiple judge runs to reduce variance
5. When to Use Which Eval Type 🔴
   - LLM-as-judge: nuanced quality, tone, citation accuracy, explanations — not measurable programmatically
   - Human eval: final validation for critical decisions; ground truth creation; catching judge errors
   - Programmatic metrics: Precision@k, token counts, latency — fast, cheap, zero LLM dependency

---

### Key Concepts That Need to Understand During This Lesson

- Rubric quality determines judge reliability — invest time in rubric design
- Never use the same model as judge that produced the answer being evaluated
- Pairwise comparison for decisions; absolute scoring for monitoring over time
- The three bias types (position, verbosity, self-preference) must all be mitigated
- LLM-as-judge is a force multiplier: scales nuanced evaluation to thousands of samples

---

### Interview Preparation

**Beginner Questions**

1. What is the LLM-as-judge pattern?
2. Why should you not use the same model as judge that produced the answer?
3. What is the difference between pairwise comparison and absolute scoring?

**Intermediate Questions**

1. How do you make LLM-as-judge evaluations reliable? Name three bias sources and how to mitigate them.
2. Design a judge prompt rubric for evaluating citation quality in a RAG system.
3. When would you choose human evaluation over LLM-as-judge?

---

## Lesson 7.6: Langfuse for Observability & Tracing 🔴 Essential

### Objective

Instrument a RAG pipeline with Langfuse to trace every query end-to-end, track costs, version prompts, and build quality dashboards.

### Topics Covered

1. Why Observability Matters for LLM Applications 🔴
2. Langfuse Architecture: Traces, Spans, Generations, Scores 🔴
3. Instrumenting Your RAG Pipeline with Langfuse 🔴
4. Cost Tracking Per Query, Per User, Per Feature 🔴
5. Prompt Versioning and Management 🟡
6. Building Dashboards for Quality Monitoring 🟡
7. Langfuse Alternatives (LangSmith, Phoenix, Helicone) 🟢

### Subtopics

1. Why Observability Matters 🔴
   - Without it: when a user reports a bad answer, you have no idea what happened
   - With it: find any query's full trace — what was retrieved, what prompt was sent, what the LLM returned, how long each step took, what it cost
   - Observability is the feedback loop that turns production behavior into system improvements
2. Langfuse Architecture 🔴
   - **Trace**: one complete query lifecycle (top-level container)
   - **Span**: a processing step within a trace (retrieve, rerank, generate)
   - **Generation**: an LLM call within a span (model, prompt, response, tokens, cost)
   - **Score**: a quality metric attached to a trace (faithfulness, user thumbs up/down)
3. Instrumenting Your Pipeline 🔴
   - Decorator-based: `@observe()` on any function automatically captures inputs, outputs, latency
   - Manual: `langfuse.trace()`, `trace.span()`, `span.generation()` for fine-grained control
   - Always log: query, retrieved docs with scores, prompt template version, LLM response, token counts, latency per stage
4. Cost Tracking 🔴
   - Langfuse aggregates token counts → calculates cost per generation using model pricing
   - Dashboard shows: cost per query, cost per user, cost per feature, daily/weekly totals
   - Identify which pipeline paths are most expensive
5. Prompt Versioning 🟡
   - Store prompt templates in Langfuse; fetch by version at runtime
   - Link which prompt version produced which trace results
   - Run evals across versions to validate improvements before promoting
6. Quality Dashboards 🟡
   - Plot faithfulness, relevancy, precision scores over time
   - Per-category breakdown: factual vs multi-hop vs unanswerable
   - Identify failure patterns from low-scoring traces
7. Alternatives 🟢
   - LangSmith: tight LangChain integration; good for LangGraph workflows
   - Phoenix (Arize): open-source; strong eval integration
   - Helicone: simpler; proxy-based, minimal code changes; cost-focused
   - Note: Langfuse was acquired by ClickHouse in January 2026; the core product remains MIT-licensed and fully self-hostable — this guide's recommendation to use Langfuse is unaffected

---

### Key Concepts That Need to Understand During This Lesson

- Observability is the production feedback loop: trace → identify failure → improve → verify with evals
- `@observe()` decorator as the zero-friction entry point to Langfuse
- Trace hierarchy: Trace → Span → Generation → Score
- Every query in production should have a trace ID for debugging
- Cost tracking is not a nice-to-have: at scale it is the difference between profitable and not

---

### Hands-on Exercises

- Instrument the Week 5/6 RAG pipeline with `@observe()` on every function
- Attach RAGAS faithfulness scores as Langfuse scores on each trace
- Build a Langfuse dashboard showing faithfulness trend over your 30-question eval set

### Assignment

📄 Assignment File: `assignments/w07-a1-eval-harness-langfuse.md`

Short description: Build a 30-question eval harness with RAGAS + LLM-as-judge, integrate Langfuse tracing, and produce a baseline scorecard.

---

### Interview Preparation

**Beginner Questions**

1. What is Langfuse and why do you use it?
2. What is the difference between a trace, a span, and a generation in Langfuse?
3. What would you trace in a production RAG system?

**Intermediate Questions**

1. How do you use Langfuse tracing to debug a bad answer in production?
2. How do you use observability data to improve a RAG system? Give a concrete example.
3. Compare Langfuse and LangSmith. When would you choose each?

---

## Week 7 Summary Checklist

- [ ] Can articulate why evals are the #1 hiring signal for GenAI engineers in 2026
- [ ] Understand the difference between offline, online, regression, and component evals
- [ ] Built a golden eval dataset of 30+ questions with diverse categories (factual, synthesis, unanswerable, adversarial)
- [ ] Can run RAGAS and interpret all four core metrics (faithfulness, relevancy, context precision, context recall)
- [ ] Implemented LLM-as-judge with a detailed rubric; can name and mitigate 3 bias types
- [ ] Langfuse integrated and tracing queries end-to-end with cost tracking
- [ ] Baseline scorecard established for RAG pipeline
- [ ] Completed eval harness assignment with Langfuse integration

---

# Week 8 — RAG Capstone

**Estimated Time:** ~15–20 hours
**Goal:** Ship a complete, production-grade RAG system. Portfolio-ready: deployed, evaluated, observed, and documented. EVALS.md + DECISIONS.md are required deliverables alongside code.

---

## Lesson 8.1: Multi-Format Document Ingestion 🟡 Important

### Objective

Build a unified ingestion pipeline that handles PDF, markdown, HTML, and plain text with consistent metadata and robust error handling.

### Topics Covered

1. Unified Ingestion Pipeline for Multiple Formats 🟡
2. Document Type Detection and Routing 🟡
3. Metadata Extraction and Standardization 🔴
4. Handling Large Document Collections 🟡
5. Error Handling and Partial Failure Recovery 🔴

### Subtopics

1. Unified Ingestion Pipeline 🟡
   - Format router: detect file type → dispatch to format-specific parser
   - Parsers: PyMuPDF for PDFs, BeautifulSoup for HTML, standard markdown parser
   - All output normalized to common schema before downstream processing
2. Document Type Detection 🟡
   - Detect by file extension first; fallback to MIME type or content sniffing
   - Route to appropriate parser at ingestion time
   - Log format distribution in your manifest for corpus analysis
3. Metadata Standardization 🔴
   - Common schema: `{text, metadata: {source, page, section, format, date, access_control}}`
   - Consistent schema enables filtering, citations, and debugging regardless of source format
   - Metadata is immutable after ingestion — if wrong, re-ingest the document
4. Handling Large Collections 🟡
   - Batch processing with async/await for throughput
   - Progress tracking: log processed count, failed count, total tokens embedded
   - Checkpointing: resume from last successful batch on failure
5. Error Handling 🔴
   - Per-document try/catch — one malformed PDF must not crash the pipeline
   - Maintain a manifest: successfully processed vs failed vs skipped
   - Failed-document queue for retry or manual review
   - Never let a single bad document block others from being indexed

---

### Key Concepts That Need to Understand During This Lesson

- Common schema is the contract between ingestion and all downstream stages
- Error isolation is non-negotiable in production: treat each document as independent
- Metadata at ingestion time is the cheapest time to capture it
- The manifest is a first-class deliverable: users need to know what made it into the index
- Async batch ingestion for large collections: sequential processing of 10K docs is too slow

---

### Interview Preparation

**Beginner Questions**

1. How do you design a document ingestion pipeline that handles multiple formats?
2. What happens when a document fails to parse in production?
3. What metadata should every chunk in your index carry?

**Intermediate Questions**

1. Design an ingestion pipeline for a corpus of 50K documents spanning PDF, HTML, and markdown. What is your architecture?
2. How do you ensure metadata consistency when documents come from 5 different source systems?
3. A PDF with embedded tables fails to parse correctly. How do you handle it in production?

---

## Lesson 8.2: Hybrid Search + Reranking + Citations 🔴 Essential

### Objective

Assemble the full retrieval stack — hybrid search, cross-encoder reranking, and reliable citations — into a production-ready pipeline.

### Topics Covered

1. Combining Dense + Sparse Retrieval with RRF 🔴
2. Integrating Cross-Encoder Reranking 🔴
3. Citation Extraction: Mapping Answer to Source Chunks 🔴
4. Citation Formats: Inline References, Footnotes, Source Cards 🟡
5. Deduplication of Overlapping Retrieved Chunks 🟡

### Subtopics

1. Dense + Sparse + RRF 🔴
   - Run BM25 and dense retrieval in parallel; merge with RRF
   - Start: retrieve top-50 from each → RRF merge → feed top-20 to reranker
   - Measure: does hybrid beat dense-only on your eval set? (it almost always does)
2. Cross-Encoder Reranking 🔴
   - Reranker takes the RRF-merged shortlist (20–50 docs) → scores each → returns sorted list
   - Use top-5 from reranker as final context for the LLM
   - Cohere Rerank or `cross-encoder/ms-marco-MiniLM-L-6-v2` (open-source)
3. Citation Extraction 🔴
   - Number each chunk in the LLM prompt: `[1] <text of chunk 1> [2] <text of chunk 2> ...`
   - Instruct the LLM to cite by number: "According to [1] and [3]..."
   - Post-process: extract reference numbers → map to source chunk metadata (doc name, page, section)
   - Validate: check that each cited number corresponds to a provided chunk (hallucinated citations are worse than no citations)
4. Citation Formats 🟡
   - Inline references: `[1]`, `[2]` embedded in the answer text
   - Footnotes: citations listed at the end of the answer
   - Source cards: clickable UI elements showing doc title, page, excerpt, relevance score
5. Deduplication 🟡
   - Remove near-duplicate chunks before passing to LLM
   - Detect with cosine similarity threshold (> 0.95 = duplicate)
   - Or use exact text overlap: if overlap > 80%, keep the higher-ranked chunk

---

### Key Concepts That Need to Understand During This Lesson

- Retrieval stack order: BM25 + dense → RRF merge → cross-encoder rerank → top-5 to LLM
- Citations are a trust mechanism, not a nice-to-have feature
- Citation validation is mandatory: hallucinated citations destroy user trust
- Source cards as the production UX pattern (Perplexity, ChatGPT browsing)
- Deduplication matters when parent-child chunking creates overlapping context

---

### Interview Preparation

**Beginner Questions**

1. What is the purpose of re-ranking after initial retrieval?
2. How do you implement reliable citations in a RAG system?
3. Why might you get duplicate chunks in your retrieval results?

**Intermediate Questions**

1. Walk through the full retrieval stack for a production RAG system. What are all the stages?
2. A user asks a question and the system cites [3] but chunk 3 does not support the claim. How do you prevent this?
3. How does the number of chunks passed to the reranker affect cost, latency, and quality?

---

## Lesson 8.3: React Streaming UI with Vercel AI SDK 🔴 Essential

### Objective

Build a production streaming chat UI that renders tokens incrementally and displays source cards alongside answers.

### Topics Covered

1. Vercel AI SDK Overview (useChat, Streaming Responses) 🔴
2. Server-Sent Events from FastAPI Backend 🔴
3. Streaming Token-by-Token Display 🔴
4. Rendering Citations Alongside Streaming Answers 🟡
5. Loading States, Error Handling, and Retry UX 🟡
6. Responsive Design for the Chat Interface 🟢

### Subtopics

1. Vercel AI SDK 🔴
   - `useChat()` hook: handles streaming, message history, input state, error states
   - **AI SDK 5+ (current standard in 2026)**: `useChat()` no longer manages input state internally — it uses a transport-based architecture. Call `sendMessage({ text: input })` instead of the older `handleSubmit`/`handleInputChange` pattern; manage the input value yourself with `useState`
   - Messages are composed of typed `parts` (`message.parts.map(part => ...)`), not a single `content` string — this supports mixed text + tool-call rendering in one message
   - The SDK standardized on plain Server-Sent Events for its streaming protocol, replacing the earlier custom data-stream format — simpler to debug with browser dev tools
   - `useCompletion()`: single-turn completion without conversation history
   - Designed to work with SSE backends out of the box
2. FastAPI SSE Backend 🔴
   - `StreamingResponse` with `async generator` yields tokens via SSE format
   - Format: `data: {"token": "..."}\n\n` per chunk; `data: [DONE]\n\n` to terminate
   - CORS must be configured for streaming: standard `CORSMiddleware` setup
3. Streaming Token Display 🔴
   - `useChat()` automatically renders tokens as they arrive — no manual streaming logic
   - Loading state: show skeleton or spinner while retrieval happens before tokens start
   - Leverage your React/TypeScript background — this is standard React state management
4. Citations Alongside Streaming 🟡
   - Tokens stream first; citation metadata arrives as a final JSON payload at end of stream
   - Parse citation data on stream completion; render source cards below the answer
   - Each source card: document title, page/section, relevance score, excerpt snippet
5. Error Handling UX 🟡
   - Network error: show retry button, preserve conversation history
   - Token limit exceeded: display truncation warning
   - Timeout: if no tokens arrive within 3s, show error + retry option
6. Responsive Design 🟢
   - Chat column (70%) + sources panel (30%) on desktop
   - Stacked layout on mobile with sources collapsible

---

### Key Concepts That Need to Understand During This Lesson

- `useChat()` as the single hook that handles 90% of streaming chat UI complexity
- SSE over WebSockets for RAG: simpler, HTTP-compatible, sufficient for unidirectional token streaming
- Citations render after streaming completes: do not block token display waiting for citation data
- Your React background is a major advantage — apply component patterns you already know
- Error handling UX directly impacts user trust in the system

---

### Interview Preparation

**Beginner Questions**

1. How do you stream LLM responses to a React frontend?
2. What is the Vercel AI SDK's `useChat()` hook and what does it handle for you?
3. Why use SSE instead of WebSockets for token streaming?

**Intermediate Questions**

1. Walk through the full data flow: user sends a query → backend retrieves + generates → frontend renders tokens. Every step.
2. How do you render citations in the UI when citation data arrives separately from the streamed tokens?
3. Design the error handling UX for a streaming RAG interface. What failure modes exist and how does each manifest to the user?
4. In AI SDK 5+, `useChat()` no longer manages input state for you. What changed, and how do you wire up the input field now?

---

## Lesson 8.4: RAGAS Eval Dashboard 🟡 Important

### Objective

Turn the one-time eval harness from Week 7 into a continuous quality monitor with trend visualization and regression alerts.

### Topics Covered

1. Automating Eval Runs on Code Changes 🟡
2. Visualizing Metric Trends 🟡
3. Per-Category Breakdown 🟡
4. Comparison View: Before/After a Pipeline Change 🟡
5. Alert Thresholds for Metric Degradation 🟡

### Subtopics

1. Automating Eval Runs 🟡
   - Trigger eval suite after every pipeline change (git hook or CI step)
   - Log results to a JSON file or Langfuse dataset per run
   - Each run should record: timestamp, pipeline version/commit, all metric scores
2. Visualizing Metric Trends 🟡
   - Streamlit dashboard or Jupyter notebook with matplotlib/plotly
   - Line charts for each metric over time (runs on x-axis, score on y-axis)
   - Spot when a code change caused a dip — correlate with commit history
3. Per-Category Breakdown 🟡
   - Aggregate scores by question type: factual, multi-hop, unanswerable, adversarial
   - A pipeline change might help factual but hurt multi-hop — aggregate scores hide this
   - Per-category view is essential for targeted debugging
4. Comparison View 🟡
   - Side-by-side: run N vs run N+1 metric scores
   - Per-question score diff: which specific questions improved or regressed?
   - This turns optimization from guesswork into data-driven decision making
5. Alert Thresholds 🟡
   - If faithfulness drops below 0.85: flag for investigation before deploying
   - If any metric drops > 5% from previous run: block deployment
   - If unanswerable question accuracy drops: the system is hallucinating more

---

### Key Concepts That Need to Understand During This Lesson

- Eval dashboard is the instrument panel for your RAG system — it shows what is healthy and what is not
- Per-category breakdown catches regressions masked by strong aggregate scores
- Comparison view enables data-driven optimization: you can see exactly which questions changed
- Alert thresholds prevent subjective deployment decisions — metrics gate the ship
- The dashboard is also a portfolio artifact: it demonstrates engineering maturity to hiring teams

---

### Interview Preparation

**Beginner Questions**

1. How do you prevent quality regression in a RAG system?
2. Why is a per-category breakdown important for interpreting eval scores?
3. What alert thresholds would you set on your RAG system's eval metrics?

**Intermediate Questions**

1. Walk through your process for evaluating the impact of a chunking strategy change on system quality.
2. An aggregate faithfulness score of 0.87 hides that multi-hop questions score 0.61. How do you surface this?
3. How do you automate eval runs in a CI/CD pipeline for a RAG system?

---

## Lesson 8.5: Langfuse Tracing in Production 🟡 Important

### Objective

Use Langfuse in production to debug bad answers, attach eval scores to traces, track costs, and link prompt changes to quality changes.

### Topics Covered

1. Instrumenting Every Pipeline Stage with @observe() 🔴
2. Custom Scores: Attaching Eval Scores to Traces 🟡
3. Cost Tracking: Per-Query, Per-User, Per-Day 🟡
4. Identifying Failure Patterns from Production Traces 🟡
5. Prompt Versioning: Linking Prompt Changes to Quality Changes 🟡

### Subtopics

1. Full Pipeline Instrumentation 🔴
   - Decorate every function: `@observe()` on router, retriever, reranker, prompt builder, generator
   - What to log per stage: inputs, outputs, latency, token counts
   - The trace ID is the primary debugging key: log it alongside every user-facing request ID
2. Custom Scores 🟡
   - After running RAGAS: `langfuse.score(trace_id=..., name="faithfulness", value=0.87)`
   - After user feedback: `langfuse.score(trace_id=..., name="thumbs_up", value=1)`
   - Scores are queryable: filter traces by low faithfulness to find failure patterns
3. Cost Tracking 🟡
   - Langfuse calculates cost from token counts + model pricing
   - Per-query cost: average and p95 (identify expensive outlier queries)
   - Per-user cost: identify heavy users for capacity planning
   - Per-feature cost: compare RAG path vs fallback path
4. Failure Pattern Identification 🟡
   - Filter traces by low faithfulness score: what do these queries have in common?
   - Common patterns: topic not covered in corpus, ambiguous query confused the router, a specific doc type not handled by ingestion
   - Each failure pattern becomes a backlog item: expand corpus, fix router, improve ingestion
5. Prompt Versioning 🟡
   - Store prompts in Langfuse prompt registry with version numbers
   - Fetch by version at runtime: `langfuse.get_prompt("rag-generation", version=3)`
   - Compare metric distributions between prompt versions using Langfuse dataset runs

---

### Key Concepts That Need to Understand During This Lesson

- Langfuse in production is the flight recorder: every query's full lifecycle is captured
- Attaching eval scores to traces creates a searchable quality signal over your production traffic
- Failure pattern analysis is how you turn observability into roadmap items
- Prompt versioning is the bridge between observability and eval-driven development
- Cost per query must be tracked from day one — surprises at invoice time are avoidable

---

### Interview Preparation

**Beginner Questions**

1. How does Langfuse help you debug a production RAG system?
2. What is a trace in Langfuse and what information does it capture?
3. How do you attach eval scores to Langfuse traces?

**Intermediate Questions**

1. A user reports that the system gave a wrong answer. Walk through how you investigate using Langfuse.
2. How do you use Langfuse to identify which query types are most expensive in your RAG pipeline?
3. How do prompt versioning in Langfuse and your eval harness work together to validate prompt improvements?

---

## Lesson 8.6: Deployment and Ship Checklist 🔴 Essential

### Objective

Deploy the full-stack RAG system to production with a working public URL, write EVALS.md and DECISIONS.md, and produce a portfolio-ready capstone.

### Topics Covered

1. Deploying FastAPI Backend (Railway or Render) 🔴
2. Deploying React Frontend (Vercel) 🔴
3. Environment Variables and Secrets Management 🔴
4. Health Checks and Basic Monitoring 🟡
5. Writing EVALS.md 🔴
6. Writing DECISIONS.md 🔴

### Subtopics

1. FastAPI Backend Deployment 🔴
   - Railway or Render: free tier with managed Postgres + pgvector support (Supabase, Neon, Railway)
   - Dockerize: `Dockerfile` with `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Environment variables: `OPENAI_API_KEY`, `DATABASE_URL`, `LANGFUSE_*` via platform secrets UI
   - Health endpoint: `GET /health` → `{"status": "ok"}` for uptime monitoring
2. React Frontend Deployment 🔴
   - Vercel: `vercel deploy` from the frontend directory
   - Set `VITE_API_URL` to the backend Railway/Render URL
   - CORS: ensure FastAPI allows requests from your Vercel domain
3. Secrets Management 🔴
   - Never commit `.env` files
   - Platform environment variable UIs for production secrets
   - Use `pydantic-settings` to load and validate env vars at startup
4. Health Checks and Monitoring 🟡
   - `/health` endpoint checked by platform every 30s; unhealthy → restart
   - Monitor: error rate, p95 latency, per-query cost (Langfuse dashboards)
   - Alert on: > 5% error rate, p95 latency > 3s
5. EVALS.md 🔴
   - Your quality report card
   - Document: metrics tracked, golden dataset composition, current baseline scores
   - Document known weaknesses: "multi-hop questions score 15% lower than factual"
   - Document improvement plan: what you would fix with more time
6. DECISIONS.md 🔴
   - Every architectural choice with rationale
   - Format: Context → Options Considered → Decision → Consequences
   - Required entries: chunking strategy, embedding model, vector DB choice, hybrid search rationale, reranker choice, eval framework choice
   - This artifact demonstrates engineering maturity more than the code itself

---

### Key Concepts That Need to Understand During This Lesson

- "Shipping" means publicly accessible URL, not "works on localhost"
- EVALS.md is your proof that the system works — without it, you have a demo, not a product
- DECISIONS.md is what separates engineers who implement from engineers who architect
- Secrets must never appear in code — this is a non-negotiable production standard
- The health endpoint is the first thing to add to any deployed API — platforms need it

---

### Hands-on Exercises

- Deploy backend to Railway with managed Postgres; verify `/health` returns 200
- Deploy frontend to Vercel; confirm it connects to the backend in production (not localhost)
- Write DECISIONS.md entries for at least 5 architectural choices

### Assignment

📄 Assignment File: `assignments/w08-a1-rag-capstone.md`

Short description: Ship a complete, production-grade RAG system with multi-format ingestion, hybrid search, reranking, citations, streaming React UI, RAGAS eval suite, Langfuse tracing, EVALS.md, and DECISIONS.md. Deployed and publicly accessible.

---

### Interview Preparation

**Beginner Questions**

1. What documentation should accompany a production RAG system?
2. What is DECISIONS.md and why do senior engineers write it?
3. What is the minimum viable deployment for a capstone project?

**Intermediate Questions**

1. Walk through the architecture of your RAG capstone end-to-end.
2. What are the known weaknesses of your capstone and how would you address them with more time?
3. How would you scale your RAG capstone to handle 100x more documents and queries?

---

## Week 8 Summary Checklist

- [ ] Multi-format ingestion pipeline working for PDF + markdown minimum
- [ ] Hybrid search + reranking producing measurably better results than naive retrieval (verified on eval set)
- [ ] Citations working reliably with source cards in the React UI
- [ ] Streaming responses rendering token-by-token in the React frontend
- [ ] RAGAS eval suite running with 30+ questions and all 4 core metrics
- [ ] Langfuse tracing capturing every pipeline stage with cost tracking
- [ ] Backend deployed and accessible at a public URL (Railway or Render)
- [ ] Frontend deployed and connected to backend (Vercel)
- [ ] EVALS.md written with methodology, baseline scores, and honest assessment of weaknesses
- [ ] DECISIONS.md written with every architectural choice documented (minimum 5 entries)
- [ ] Portfolio-ready: someone can visit the URL, try it, and understand what it demonstrates
- [ ] Can answer "Walk me through your RAG system" for 30 minutes in an interview

---

# Month 2 Complete ✓

You now have:

1. Deep RAG architecture fluency across five patterns: Naive, Advanced, Modular, Agentic, and GraphRAG
2. Chunking mastery: measured tradeoffs between fixed-size, recursive, semantic, parent-child, and Contextual Retrieval
3. Production retrieval stack: hybrid search (BM25 + dense + RRF) + cross-encoder reranking
4. LangGraph proficiency: stateful, conditional, cyclical workflows for any agentic pattern
5. Advanced RAG patterns implemented: HyDE, query expansion, corrective RAG, Adaptive RAG query routing
6. Eval-driven development workflow: RAGAS + LLM-as-judge + golden dataset + regression detection
7. Production observability: Langfuse tracing on every pipeline stage with cost tracking and prompt versioning
8. A deployed, evaluated, and documented RAG capstone that is portfolio-ready

**Next → Month 3: Agent Systems, MCP Implementation, Tool Use at Scale, and Production Architecture**
