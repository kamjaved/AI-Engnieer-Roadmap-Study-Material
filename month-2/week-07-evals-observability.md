# Week 7: Evals & Observability

> **Month 2 -- RAG, Retrieval, Evals & Observability**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 6](./week-06-langgraph-advanced-rag.md) | Next: [Week 8](./week-08-rag-capstone.md)

---

## Overview

This is the most important week of the entire roadmap. Evals are the differentiator between a demo and a product, and in 2026, eval fluency is the strongest hiring signal for GenAI engineers. This week covers why evals matter, how to build them, the RAGAS framework, LLM-as-judge patterns, and Langfuse for production observability. You will leave this week with a working eval harness that you will use in every project going forward.

---

## Lesson 1: Why Evals Matter

**Sub-topics:**
- The 2026 hiring signal: "How do you evaluate your systems?"
- The gap between "vibes-based" and "metrics-driven" development
- Evals as guardrails, regression tests, and improvement drivers
- Eval-driven development: write evals before building features
- Real-world examples of systems that failed due to missing evals

**Key Concepts:**

Most GenAI tutorials skip evaluation entirely. The result is developers who can build impressive demos but cannot answer "How do you know this works?" or "How did the last change affect quality?" In production, you need to detect when a prompt change improves faithfulness but hurts relevancy, when a new embedding model helps for technical queries but hurts for conversational ones, or when a reranker adds latency without improving answer quality.

Evals are not a phase at the end of development -- they are the foundation. The eval-driven development cycle is: define what "good" looks like (golden QA pairs + metrics), measure your baseline, make a change, measure again, ship only if metrics improve. This is the workflow that senior GenAI engineers use daily, and it is the first thing interviewers probe for.

**Interview Questions:**

1. *How do you evaluate a RAG system?*
   Use a combination of retrieval metrics (precision, recall, MRR) and generation metrics (faithfulness, answer relevancy, answer correctness). Build a golden dataset of question-answer-context triples. Use RAGAS for automated scoring and LLM-as-judge for nuanced quality assessment. Track all metrics in Langfuse to detect regressions.

2. *What is the difference between offline and online evals?*
   Offline evals run on a fixed golden dataset before deployment -- they catch regressions. Online evals measure live user interactions -- thumbs up/down, time-to-resolution, follow-up question rate. You need both: offline for gating deployments, online for catching issues the golden dataset missed.

3. *How do you build a golden evaluation dataset?*
   Start with 30-50 diverse questions that represent real user queries. For each question, provide the expected answer and the relevant source passages. Include edge cases: ambiguous queries, questions with no answer in the corpus, multi-hop questions. Have domain experts validate the dataset. Expand it as you discover new failure modes.

---

## Lesson 2: Eval Types

**Sub-topics:**
- Offline evals (pre-deployment, golden dataset)
- Online evals (production feedback signals)
- Regression evals (did the last change break something?)
- A/B testing for GenAI (prompt variants, model swaps)
- Component-level vs end-to-end evals

**Key Concepts:**

A mature eval system has three layers. Component evals test individual stages: retrieval precision, reranker effectiveness, prompt quality. End-to-end evals test the full pipeline: given a question, is the final answer correct and well-cited? Regression evals run the full suite after every change to catch degradation.

The critical insight is that improving one component can degrade the overall system. A better reranker might surface different documents that your generation prompt was not optimized for. Only end-to-end evals catch these interaction effects. Run both component and end-to-end evals, and always check end-to-end metrics before shipping.

**Interview Questions:**

1. *Why run component-level evals in addition to end-to-end?*
   End-to-end evals tell you something is broken but not where. Component evals pinpoint the issue -- is it retrieval, reranking, or generation? This speeds up debugging. However, you must also run end-to-end evals because component improvements can cause unexpected regressions in the full pipeline.

---

## Lesson 3: Building Eval Datasets and Metrics

