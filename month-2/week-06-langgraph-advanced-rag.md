# Week 6: LangGraph + Advanced RAG

> **Month 2 -- RAG, Retrieval, Evals & Observability**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 5](./week-05-rag-architecture.md) | Next: [Week 7](./week-07-evals-observability.md)

---

## Overview

This week introduces LangGraph as your primary orchestration framework and applies it to advanced RAG patterns. You will learn LCEL as the foundation, build stateful workflows with LangGraph, and implement sophisticated retrieval patterns that go beyond simple vector lookup.

---

## Lesson 1: LangChain Expression Language (LCEL) Fundamentals

**Sub-topics:**
- LCEL pipe syntax and Runnables
- RunnablePassthrough, RunnableLambda, RunnableParallel
- Streaming with LCEL chains
- Binding tools and output parsers
- When LCEL helps vs when it adds unnecessary abstraction

**Key Concepts:**

LCEL is LangChain's declarative syntax for composing chains. At its core, it uses Python's pipe operator (`|`) to chain Runnables -- units of computation that accept input and return output. A simple RAG chain in LCEL looks like: `retriever | format_docs | prompt | llm | output_parser`. Each stage transforms the data flowing through.

The key Runnables to know: `RunnablePassthrough` passes input unchanged (useful for injecting the original query alongside retrieved docs), `RunnableLambda` wraps any Python function as a Runnable, and `RunnableParallel` runs multiple branches simultaneously. LCEL is most valuable when your chain is relatively linear. For complex branching, conditional logic, or stateful workflows, LangGraph is the better tool.

**Interview Questions:**

1. *What problem does LCEL solve?*
   It provides a composable, streamable interface for chaining LLM operations. Each component implements the same Runnable interface, so you get streaming, batching, and async support automatically without writing boilerplate.

2. *When would you use raw Python functions instead of LCEL?*
   When the logic is simple and linear enough that the pipe abstraction adds complexity without benefit, or when you need fine-grained error handling that is easier to express in vanilla Python try/except blocks.

---

## Lesson 2: LangGraph for Stateful Workflows

**Sub-topics:**
- Graph concepts: nodes, edges, conditional edges
- State management with TypedDict or Pydantic models
- Conditional routing based on state
- Cycles and iterative processing
- Checkpointing and persistence
- LangGraph vs LCEL: when to reach for which

**Key Concepts:**

LangGraph models workflows as directed graphs where nodes are processing steps and edges define data flow. Unlike LCEL's linear chains, LangGraph supports cycles -- a node can route back to a previous node based on conditions. This is critical for patterns like corrective RAG, where a bad retrieval triggers a re-query loop.

State is the backbone: you define a TypedDict (or Pydantic model) that holds everything the graph needs. Each node reads from state, does its work, and returns a partial state update. LangGraph merges these updates automatically. Conditional edges inspect the current state and route to the appropriate next node. This makes complex workflows readable: the graph structure itself documents the logic flow.

**Interview Questions:**

1. *How does LangGraph differ from a simple chain?*
   LangGraph supports cycles, conditional routing, and persistent state. A chain is linear -- data flows one direction. LangGraph can loop, branch, and make dynamic decisions, which is necessary for agents and corrective patterns.

2. *What is the role of state in LangGraph?*
   State is a shared data structure (TypedDict) that nodes read from and write to. It carries context across the graph -- retrieved documents, query reformulations, quality scores, iteration counts. Each node returns partial updates that LangGraph merges into the full state.

3. *When should you use LangGraph over LCEL?*
   When your workflow needs conditional branching, cycles (retry loops), multi-step reasoning with state tracking, or human-in-the-loop approval gates. LCEL is better for simple, linear retrieve-and-generate chains.

---

## Lesson 3: Advanced RAG Patterns

**Sub-topics:**
- Query expansion (generate multiple query variants)
- HyDE (Hypothetical Document Embeddings)
- Multi-query retrieval (parallel queries, deduplicated results)
- Step-back prompting (abstract the question first)
- Corrective RAG (detect bad retrievals, re-query)
- Adaptive RAG (route to different strategies based on query type)
- Self-RAG (LLM grades its own retrieval and generation)

**Key Concepts:**

Query expansion addresses the vocabulary gap between how users phrase questions and how documents express answers. Instead of searching with the raw query, you generate 3-5 reformulations and search with all of them, deduplicating the results. HyDE takes a different approach: ask the LLM to generate a hypothetical answer (without retrieval), then use that answer as the search query. Since the hypothetical answer is in "document language," it often retrieves better results than the original question.

