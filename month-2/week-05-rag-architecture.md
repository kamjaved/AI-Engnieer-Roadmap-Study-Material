# Week 5: RAG Architecture Patterns

> **Month 2 -- RAG, Retrieval, Evals & Observability**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 4](../month-1/week-04-embeddings-vector-search.md) | Next: [Week 6](./week-06-langgraph-advanced-rag.md)

---

## Overview

This week transitions from basic retrieval into production RAG architecture. You will learn the spectrum of RAG patterns, master multiple chunking strategies with measurable tradeoffs, implement hybrid search, build document processing pipelines for real-world formats, and get introduced to re-ranking as a retrieval quality multiplier.

---

## Lesson 1: RAG Architecture Patterns

**Sub-topics:**
- Naive RAG (embed-retrieve-generate) and its limitations
- Advanced RAG (pre-retrieval optimization, post-retrieval refinement)
- Modular RAG (pluggable components: retriever, reranker, generator as interchangeable modules)
- Agentic RAG (LLM decides when and how to retrieve, iterative retrieval)
- Choosing the right pattern for a given use case

**Key Concepts:**

Naive RAG follows a linear pipeline: chunk documents, embed them, retrieve top-k by similarity, and feed them into an LLM. This works for simple cases but breaks down when queries are ambiguous, documents are noisy, or the answer requires synthesis across multiple sources. Advanced RAG addresses this by adding stages -- query rewriting before retrieval, re-ranking after retrieval, and citation extraction during generation.

Modular RAG takes this further by treating each stage as a swappable component. You can mix dense retrieval with sparse retrieval, swap rerankers, or change generators without rewriting the pipeline. Agentic RAG gives the LLM itself control over the retrieval process -- it can decide to search again with a refined query, skip retrieval entirely for factual questions it already knows, or combine results from multiple sources iteratively.

**Interview Questions:**

1. *What is the difference between Naive RAG and Advanced RAG?*
   Naive RAG is a single-pass pipeline (retrieve then generate). Advanced RAG adds pre-retrieval steps like query expansion and post-retrieval steps like re-ranking and answer verification to improve quality.

2. *When would you choose Agentic RAG over a static pipeline?*
   When queries are diverse and require different retrieval strategies, when multi-hop reasoning is needed, or when the system must decide dynamically whether retrieval is even necessary.

3. *What are the failure modes of Naive RAG?*
   Poor retrieval due to query-document mismatch, context window pollution with irrelevant chunks, hallucination when retrieved context is insufficient, and inability to handle queries requiring multi-step reasoning.

---

## Lesson 2: Chunking Strategies Deep Dive

**Sub-topics:**
- Fixed-size chunking (character/token count with overlap)
- Recursive chunking (split by structure: paragraphs, sentences, then characters)
- Semantic chunking (split by embedding similarity between consecutive sentences)
- Parent-child chunking (retrieve child, return parent for context)
- Hierarchical chunking (document > section > paragraph, with metadata at each level)
- Chunk size tradeoffs: precision vs recall vs cost

**Key Concepts:**

Chunking is arguably the most impactful decision in a RAG pipeline. Fixed-size chunks are simple but break semantic boundaries -- a paragraph about pricing might get split across two chunks, losing coherence. Recursive chunking respects document structure by splitting on natural boundaries first. Semantic chunking uses embeddings to detect topic shifts, creating chunks that are topically coherent.

Parent-child chunking is a powerful pattern: you embed small, precise child chunks for retrieval accuracy, but when a child matches, you return the larger parent chunk to give the LLM more context. This solves the classic tension between retrieval precision (small chunks) and generation quality (more context). Hierarchical chunking adds metadata at each level so you can filter by section headers or document structure before doing vector search.

**Interview Questions:**

1. *Why not just use large chunks to give the LLM more context?*
   Large chunks dilute the embedding signal -- a 2000-token chunk about multiple topics will poorly match a specific query. They also consume more of the context window, increasing cost and potentially confusing the model with irrelevant information.

2. *Explain the parent-child chunking strategy.*
   Embed small child chunks (e.g., 200 tokens) for precise retrieval. When a child matches, return its parent chunk (e.g., the full section, 1000 tokens) to the LLM so it has enough surrounding context for a coherent answer.

---

## Lesson 3: Hybrid Search

**Sub-topics:**
- Dense retrieval (vector similarity) strengths and weaknesses
- Sparse retrieval (BM25 / TF-IDF) strengths and weaknesses
- Reciprocal Rank Fusion (RRF) for combining results
- When hybrid outperforms pure dense search
- Implementation with libraries (rank_bm25 + vector DB)

**Key Concepts:**