**Sub-topics:**
- Golden QA pairs: structure, diversity, and edge cases
- Synthetic dataset generation (LLM-generated questions from your corpus)
- Retrieval metrics: Precision@k, Recall@k, MRR, NDCG
- Generation metrics: faithfulness, relevancy, correctness, harmfulness
- Custom metrics for domain-specific requirements
- Statistical significance: when is an improvement real?

**Key Concepts:**

Your eval dataset must be representative and diverse. Include straightforward factual questions, questions requiring multi-chunk synthesis, questions with no answer in the corpus (testing the system's ability to say "I don't know"), adversarial questions that test guardrails, and paraphrased versions of the same question (testing consistency).

For metrics, the core four are: **Faithfulness** (is the answer grounded in the retrieved context?), **Answer Relevancy** (does the answer address the question?), **Context Precision** (are the retrieved documents relevant?), and **Context Recall** (were all necessary documents retrieved?). These four together give a comprehensive view of both retrieval and generation quality.

**Interview Questions:**

1. *What does faithfulness measure and why is it critical?*
   Faithfulness measures whether the generated answer is supported by the retrieved context. It detects hallucination -- when the LLM generates plausible-sounding information that is not in the source documents. This is the most critical metric because hallucination erodes user trust.

2. *How do you handle questions with no answer in the corpus?*
   Include "unanswerable" questions in your eval set and measure how often the system correctly responds with "I don't know" or equivalent. A system that always attempts an answer, even without supporting evidence, will hallucinate on these cases.

---

## Lesson 4: RAGAS Framework

**Sub-topics:**
- RAGAS architecture and philosophy
- Supported metrics: faithfulness, answer_relevancy, context_precision, context_recall
- Running RAGAS on your dataset (code walkthrough)
- Interpreting RAGAS scores
- Limitations of RAGAS (cost, LLM dependency, metric correlations)
- Alternatives: DeepEval, custom eval scripts

**Key Concepts:**

RAGAS (Retrieval-Augmented Generation Assessment) is the standard framework for evaluating RAG systems. It uses LLM-as-judge under the hood: for each metric, it constructs a specific prompt that asks an LLM to evaluate a particular quality dimension. For example, for faithfulness, it extracts claims from the generated answer and checks each claim against the retrieved context.

Running RAGAS requires a dataset of (question, answer, contexts, ground_truth) tuples. You call `evaluate()` with your dataset and selected metrics, and it returns scores per sample and aggregated. A typical workflow: run RAGAS after every change, compare scores against your baseline, and only deploy if scores improve or hold steady. Be aware that RAGAS costs money (LLM calls per evaluation) and can have variance -- run multiple times and average if making close decisions.

**Interview Questions:**

1. *How does RAGAS measure faithfulness?*
   It extracts individual claims/statements from the generated answer, then checks each claim against the retrieved context to determine if it is supported. The faithfulness score is the ratio of supported claims to total claims.

2. *What are the limitations of using RAGAS?*
   It depends on LLM quality for judging (garbage in, garbage out), it costs money per eval run, scores can have variance between runs, and it may not capture domain-specific quality dimensions. Use it as a foundation, supplement with custom metrics for your domain.

---

## Lesson 5: LLM-as-Judge Pattern

**Sub-topics:**
- Using an LLM to evaluate LLM output (meta-evaluation)
- Designing judge prompts (rubrics, scoring criteria, examples)
- Pairwise comparison vs absolute scoring
- Reducing judge bias (position bias, verbosity bias, self-preference)
- When to use LLM-as-judge vs human evaluation vs programmatic metrics

**Key Concepts:**

LLM-as-judge uses a separate LLM call (often a stronger model like GPT-4 or Claude) to evaluate the quality of a generated response. You provide the judge with the question, retrieved context, generated answer, and a detailed rubric. The judge scores on dimensions you define: accuracy, completeness, tone, citation quality, etc.

The key to reliable LLM-as-judge is the rubric. Vague instructions like "rate quality 1-5" produce inconsistent results. Instead, define exactly what each score means: "5 = all claims are factually supported by context with specific citations; 3 = mostly correct but missing one key point; 1 = contains hallucinated claims." Include examples of each score level. For critical decisions, use pairwise comparison ("Is answer A better than answer B?") which is more reliable than absolute scoring.

**Interview Questions:**

1. *How do you make LLM-as-judge evaluations reliable?*
   Use detailed rubrics with score definitions and examples. Use pairwise comparison for high-stakes decisions. Average across multiple judge runs. Validate judge scores against human annotations on a subset. Use a stronger model than the one being evaluated.

---

## Lesson 6: Langfuse for Observability & Tracing

**Sub-topics:**
- Why observability matters for LLM applications
- Langfuse architecture: traces, spans, generations, scores
- Instrumenting your RAG pipeline with Langfuse
- Cost tracking per query, per user, per feature
- Prompt versioning and management
- Building dashboards for monitoring quality over time
- Comparing Langfuse alternatives (LangSmith, Phoenix, Helicone)

**Key Concepts:**

Observability in GenAI applications means being able to trace every query through the full pipeline: what was retrieved, how it was reranked, what prompt was sent to the LLM, what the LLM returned, and how long/costly each step was. Langfuse provides this with a decorator-based API: wrap your functions with `@observe()` and Langfuse automatically captures inputs, outputs, latency, and cost.

Beyond tracing, Langfuse enables prompt versioning (track which prompt version produced which results), cost tracking (know your per-query and per-user costs), and score aggregation (plot faithfulness scores over time). This creates a feedback loop: observe production behavior, identify failure patterns, improve your pipeline, verify improvement with evals.

**Interview Questions:**

1. *What would you trace in a production RAG system?*
   Every stage: query preprocessing (routing, expansion), retrieval (which documents, similarity scores), reranking (score changes, documents dropped/promoted), prompt assembly (template version, token count), LLM generation (model, latency, cost, tokens), and post-processing (citation extraction, output validation). Also trace user feedback signals.

2. *How do you use observability data to improve a RAG system?*
   Identify patterns in low-scoring queries -- common failure modes like missing document types, ambiguous queries that confuse the router, or prompts that cause hallucination on certain topics. Use these patterns to expand your eval dataset, refine your chunking/retrieval, and improve your prompts.

---

## Assignment: 30-Question Eval Harness with Langfuse

**Objective:** Build a comprehensive eval harness for your RAG system and integrate Langfuse tracing.

**Requirements:**
- Create a golden dataset of 30 question-answer-context triples covering:
  - 15 straightforward factual questions
  - 5 multi-chunk synthesis questions
  - 5 questions with no answer in the corpus
  - 5 adversarial/edge case questions
- Implement RAGAS evaluation (faithfulness, answer_relevancy, context_precision, context_recall)
- Implement at least 1 custom LLM-as-judge metric (e.g., citation quality)
- Integrate Langfuse tracing into your Week 5/6 RAG pipeline
- Run the eval suite and produce a baseline scorecard
- Create a simple dashboard (can be a notebook or streamlit) showing metrics over time

**Stretch goals:**
- Add regression detection: alert when any metric drops >5% from baseline
- Implement cost-per-query tracking in Langfuse
- Build a prompt versioning workflow: test new prompts against the eval suite before deploying
- Generate synthetic eval questions from your corpus using an LLM

---

## Summary Checklist

- [ ] Can articulate why evals are the #1 hiring signal for GenAI engineers in 2026
- [ ] Understand the difference between offline, online, and regression evals
- [ ] Built a golden eval dataset of 30+ questions with diverse categories
- [ ] Can run RAGAS and interpret faithfulness, relevancy, precision, and recall scores
- [ ] Implemented LLM-as-judge with a detailed rubric
- [ ] Langfuse integrated and tracing queries end-to-end
- [ ] Baseline scorecard established for your RAG pipeline
- [ ] Understand cost tracking and prompt versioning workflows
- [ ] Completed assignment with working eval harness + Langfuse tracing
- [ ] System design sketch: eval pipeline for a production GenAI application
- [ ] Weekly writing: 1 post about why evals matter or what you learned building your harness