Corrective RAG adds a quality check after retrieval. A grading step (often LLM-as-judge) evaluates whether the retrieved documents actually answer the query. If the grade is low, the system can: rewrite the query and retry, fall back to web search, or escalate to the user. This is a natural fit for LangGraph's conditional edges -- the grading node routes to either "generate answer" or "retry retrieval."

**Interview Questions:**

1. *Explain the HyDE pattern and when it helps.*
   HyDE asks the LLM to generate a hypothetical answer without any retrieval, then embeds that answer to search for real documents. It helps when user queries are short or use different terminology than the documents, since the hypothetical answer bridges the vocabulary gap.

2. *How does Corrective RAG prevent hallucination?*
   After retrieval, a grading step checks document relevance. If retrieved documents are irrelevant, the system re-queries or uses fallback sources instead of forcing the LLM to generate from bad context, which would cause hallucination.

---

## Lesson 4: Query Routing

**Sub-topics:**
- Semantic routing (classify query intent, route to appropriate pipeline)
- Routing by data source (different retrievers for different document types)
- LLM-based routing vs embedding-based classification
- Fallback strategies when routing fails
- Implementation with LangGraph conditional edges

**Key Concepts:**

Not all queries should go through the same pipeline. A factual lookup ("What is the API rate limit?") needs precise retrieval, while a conceptual question ("How do transformers work?") benefits from broader context. Query routing classifies the incoming query and dispatches it to the appropriate retrieval strategy.

You can implement routing with an LLM call (classify the query into categories) or with embedding similarity (compare the query embedding to category exemplars). LLM-based routing is more flexible but adds latency and cost; embedding-based routing is faster but requires pre-defined categories with examples. In LangGraph, routing is a conditional edge: the router node outputs a category, and the conditional edge maps categories to downstream nodes.

**Interview Questions:**

1. *Why route queries instead of using one pipeline for everything?*
   Different query types have different optimal retrieval strategies. A keyword-heavy query benefits from BM25, a semantic question from dense retrieval, and a multi-hop question from iterative retrieval. Routing lets you optimize each path instead of compromising on a one-size-fits-all approach.

---

## Lesson 5: Caching Strategies

**Sub-topics:**
- Exact match caching (hash-based, Redis)
- Semantic caching (similar queries hit cache)
- Embedding cache (avoid re-embedding identical documents)
- LLM response caching (prompt + model + params as key)
- Cache invalidation when documents update
- Cost savings calculation

**Key Concepts:**

Caching is a straightforward cost and latency optimization. Exact match caching stores query-response pairs keyed by the query hash. Semantic caching is more powerful: embed each query and check if a cached query exists within a similarity threshold. If so, return the cached response. This handles paraphrased questions that should get the same answer.

For RAG systems, the biggest caching opportunity is often at the embedding stage. If your document corpus does not change frequently, pre-computed embeddings eliminate the most expensive repeated computation. LLM response caching is useful for deterministic queries (temperature=0, same prompt) but requires careful invalidation when the underlying documents or prompts change.

**Interview Questions:**

1. *What is semantic caching and when is it appropriate?*
   Semantic caching embeds queries and returns cached responses for semantically similar (not just identical) queries. It is appropriate when many users ask similar questions in different words, and the underlying data does not change frequently. It is inappropriate when answers are highly personalized or time-sensitive.

---

## Assignment: Advanced RAG Pipeline with LangGraph

**Objective:** Build an advanced RAG pipeline using LangGraph that implements query routing and re-ranking.

**Requirements:**
- Define a LangGraph state schema with query, retrieved docs, quality score, route, and answer
- Implement a query router node (at least 2 routes: "factual lookup" and "conceptual explanation")
- Each route uses a different retrieval strategy (e.g., hybrid search vs pure dense)
- Add a re-ranking step using Cohere Rerank or a cross-encoder
- Implement corrective RAG: grade retrieved docs, re-query if below threshold
- Use the corpus from Week 5's assignment
- Visualize the graph with `graph.get_graph().draw_mermaid()`

**Stretch goals:**
- Add HyDE as an option for the conceptual route
- Implement semantic caching with Redis
- Add a "no answer" pathway when retrieval quality is too low even after retry

---

## Summary Checklist

- [ ] Can write LCEL chains and know when to reach for LangGraph instead
- [ ] Built a LangGraph workflow with nodes, edges, conditional routing, and state
- [ ] Implemented at least 3 advanced RAG patterns (query expansion, HyDE, corrective)
- [ ] Query routing working with 2+ routes to different retrieval strategies
- [ ] Understand caching strategies and their cost/latency impact
- [ ] Completed assignment: LangGraph pipeline with routing + re-ranking
- [ ] System design sketch: multi-strategy RAG system for a heterogeneous corpus
- [ ] Weekly writing: 1 post about LangGraph or an advanced RAG pattern
