# Interview Prep — Project 2: Internal GenAI Knowledge Assistant Initiative

> Prep material only — not resume content, and not to be read aloud verbatim. Framed as a team-based internal engineering initiative (not a client engagement, not a personal project). Every technical detail below is grounded in your actual RAG and Memory/Checkpointing crash-course builds. Written entirely in English, as requested. No client, product, or confidential names are used anywhere.

---

## 1. How to introduce it (30 seconds)

"Alongside my client delivery work, I was part of an internal team that built a GenAI knowledge assistant for internal use — the idea was to let employees ask natural-language questions against our internal documentation (policies, process guides, product/service references) instead of searching through folders or wikis. It was a small cross-functional build: a tech lead who owned the overall agent architecture, an engineer handling the vector infrastructure, another on the internal UI, and I owned the retrieval pipeline and evaluation, plus the API layer that tied retrieval, generation, and memory together for the assistant."

That last sentence is the one to get comfortable saying without hesitation — it's specific, it's bounded, and it matches everything below it.

---

## 2. Team and Scope — what I owned vs. what I didn't

Say this plainly if asked "what exactly was your contribution" — a precise answer here is what makes the rest of the story credible.

**What I owned:**
- The retrieval pipeline: chunking strategy (including evaluating parent-child chunking against plain recursive chunking), and building hybrid retrieval — combining dense vector search with a BM25 keyword retriever via Reciprocal Rank Fusion, plus experimenting with HyDE query transformation for vague queries.
- The evaluation harness: a RAGAS-based evaluation pipeline (context precision, context recall, faithfulness, answer relevancy) against a hand-curated question set, so retrieval and generation changes could be measured, not just eyeballed.
- The FastAPI service layer connecting retrieval, generation, and memory into one request path — this fell to me largely because of my backend/full-stack background relative to the rest of the team.

**What I contributed to, but didn't own outright:**
- Long-term memory: I implemented the classification-and-storage piece (deciding which facts from a conversation were durable enough to persist across sessions) inside an architecture our tech lead had already designed.
- Debugging: I was the one who traced a real checkpoint-accumulation bug during integration testing (below), even though the checkpointing design itself belonged to the tech lead.

**What I did not own:**
- The overall LangGraph agent design and the Postgres checkpointing setup (`AsyncPostgresSaver`, the checkpoint schema) — that was our tech lead's design. I worked inside it and understand it well enough to explain and debug it, but I didn't architect it from scratch.
- Vector infrastructure provisioning (the Pinecone index setup, embedding model selection) — owned by another engineer on the team; I consumed that infrastructure through a retrieval interface.
- The internal front-end UI — a separate engineer's scope; I only own the API contract it talks to.

If an interviewer asks "so you built the whole RAG-plus-memory system yourself?" — the honest, better answer is: "No — I owned retrieval and evaluation end-to-end, and the API integration layer; memory and checkpointing architecture was a teammate's design that I worked inside of and helped debug." That answer is *more* convincing than claiming solo ownership of everything, not less.

---

## 3. The System — walked through from my actual vantage point

### 3.1 What the assistant needed to do

The goal was straightforward to state, harder to get right: answer employee questions grounded only in our internal documents, cite what it used, and say "I don't have that in the knowledge base" instead of guessing when the docs didn't have the answer. Documents were a mix of markdown and PDF — policy docs, process guides, a product/service reference set.

### 3.2 The retrieval pipeline (my primary area)

Ingestion loaded both file types into a common `Document` shape with metadata attached at load time (source, team/category, doc type) — attaching it at load time mattered because chunking later just copies whatever metadata already exists forward; it doesn't invent it.

For chunking, I evaluated plain recursive character-based splitting against parent-child chunking. Recursive splitting is simple and works well for prose, but I found it has a real failure mode: on structured content — tables, a heading immediately followed by a long section — the splitter can strand a heading alone in its own tiny, meaningless chunk purely on character-count boundary luck. Parent-child chunking (a small child chunk for search, a larger linked parent for context) reduces that risk, but I want to be precise here rather than oversell it: it reduces the risk, it doesn't eliminate it, because the parent splitter is still character-count-driven at a bigger window. I saw this directly — a parent chunk that was still missing a table's header row on one test case.

For retrieval itself, I didn't stop at plain dense vector search. I built a hybrid retriever — dense (vector similarity) plus BM25 (keyword/sparse), fused with Reciprocal Rank Fusion, which combines ranked lists using rank position rather than raw scores, so it works even though dense cosine scores and BM25 scores live on completely different, incomparable scales. Dense retrieval is strong on paraphrased, natural-language questions; BM25 is strong when a query contains an exact term (a specific policy name, a product name) that dense retrieval can under-weight. I also experimented with HyDE — generating a hypothetical, possibly-wrong-but-plausible answer with an LLM first, then embedding *that* to search, because a hypothetical answer reads like document language, while a short user question often doesn't.