Dense retrieval excels at semantic similarity -- it understands that "automobile" and "car" are related. But it struggles with exact keyword matches, rare terms, and structured queries like product IDs or error codes. BM25 (sparse retrieval) handles these cases well because it does exact lexical matching with term frequency weighting. Hybrid search combines both: run the query through dense and sparse retrievers, then merge results using Reciprocal Rank Fusion, which weights items by their rank position across both lists.

In practice, hybrid search provides a measurable improvement (typically 5-15% in recall) over either method alone, particularly on heterogeneous document collections where some queries are keyword-heavy and others are semantic.

**Interview Questions:**

1. *When does BM25 outperform dense retrieval?*
   For exact keyword searches, domain-specific jargon, product codes, error messages, and queries where the user knows the exact terminology. BM25 is also better when you have very little training data for the embedding model.

---

## Lesson 4: Document Processing Pipelines

**Sub-topics:**
- PDF extraction (PyMuPDF, pdfplumber, Unstructured)
- Markdown and HTML parsing (preserving structure)
- Table extraction and structured data handling
- Image and diagram handling (OCR, vision model descriptions)
- Metadata extraction (title, author, date, section headers)
- Handling messy real-world documents

**Key Concepts:**

Real-world documents are messy. PDFs contain tables that break across pages, headers and footers that pollute text extraction, and embedded images with critical information. A production document pipeline must handle all these cases. The Unstructured library is the current best option for multi-format ingestion -- it detects document elements (titles, text, tables, images) and preserves structure.

Tables require special handling: you can serialize them as markdown, extract them as structured data, or describe them in natural language for embedding. The choice depends on your query patterns. For mixed-format corpora, maintaining provenance metadata (source file, page number, section) is critical for citation and debugging.

**Interview Questions:**

1. *How do you handle tables in a RAG pipeline?*
   Options include: serializing as markdown for embedding, extracting as structured JSON for programmatic queries, or using a vision model to describe the table in natural language. The best approach depends on query patterns -- markdown works for general questions, structured extraction for specific lookups.

---

## Lesson 5: Re-ranking Introduction

**Sub-topics:**
- Why initial retrieval is approximate (bi-encoder limitations)
- Cross-encoder re-ranking (how it works, why it is more accurate)
- Cohere Rerank API
- Open-source cross-encoders (sentence-transformers)
- Cost/latency tradeoffs of re-ranking

**Key Concepts:**

Bi-encoder models (used for initial retrieval) encode queries and documents independently, then compare with a fast similarity metric. This is efficient but loses nuance. Cross-encoder re-rankers process the query and each candidate document together, allowing direct token-level interaction. This is far more accurate but computationally expensive -- you cannot run it over millions of documents.

The standard pattern is a two-stage pipeline: retrieve top-50 or top-100 with a fast bi-encoder, then re-rank that shortlist with a cross-encoder to get the best top-5. Cohere Rerank provides a hosted cross-encoder API that is easy to integrate. For open-source, the `cross-encoder/ms-marco-MiniLM-L-6-v2` model is a solid starting point.

**Interview Questions:**

1. *Why use a two-stage retrieval pipeline instead of just a more accurate retriever?*
   Cross-encoders are O(n) with the number of candidates because they process each query-document pair together. Running them over millions of documents is too slow. A fast bi-encoder narrows the field to a manageable shortlist that the cross-encoder can re-rank accurately.

---

## Assignment: Chunking Strategy Comparison

**Objective:** Build 3 chunking strategies and measure retrieval precision on the same corpus.

**Requirements:**
- Select a corpus of at least 20 documents (technical docs, Wikipedia articles, or your own)
- Implement fixed-size (512 tokens, 128 overlap), recursive (by paragraph/sentence), and semantic chunking
- Embed all three using the same embedding model (e.g., OpenAI text-embedding-3-small)
- Create 15 test queries with known relevant passages (golden set)
- Measure Precision@5 and Recall@5 for each strategy
- Write up which strategy won and why in a DECISIONS.md

**Stretch goals:**
- Add parent-child chunking as a 4th strategy
- Implement hybrid search (BM25 + dense) on the best chunking strategy
- Visualize chunk boundary quality (show where semantic vs fixed splits differ)

---

## Summary Checklist

- [ ] Can explain 4 RAG architecture patterns and when to use each
- [ ] Implemented 3+ chunking strategies with measurable precision/recall
- [ ] Understand hybrid search (dense + BM25) and Reciprocal Rank Fusion
- [ ] Built a document processing pipeline for at least 2 formats (PDF + markdown)
- [ ] Understand cross-encoder re-ranking and the two-stage retrieval pattern
- [ ] Completed assignment with DECISIONS.md documenting chunking choice rationale
- [ ] System design sketch: RAG pipeline for a 10K-document knowledge base
- [ ] Weekly writing: 1 post about a chunking or retrieval insight