### 3.3 The evaluation harness (my primary area)

Retrieval quality is not something you can eyeball reliably, so I built a RAGAS-based evaluation pass — context precision and context recall on the retrieval side, faithfulness and answer relevancy on the generation side — run against a small, hand-written set of question/reference pairs the team put together from real documents. I kept retrieval and generation metrics conceptually separate on purpose: a low-faithfulness score with good retrieval means the model is ignoring good context; a low-context-precision score means retrieval itself needs work — and those two failure modes need completely different fixes.

### 3.4 The API/service layer (my primary area)

I built the FastAPI layer that tied everything together for a single request: retrieve, assemble a grounded prompt with numbered, citable sources, generate an answer, and return both the answer and the raw retrieved chunks — not just the final text — specifically so a wrong answer could be diagnosed as a retrieval failure or a generation failure, rather than guessed at.

### 3.5 Memory and checkpointing (teammate's architecture, my integration work)

The agent ran on LangGraph with Postgres-backed checkpointing (`AsyncPostgresSaver`) for crash recovery — that architecture belonged to our tech lead. What I want to be accurate about: checkpointing gives you crash-recovery, not memory management — a checkpoint has no concept of tokens or context-window limits, it just persists whatever state exists. So the team layered short-term memory (rolling summarization once a conversation crossed a message-count/token threshold) and long-term memory (durable, cross-session facts) on top of that, as a separate concern from checkpointing itself.

My specific piece here was the long-term memory classification-and-storage component: an LLM call classifies whether a given exchange contains a durable fact worth remembering across sessions (a stated preference, for instance) versus something to ignore, and persists it against the user rather than the conversation thread, so it's available in a completely different, later conversation.

---

## 4. Real Problems I Actually Faced (use these for "tell me about a bug you debugged")

### Problem 1 — A checkpoint accumulation bug that silently defeated summarization

During integration testing, I noticed conversations that should have been getting shorter (thanks to summarization) were instead sending more and more tokens to the model every turn, quietly, with no error. I traced it to an interaction between two systems that weren't originally designed to run together this way: the checkpointer was keeping its own accumulating copy of message history under a stable thread ID (via LangGraph's `add_messages` reducer, which only ever appends, never replaces), while a separate summarization step was assembling its *own* trimmed context and sending that to the model. Every turn, the trimmed context was landing on top of the checkpoint's already-growing history instead of replacing it.

It took a while to find, specifically because every check at the persistence layer looked correct — summaries were being written, counts matched expectations. The bug only became visible once I inspected what was actually being sent to the LLM on a given call, not just what was in the database.

The fix the team landed on was scoping the checkpoint's thread identity per-turn (rather than reusing one stable ID across a whole conversation), so the checkpoint never had anything to accumulate in the first place, and cross-turn memory became exclusively the Postgres summarization/long-term-memory layer's job. That was a real trade-off, not a clean win: it means we gave up true crash-resume in the middle of a single turn (a narrower, more acceptable risk for a synchronous request than losing an entire conversation's memory).

### Problem 2 — Retrieval quality issues that initially looked random

Two separate, non-obvious issues surfaced during testing. First, some retrieved chunks were oddly tiny and useless — turned out to be section headings that got stranded alone by the splitter purely due to character-count boundaries, not a bug in the splitting logic itself. Second, one PDF's extracted text had a stray space inserted mid-word (a kerning artifact from the PDF itself, not a typo in the source document) that made a naive exact-text search silently fail to find an obviously-relevant chunk.

Both were fixed at the right layer rather than papered over: chunking strategy (parent-child, with the honest caveat that it reduces rather than eliminates the risk) for the first, and normalizing whitespace before any text comparison for the second.

### Problem 3 — Realizing a retrieval score isn't a trustworthy confidence signal

While debugging a wrong answer, I found the *highest*-scoring retrieved chunk for that query wasn't actually the one that contained the right information — it scored highest mostly on keyword overlap with the question, not on actually answering it. That's the reason the API layer returns raw retrieved chunks alongside every answer: a cosine similarity score is useful for comparing candidates *within* one query, but it's not a calibrated correctness signal you can trust across queries or show to an end user as "confidence."

---

## 5. Trade-offs and Why-Not-X Question Bank

**"Why hybrid retrieval with two separate retrievers and Reciprocal Rank Fusion, instead of your vector database's native hybrid search?"**
Because it's pure application-side code — it doesn't require migrating the existing vector index's schema or metric, which mattered given the index was already live with other consumers. The trade-off is real: you run two retrieval calls instead of one, and there's no server-side tunable weighting between dense and sparse the way a native hybrid mode might offer. RRF needing no tuned weights (it only uses rank position) made that an acceptable trade for us at this scale.

**"Why didn't you add a reranker on top of retrieval?"**
That's an honest gap, not an oversight I'm hiding — a cross-encoder reranker on the initially-retrieved candidates was identified as the natural next step (narrow, precise re-scoring of an already-narrowed candidate set) but wasn't built in the phase I worked on. It's the clear next item if I were continuing the work.

**"Why parent-child chunking instead of just increasing chunk size?"**
Because bigger chunks don't just help — they dilute both retrieval (the embedding starts representing an average of multiple ideas instead of one) and generation (more irrelevant surrounding text competing for the model's attention, at higher token cost). Parent-child keeps the searchable unit small and precise while giving generation a larger, linked context only when that specific chunk is retrieved — though as noted above, it reduces rather than eliminates the risk of losing structural context like table headers.

**"Why build BM25 by hand instead of using your vector store's built-in hybrid feature, if you're already paying for the vector database?"**
Same schema-migration reasoning as above, plus the vector database's hybrid offering wasn't something we'd validated for our specific document shapes (a lot of structured/tabular content) at the time — the in-memory BM25 approach let us validate whether hybrid retrieval helped at all, cheaply, before considering a heavier infrastructure change.

**"Why RAGAS instead of just having people manually review answers?"**
Manual review doesn't scale past a handful of test cases and doesn't survive being re-run after every change — which is exactly what you need when you're iterating on chunking, retrieval, or prompts. RAGAS gave the team a repeatable regression check. The honest caveat: it's an LLM-as-judge metric, so it's only as trustworthy as its calibration against real human judgment — something the team only partially validated, on a small sample, not the full question set.

---

## 6. Limitations, Gaps, and "What Would You Change" (say these unprompted — it reads as maturity, not weakness)

- **No reranking stage.** Retrieval was dense+sparse+RRF, but nothing re-scored the fused top-k candidates with a cross-encoder before generation. If I rebuilt this, that's the first addition — it's a well-understood way to improve precision on the already-narrowed set without touching the rest of the pipeline.
- **BM25 wasn't a real persisted index.** It was rebuilt in memory on process start, which is fine at the corpus size we were testing against but wouldn't hold up as the document set grew — a production version needs a real persisted sparse index.
- **Metadata filters were caller-supplied, not identity-derived.** Retrieval could be filtered by team/doc-type, but the filter value was whatever the caller passed — not derived server-side from the authenticated user's actual permissions. That's fine for an internal pilot with a small, trusted user group, but it's a real access-control gap that would need closing before a wider rollout.
- **Query expansion was discussed but not built.** We talked about generating multiple reworded versions of a vague query and retrieving for all of them, but judged it unnecessary at our corpus size and query patterns — deferred, not implemented.
- **No dedicated observability for checkpoint-vs-persistence divergence.** The checkpoint's internal state and the Postgres-side summary/memory state could in principle disagree, and we didn't build a monitored check for that — only ad hoc debug endpoints we used manually during development. In a real production rollout, that comparison should be an automated, monitored invariant, not something a developer checks by hand.
- **Not validated at scale.** This ran as an internal pilot with a limited group of users, not a company-wide rollout — so questions about latency or index behavior at 50–100x the document count are honestly "we'd need to test that," not something I can claim we already proved.

**"What would you change if you built it again?"** — Add the reranker first (cheapest, highest-leverage gap), then move metadata filtering to be identity-derived rather than caller-supplied before any wider rollout, since that's a real security gap masquerading as a minor detail.

---

## 7. Quick-Reference Answer Bank for the Six Question Types You Flagged

**"Why didn't you use approach X instead?"** — Pick the specific X from the relevant section above (reranker, native hybrid search, bigger chunks, manual review instead of RAGAS) and lead with the *reason*, not a defense — every "why not X" answer above states the actual constraint (schema migration cost, validated-first-cheaply, dilution effect, scalability of manual review) rather than "we didn't think of it."

**"What were the limitations of your approach?"** — Section 6, verbatim if needed. Lead with the reranker gap and the caller-supplied filter gap — those are the two most technically substantive ones.

**"What would you change if you built it again?"** — End of Section 6: reranker first, then identity-derived filtering.

**"Why did you choose this architecture/technology?"** — RRF over native hybrid (schema/migration cost), parent-child over bigger chunks (dilution), RAGAS over manual review (repeatability) — each has a one-sentence reason in Section 5, not just "it's standard practice."

**"What exactly was your contribution?"** — Section 2, said plainly: retrieval pipeline, evaluation harness, and the API integration layer, owned end-to-end; long-term memory classification and checkpoint debugging, contributed to inside a teammate's architecture; overall agent/checkpoint design and vector infra, explicitly not yours.

**"What problems did you actually face?"** — Section 4's three problems, each with a real root cause and a real fix, not a generic "we had some retrieval issues."
