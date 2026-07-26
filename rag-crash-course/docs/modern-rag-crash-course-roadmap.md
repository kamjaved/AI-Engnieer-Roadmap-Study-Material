# Modern RAG — Lean Crash Course

> Same lineage as `langgraph-memory-crash-course-roadmap.md`, same format, different system. This is a standalone learning document — every lesson carries enough context to be pasted, on its own, into ChatGPT, Gemini, or Claude and produce correct, scoped code.

---

## 0. Summary & Objective — Read This First (Including If You're an AI Tool)

**What this is.** A ~2.5–3 hour, hands-on crash course that teaches the complete mechanics behind a production-grade Retrieval-Augmented Generation pipeline — documents → chunks → embeddings → vector index → retrieval → metadata filtering → prompt augmentation → generation → evaluation → optimization — using a small internal "DevPortal" knowledge base as the vehicle. It is deliberately small so the RAG concepts stay visible and uncluttered by domain complexity, auth, UI polish, or infra you don't need to learn RAG.

**What you'll be able to do afterward.** Explain, from first principles and with working code you wrote yourself, why each stage of a RAG pipeline exists, what specifically breaks when you skip it, and what the beginner/production/enterprise version of that stage looks like — then defend those choices in a design review or interview.

**Domain used.** Six short markdown docs (`deploy.md`, `auth.md`, `rate_limits.md`, `on_call.md`, `migrations.md`, `incident_response.md`) simulating an internal developer-platform knowledge base, each with lightweight metadata (`team`, `doc_type`). That's the entire corpus — deliberately thin, because the learning goal is RAG mechanics, not document management.

**Explicitly out of scope for this crash course:** authentication, a database for app state, Alembic-style migrations, a frontend, CI/CD, Kubernetes, multi-tenant infra, and agentic query routing. Every lesson flags exactly what it's skipping and why, and the recap (Lesson 11) tells you what to build next once this is done.

**How to use this document.** Work top to bottom. Each lesson is self-contained: objective, why it matters, what to build, a short illustrative code pattern (for your own mental model), and a ready-to-paste "AI Build Prompt" you can hand to a coding assistant to generate the actual implementation. Do the "Done When" check before moving on — RAG bugs are almost always silent (a wrong answer that *sounds* confident), and they compound if you don't verify each stage independently.

**Total time:** ~2 hours 55 minutes. Natural split point: Lessons 1–5 (~1h20, gets you to a populated, queryable vector index) and Lessons 6–11 (~1h35, retrieval, generation, the full app, evaluation, and production hardening).

**Assumed prerequisites (per your setup):** you already have an `OPENAI_API_KEY` and a `PINECONE_API_KEY`, Python 3.13+ and `uv` installed. This course does not walk you through obtaining either key or installing base tooling.

---

## 0.5 Verification Notes (checked July 2026)

Before starting, here's what was fact-checked against current PyPI releases and official LangChain/Pinecone/OpenAI docs, so the code below isn't teaching you deprecated syntax.

- **Pinecone's Python SDK is `pinecone` on PyPI, not `pinecone-client`.** The latter is deprecated — installing it alongside `pinecone` causes import collisions. The SDK is currently on a v9 rewrite (single install covers REST, gRPC, and asyncio transports; requires Python 3.10+), and `langchain-pinecone` (currently ~0.2.11) targets it. If you find older tutorials using `pinecone.init(...)`, that's v2 syntax and no longer works — this course uses the current `Pinecone(api_key=...)` client-object pattern throughout.
- **`langchain-pinecone`'s `PineconeVectorStore` and `langchain-openai`'s `OpenAIEmbeddings`/`ChatOpenAI` are current and stable** — no breaking changes pending. Versions verified: `langchain` ~1.3.14, `langchain-openai` ~1.4.1, `langchain-text-splitters` ~1.1.2, `langchain-pinecone` ~0.2.11.
- **OpenAI's `text-embedding-3-small` and `text-embedding-3-large` are both still current and non-deprecated** as of mid-2026 (only `text-embedding-ada-002` is legacy). This course defaults to `-small` (1536 dimensions, the cost-effective default most teams start with) and Lesson 10 shows the one-line swap to `-large` as an optimization lever.
- **Pinecone ships a hosted reranker** (`pc.inference.rerank`, model `bge-reranker-v2-m3`) reachable with the same Pinecone API key you already have — no third-party reranking key needed. Lesson 10 uses this instead of pulling in a separate reranking provider, to keep the dependency surface to exactly what you told me you have credentials for.
- **On chat model naming:** OpenAI's flagship chat model name changes faster than this document can stay accurate (multiple GPT-5.x releases shipped between March and July 2026 alone). Code below uses `gpt-4.1` as a concrete, currently-valid, long-context API model so every snippet actually runs — but the generation model is the least RAG-specific part of this stack. Swap `CHAT_MODEL` in your `.env` for whatever current flagship your account has access to; nothing else in the pipeline changes.

None of this affects sequencing — proceed lesson by lesson exactly as written.

---

## 1. Lesson 1 — Prerequisites & Lean Project Setup

### 🎯 Objective
Stand up the minimum project skeleton this course needs. No FastAPI yet, no database, no auth.

### 🧠 Why This Matters
RAG's actual mechanism — turning documents into a searchable, groundable knowledge source — has nothing to do with FastAPI or a request/response cycle. Wrapping the pipeline in a web server before it works standalone is a common beginner mistake: you end up debugging HTTP and retrieval quality at the same time. This course builds and validates each pipeline stage as a plain, directly-runnable Python module first (`uv run python -m rag.stage_name`), and only wraps the whole thing behind an API in Lesson 8 — services are the last mile, not the starting point.

### 📥 Dependencies
```bash
uv init rag-crash-course --python 3.13
cd rag-crash-course
uv add langchain langchain-openai langchain-pinecone langchain-text-splitters pinecone pydantic-settings python-dotenv
uv add --dev ruff
```

| Package | Why |
|---|---|
| `langchain` | core primitives: prompt templates, LCEL runnables, document schema |
| `langchain-openai` | `OpenAIEmbeddings` and `ChatOpenAI` — thin wrappers over the `openai` SDK |
| `langchain-pinecone` | `PineconeVectorStore` — the LangChain-native interface to your index |
| `langchain-text-splitters` | `RecursiveCharacterTextSplitter` and friends (Lesson 3) |
| `pinecone` | the actual Pinecone SDK — index creation, upsert, query, rerank (Lessons 5, 6, 10) |
| `pydantic-settings` | typed `.env` loading |
| `ruff` | dev-only linting |

Notice what's **not** here yet: `fastapi` (Lesson 8), `ragas` (Lesson 9). Installing them now would work fine, but pulling dependencies in at the lesson that actually needs them keeps you from debugging an import you haven't used yet.

### 🛠️ What To Build
```text
rag-crash-course/
  .env
  pyproject.toml
  data/
    docs/
      deploy.md
      auth.md
      rate_limits.md
      on_call.md
      migrations.md
      incident_response.md
  src/
    rag/
      __init__.py
      config.py              # pydantic-settings
      ingestion/
        __init__.py
        loader.py             # Lesson 3
        chunker.py            # Lesson 3
      indexing/
        __init__.py
        embed_and_index.py    # Lesson 5
      retrieval/
        __init__.py
        retriever.py          # Lesson 6
        reranker.py           # Lesson 10
      generation/
        __init__.py
        prompt.py             # Lesson 7
        chain.py              # Lesson 7
      evaluation/
        __init__.py
        eval_dataset.py       # Lesson 9
        run_eval.py           # Lesson 9
```

`.env`:
```text
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk-...
PINECONE_INDEX_NAME=devportal-kb
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4.1
```

The six seed docs — short, deliberately thin, ~150–250 words each, one topic per file: a deployment runbook, an auth/token policy doc, a rate-limits reference, an on-call rotation guide, a database-migration checklist, and an incident-response playbook. Each doc gets `team` (`platform` | `security` | `data`) and `doc_type` (`runbook` | `policy` | `guide`) metadata — you'll use exactly these two fields for metadata filtering in Lesson 6.

### 🤖 AI Build Prompt
```text
Generate:
1. src/rag/config.py — a pydantic-settings BaseSettings class loading
   OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME,
   EMBEDDING_MODEL (default "text-embedding-3-small"), and CHAT_MODEL
   (default "gpt-4.1") from .env. Export a module-level `settings`
   instance.
2. Six short markdown files under data/docs/ for a fictional internal
   developer platform: deploy.md (deployment runbook), auth.md
   (token/auth policy), rate_limits.md (API rate-limit reference),
   on_call.md (on-call rotation guide), migrations.md (DB migration
   checklist), incident_response.md (incident playbook). Each 150-250
   words, plain prose, no frontmatter.
3. A Python dict DOC_METADATA in src/rag/ingestion/loader.py (stub for
   now) mapping each filename to {"team": ..., "doc_type": ...} using:
   deploy.md/platform/runbook, auth.md/security/policy,
   rate_limits.md/platform/policy, on_call.md/platform/runbook,
   migrations.md/data/runbook, incident_response.md/security/runbook.

Do not add FastAPI, a database, or the ragas dependency yet — those
are separate lessons.
```

### ✅ Done When
`uv run python -c "from rag.config import settings; print(settings.PINECONE_INDEX_NAME)"` prints your index name with no import errors, and all six markdown files exist under `data/docs/`.

### ⏱️ ~10 minutes

---

## 2. Lesson 2 — The RAG Mental Model

### 🎯 Objective
Before writing a line of pipeline code, fix the core idea precisely enough that every later lesson is just "implementing one box in this diagram" rather than a new concept.

### 🧠 Why This Matters
"RAG" gets used loosely to mean anything that combines an LLM with "your data." That looseness is where production bugs hide — a bad answer is almost never a single bug, it's a *stage* bug (bad chunk, bad retrieval, bad prompt, or a model that ignores good context), and you can't debug what you can't name.

```text
Why RAG exists at all
  An LLM's knowledge is frozen at training time and bounded by its
  context window. Two ways to make it answer from YOUR current data:
  fine-tuning (bakes facts into weights — slow, expensive, still not
  great at precise recall) or RAG (fetch the relevant facts at query
  time and hand them to the model as context — cheap, instantly
  updatable, and the model's reasoning ability still does the work).
  RAG doesn't make the model smarter; it makes the model's existing
  reasoning ability operate on the right facts.

Document
  Your raw source of truth (a markdown file, a PDF, a wiki page).
  Too large to embed as one meaningful unit — a whole doc's vector
  represents an average of everything in it, which matches nothing
  precisely.

Chunk
  A document split into retrievable units. The thing you actually
  embed and index. Chunk boundaries ARE a design decision, not an
  implementation detail (Lesson 3).

Embedding
  A chunk's meaning, represented as a fixed-length vector. "Similar
  meaning" becomes "nearby vectors" — this is what makes semantic
  search possible instead of exact keyword match (Lesson 4).

Vector index
  Where embeddings live so "find the k chunks nearest to this query"
  is fast at scale — approximate nearest-neighbor search, not a
  linear scan (Lesson 5).

Retrieval
  Turning a user's question into a query embedding, searching the
  index, optionally filtering by metadata, and getting back the
  chunks most likely to contain the answer (Lesson 6).

Augmentation
  Stuffing those retrieved chunks into the prompt alongside the
  question, with instructions that ground the model's answer in
  them. This is the step that actually makes it "Retrieval-AUGMENTED
  Generation" rather than just search (Lesson 7).

Generation
  The LLM call itself, producing an answer conditioned on the
  augmented prompt (also Lesson 7).
```

The core relationship to hold in your head for the rest of this course: **retrieval quality caps generation quality — a perfect prompt cannot rescue chunks that don't contain the answer, and a sloppy prompt can waste chunks that do.** You will build and evaluate these as separable stages on purpose, because in production you diagnose and fix them separately.

### 🤖 AI Build Prompt
None — this lesson is conceptual. To sanity-check your own understanding, ask an AI tool: *"If a RAG app confidently answers a question wrong, list the distinct pipeline stages that could be the root cause, and for each, what a symptom that isolates it would look like."* The answer should distinguish at minimum: bad chunking (answer exists in the doc but got split across a boundary), bad embedding/retrieval (right chunk exists in the index but wasn't retrieved), bad augmentation (right chunk was retrieved but the prompt buried or mishandled it), and bad generation (model ignored good context and used its own prior knowledge instead).

### ⏱️ ~15 minutes

---

## 3. Lesson 3 — Documents → Chunks

### 🎯 Objective
Load the seed docs and split them into retrievable chunks, carrying doc-level metadata onto every chunk.

### 🧠 Why This Matters
This is the stage most tutorials treat as boilerplate and most production incidents trace back to. A chunk is the *unit of retrievable meaning* — get the boundary wrong and you can have the answer sitting in your corpus, correctly embedded, correctly indexed, and still never surface it, because the sentence that answers the question got split from the sentence that gives it context.

**Beginner approach — fixed-size character chunking.** Split every N characters, ignoring structure. Fast to implement, frequently cuts mid-sentence or mid-code-block. Fine for a demo, wrong for anything you'll evaluate.

**Production approach — recursive, structure-aware chunking.** `RecursiveCharacterTextSplitter` tries a list of separators in priority order (`"\n\n"`, `"\n"`, `" "`, `""`) and only falls back to a harder split when a chunk still exceeds `chunk_size`. In practice this means it splits on paragraph boundaries first, and only cuts mid-sentence as a last resort. This is the default a production team should reach for unless they've measured a reason not to.

**Enterprise approach — semantic / layout-aware chunking.** For heterogeneous corpora (PDFs with tables, HTML with nested sections, code with function boundaries), you chunk on document *structure* (markdown headers, HTML sections, AST nodes for code) or on *semantic similarity* (embed sentences, cut where consecutive-sentence similarity drops — "semantic chunking"). More expensive to build and run, but it's what closes the gap when recursive character chunking still produces chunks that mix unrelated topics.

**Chunk size and overlap — the actual tradeoff, not a magic number:**
- **Too small** (e.g. 100 tokens): each chunk is precise but loses surrounding context — you retrieve a sentence fragment that answers "what" but not "why" or "when," and the LLM has nothing to reason with.
- **Too large** (e.g. 2000+ tokens): retrieval gets *less* precise, because a chunk mixing three topics has a diluted embedding that matches all three queries weakly instead of one query strongly — and you burn prompt tokens on irrelevant text.
- **Overlap** (commonly 10–20% of chunk size) prevents losing a sentence that straddles a boundary, at the cost of duplicate content inflating your index size and, at query time, sometimes retrieving near-duplicate chunks that don't add information.
- Common mistake: picking chunk size once, never revisiting it. Chunk size is a hyperparameter you tune against Lesson 9's evaluation numbers, not a constant you set on day one and forget.

### 🛠️ What To Build
- `ingestion/loader.py` — reads every `.md` under `data/docs/`, attaches `team`/`doc_type` metadata per file, returns a list of LangChain `Document` objects (`page_content` + `metadata`).
- `ingestion/chunker.py` — `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=75)`, splits each `Document`, and propagates the parent doc's metadata onto every chunk plus a `source` field (the filename) and a stable `chunk_id`.

### 💡 Core Pattern
```python
# The point of this snippet: metadata must be attached to the PARENT
# document before splitting, so every chunk inherits it. Attach
# metadata after splitting and you have to re-derive which chunk
# came from which source — error-prone and easy to get wrong silently.
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=75,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)  # metadata carries over automatically
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{chunk.metadata['source']}::{i}"
    return chunks
```

### 🤖 AI Build Prompt
```text
Using langchain-core and langchain-text-splitters, generate:
1. src/rag/ingestion/loader.py — load_documents() that reads every
   .md file from data/docs/, wraps each as a langchain_core.documents
   .Document, and attaches metadata {"source": filename, "team":...,
   "doc_type": ...} using the DOC_METADATA mapping from Lesson 1.
2. src/rag/ingestion/chunker.py — chunk_documents(docs) using
   RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=75),
   propagating parent metadata onto every chunk and adding a
   deterministic "chunk_id" field (f"{source}::{index}").
3. A __main__ block (or src/rag/ingestion/run_ingest_preview.py) that
   loads, chunks, and prints: total chunk count, and for the longest
   document, how many chunks it produced and their character lengths.
Do not call any embedding or Pinecone API yet — this lesson stops at
plain-text chunks.
```

### ✅ Done When
Running the preview script shows a reasonable chunk count (roughly 2–4 chunks per seed doc at this size) and every printed chunk's metadata includes `source`, `team`, `doc_type`, and `chunk_id` — confirm by eye that no chunk's `page_content` cuts off mid-sentence in a way that would lose meaning.

### 🔑 Concepts You Must Be Able to Explain
Why chunk size is a tradeoff and not a constant. Why metadata has to be attached before splitting, not after. What "recursive" means in `RecursiveCharacterTextSplitter` — it's not recursion over documents, it's a priority-ordered fallback through separators.

### ⏭️ Deferred (Production Extension)
Semantic/embedding-based chunk-boundary detection, layout-aware chunking for PDFs/HTML with tables, and chunk-size auto-tuning against eval metrics (Lesson 9 gives you the harness; wiring an automated sweep is a natural next step once this course ends).

### ⏱️ ~20 minutes

---

## 4. Lesson 4 — Embeddings: The Vector Space Mental Model

### 🎯 Objective
Understand what an embedding actually *is* before treating `OpenAIEmbeddings()` as a black box, and generate embeddings for your chunks.

### 🧠 Why This Matters
Every retrieval bug that isn't a chunking bug is usually an embedding-model mismatch bug. If you don't have the mental model, "why did retrieval get worse after I changed one line" turns into hours of confused debugging instead of a five-second diagnosis.

```text
What an embedding is
  A fixed-length list of floats (1536 numbers for text-embedding-3-
  small) positioning a piece of text in a high-dimensional space,
  such that texts with similar MEANING end up at similar POSITIONS —
  not similar spelling. "How do I reset my password" and "steps to
  recover account access" land near each other despite sharing almost
  no words. This is the entire reason semantic search beats keyword
  search for natural-language questions.

Why cosine similarity
  Two vectors' cosine similarity measures the ANGLE between them, not
  their length — so a short chunk and a long chunk discussing the
  same thing can still score as similar. Cosine is the default sane
  metric for text embeddings; dot product is equivalent when vectors
  are normalized (OpenAI's embeddings are), and Euclidean distance
  behaves worse in high dimensions ("curse of dimensionality" —
  distances compress and become less discriminating).

The constraint that causes the most production incidents
  Your query embedding and your indexed embeddings MUST come from the
  SAME model. Different embedding models produce vector spaces that
  are not just differently-scaled — they're not comparable AT ALL. If
  you re-index half your corpus with text-embedding-3-large and query
  against vectors still indexed with -small, you won't get an error —
  you'll get silently garbage results, because Pinecone will happily
  compute a cosine similarity between incompatible vectors and return
  a confident-looking but meaningless ranking.
```

**Beginner approach:** embed everything with one model, one dimension, never think about it again. Fine until you need multilingual support or hit a cost wall.

**Production approach:** pick `text-embedding-3-small` (1536-dim) as the default — cheap, fast, strong general-purpose retrieval — and treat the model choice as a config value (`EMBEDDING_MODEL` in your `.env`), not a hardcoded string, so swapping it is a deliberate, tracked decision.

**Enterprise approach:** support multiple embedding models behind a versioned index naming scheme (e.g. `devportal-kb-v2-3large`), so you can run an A/B comparison or migrate without downtime — Lesson 10 touches on why re-embedding the whole corpus on every doc change doesn't scale and what incremental indexing looks like instead.

### 🛠️ What To Build
Nothing persisted yet — this lesson is a standalone script proving you understand what you're about to index: embed two semantically-similar sentences and two unrelated ones, print their pairwise cosine similarities, and confirm similar sentences score higher.

### 💡 Core Pattern
```python
# The point of this snippet: SEE the vector space work before trusting
# Pinecone to do similarity search for you. This is a five-line sanity
# check that will save you an hour the first time retrieval looks wrong.
import numpy as np
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

texts = [
    "How do I roll back a failed deployment?",
    "What's the process for reverting a broken release?",
    "What's the on-call rotation schedule?",
]
vectors = embeddings.embed_documents(texts)

def cosine_sim(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

print("similar meaning:", cosine_sim(vectors[0], vectors[1]))    # high
print("unrelated:      ", cosine_sim(vectors[0], vectors[2]))    # lower
```

### 🤖 AI Build Prompt
```text
Using langchain-openai, generate a standalone script
src/rag/ingestion/embedding_sanity_check.py that:
1. Instantiates OpenAIEmbeddings using settings.EMBEDDING_MODEL from
   config.py.
2. Embeds three sentences: two semantically similar (paraphrases of
   each other) and one unrelated, all about the DevPortal domain
   (deployments, on-call, auth — pick your own wording).
3. Computes pairwise cosine similarity using numpy (no external
   similarity library) and prints all three pairwise scores with
   labels.
4. Asserts (with a plain assert + printed message, not a test
   framework) that the two similar sentences score higher against
   each other than either scores against the unrelated one.
```

### ✅ Done When
The script runs, prints three similarity scores, and the assertion passes — the two paraphrased sentences score meaningfully higher than either does against the unrelated sentence.

### 🔑 Concepts You Must Be Able to Explain
Why embedding model consistency between index-time and query-time is non-negotiable, and why that failure mode is silent rather than an error. Why cosine similarity, specifically, is the right default for text embeddings.

### ⏱️ ~15 minutes

---

## 5. Lesson 5 — Vector Store & Indexing (the write path)

### 🎯 Objective
Create a Pinecone serverless index and upsert your embedded chunks into it — the pipeline's write path, run once (or on every doc update), separate from the read path you'll build in Lesson 6.

### 🧠 Why This Matters
A vector index isn't "a database that happens to store vectors" — it's built around approximate nearest-neighbor (ANN) search, because at real scale (millions of vectors) an exact brute-force comparison against every stored vector is too slow. Pinecone (like most production vector DBs) uses graph-based ANN indexing under the hood, trading a small amount of recall accuracy for massive speed. You don't implement the ANN algorithm yourself — but you do need to understand the two decisions that shape it: **index dimension** (must exactly match your embedding model's output — 1536 for `-small`) and **distance metric** (cosine, for the reasons in Lesson 4).

**Beginner approach:** one index, no namespaces, no metadata, `metric="cosine"`, done. This is what you're building today, and it's a legitimate production pattern for a single-tenant, single-corpus app.

**Production approach:** attach metadata at upsert time (you're already doing this, since Lesson 3 propagated it onto every chunk) so retrieval can filter, not just rank — Lesson 6 depends on this. Also: batch your upserts (Pinecone recommends batches, not one vector per call) and make ingestion idempotent by using a deterministic `chunk_id` as the vector ID, so re-running ingestion after a doc edit *overwrites* the old chunk instead of duplicating it.

**Enterprise approach:** **namespaces** for hard tenant/environment isolation (e.g. one namespace per customer, or `staging` vs `prod`) — namespaces are a physical partition within the index, faster and more isolated than a metadata filter for that use case. Multiple indexes (or a `doc_version` metadata field plus filtering) when you need to run two embedding-model generations side by side during a migration.

### 📥 Assumed State
Lessons 3–4's chunking and embedding both work in isolation.

### 🛠️ What To Build
`indexing/embed_and_index.py` — create the index if it doesn't exist (dimension from the embedding model, `metric="cosine"`, `ServerlessSpec`), then use `PineconeVectorStore.from_documents(chunks, embeddings, index_name=...)` to embed and upsert every chunk in one call — LangChain handles the batching for you.

### 💡 Core Pattern
```python
# The point of this snippet: index creation is idempotent (check
# has_index first) and dimension is derived from the embedding model,
# never hardcoded — hardcode it once and the day you swap embedding
# models, index creation silently succeeds with the WRONG dimension
# and every subsequent upsert throws a cryptic mismatch error.
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from rag.config import settings

EMBEDDING_DIMENSIONS = {"text-embedding-3-small": 1536, "text-embedding-3-large": 3072}

def get_or_create_index(pc: Pinecone) -> None:
    if not pc.has_index(settings.PINECONE_INDEX_NAME):
        pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSIONS[settings.EMBEDDING_MODEL],
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

def index_chunks(chunks: list) -> PineconeVectorStore:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    get_or_create_index(pc)
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
    return PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=settings.PINECONE_INDEX_NAME,
        ids=[c.metadata["chunk_id"] for c in chunks],  # idempotent re-ingestion
    )
```

### 🤖 AI Build Prompt
```text
Using pinecone and langchain-pinecone, generate
src/rag/indexing/embed_and_index.py:
1. get_or_create_index(pc: Pinecone) -> None — checks pc.has_index(),
   creates a serverless index (cloud="aws", region="us-east-1",
   metric="cosine") with dimension looked up from an
   EMBEDDING_DIMENSIONS dict keyed by settings.EMBEDDING_MODEL
   (text-embedding-3-small: 1536, text-embedding-3-large: 3072) if it
   doesn't already exist.
2. index_chunks(chunks: list[Document]) -> PineconeVectorStore — builds
   OpenAIEmbeddings(model=settings.EMBEDDING_MODEL), calls
   PineconeVectorStore.from_documents with explicit ids= set to each
   chunk's chunk_id metadata field (so re-running ingestion overwrites
   rather than duplicates).
3. A __main__ entrypoint (src/rag/run_ingest.py) that chains
   load_documents() -> chunk_documents() -> index_chunks() and prints
   the resulting vector count via pc.Index(name).describe_index_stats().
```

### ✅ Done When
`uv run python -m rag.run_ingest` completes without error, and `describe_index_stats()` reports a vector count matching your chunk count from Lesson 3. Run it a second time immediately after — the count should stay the same, not double (proves the `ids=` idempotency).

### 🔑 Concepts You Must Be Able to Explain
Why index dimension must match the embedding model, and what happens (concretely, not vaguely) if it doesn't. Why using a deterministic ID instead of an auto-generated one is a production requirement, not a nicety. What a namespace is and when you'd reach for one instead of a metadata filter.

### ⏭️ Deferred (Production Extension)
Incremental/content-hash-based indexing so unchanged chunks aren't re-embedded on every ingestion run (Lesson 10 explains why this matters at scale); multi-namespace tenant isolation; a background job/webhook that re-runs ingestion automatically when source docs change.

### ⏱️ ~20 minutes

---

## 6. Lesson 6 — Retrieval & Metadata Filtering (the read path)

### 🎯 Objective
Turn a natural-language question into the k most relevant chunks — with and without metadata filters — completing the "R" in RAG.

### 🧠 Why This Matters
Retrieval is where most of your actual product quality lives, and it's the stage people under-invest in because "it's just `similarity_search`, right?" Two decisions dominate retrieval quality: **how many chunks you pull (`k`)** and **whether you narrow the search space before or alongside the vector search (metadata filtering)**.

**The `k` tradeoff:**
- Too small (`k=1–2`): you miss relevant context that happened to score slightly lower than the top hit — very common when the answer spans two chunks.
- Too large (`k=20+`) fed directly to generation: you dilute the prompt with noise, pay for tokens you didn't need, and risk the "lost in the middle" problem (Lesson 10) where the LLM under-attends to context buried in a long prompt.
- **Production default:** retrieve a wider candidate set (`k=15–25`) and either filter it down with metadata, or rerank it down to `k=3–5` before generation (Lesson 10) — separating "cast a wide net" from "pick the best few" is a two-stage pattern, not a single `top_k` knob.

**Metadata filtering — a retrieval lever, not an afterthought:**
Pinecone lets you pass a `filter` dict alongside the vector query, evaluated *before or alongside* the ANN search rather than as a post-hoc Python filter on the results. This matters for three separate reasons: (1) **relevance** — a query about "on-call" shouldn't surface a `data` team migration doc even if it scores decently on pure semantic similarity; (2) **correctness at scale** — pre-filtering a large index by tenant/team is dramatically cheaper than retrieving 1000 candidates and filtering in application code; (3) **access control** — if a user should only see `platform`-team docs, filtering at the vector-search layer is the enforcement point, not a check you bolt on after the fact (and forget on one code path).

**Beginner approach:** unfiltered `similarity_search(query, k=4)`. Fine for a single-corpus demo.

**Production approach:** always pass an explicit filter (even an empty `{}`) so filtering is a conscious parameter of every query, not something added later under time pressure; expose `team`/`doc_type` filters as parameters your retrieval function accepts.

**Enterprise approach:** filter-driven access control enforced server-side per authenticated user/tenant (never trust a client-supplied filter for security — derive it from the authenticated session), plus hybrid dense+sparse search (Lesson 10) for queries containing exact identifiers (error codes, endpoint names) that pure semantic search under-weights.

### 🛠️ What To Build
`retrieval/retriever.py` — a function that takes a query string, an optional metadata filter dict, and `k`, and returns scored chunks.

### 💡 Core Pattern
```python
# The point of this snippet: filter is a first-class parameter, not an
# afterthought — and note similarity_search_with_score, not
# similarity_search, because a raw cosine score is diagnostic
# information you want (Lesson 9 needs it), even though it is NOT a
# calibrated confidence — don't present it to end users as "% match."
from langchain_pinecone import PineconeVectorStore

def retrieve(
    vector_store: PineconeVectorStore,
    query: str,
    k: int = 5,
    team: str | None = None,
    doc_type: str | None = None,
) -> list[tuple]:
    filter_dict: dict = {}
    if team:
        filter_dict["team"] = {"$eq": team}
    if doc_type:
        filter_dict["doc_type"] = {"$eq": doc_type}

    return vector_store.similarity_search_with_score(
        query, k=k, filter=filter_dict or None,
    )
```

### 🤖 AI Build Prompt
```text
Using langchain-pinecone, generate src/rag/retrieval/retriever.py:
1. get_vector_store() -> PineconeVectorStore — reconnects to the
   existing index (does NOT re-create or re-upsert) using
   OpenAIEmbeddings(model=settings.EMBEDDING_MODEL) and
   settings.PINECONE_INDEX_NAME.
2. retrieve(vector_store, query: str, k: int = 5, team: str | None =
   None, doc_type: str | None = None) -> list[tuple[Document, float]]
   — builds a Pinecone filter dict from team/doc_type using $eq when
   provided, calls similarity_search_with_score, returns results.
3. A __main__ demo (src/rag/run_retrieval_demo.py) that runs the same
   query ("how do I roll back a deployment?") three times: no filter,
   filter team="platform", filter team="security" — and prints each
   result set's chunk sources and scores side by side so the filtering
   effect is visible.
```

### ✅ Done When
The demo script shows the unfiltered query returning the deploy-runbook chunk as the top hit, and the `team="security"` filtered query either returns zero platform-team results or none at all — proving the filter is actually constraining the search, not just re-ranking within the same result set.

### 🔑 Concepts You Must Be Able to Explain
Why metadata filtering happens at the vector-search layer instead of as a post-hoc Python `if` on results. Why a raw cosine similarity score is not a calibrated confidence value. The two-stage "wide retrieval, then narrow" pattern and why it's different from just picking a smaller `k`.

### ⏭️ Deferred (Production Extension)
Server-side, session-derived filters for access control (this lesson's filters are caller-supplied, which is fine for a single-user demo and unsafe for a multi-tenant app); hybrid dense+sparse retrieval; query rewriting before embedding (both in Lesson 10).

### ⏱️ ~15 minutes

---

## 7. Lesson 7 — Prompt Augmentation & Generation

### 🎯 Objective
Turn retrieved chunks into a grounded answer: build the augmented prompt and wire it to the LLM as an LCEL chain.

### 🧠 Why This Matters
"Augmentation" sounds like it should be complicated. Mechanically, it's string concatenation: system instructions + formatted retrieved chunks + the user's question. What separates a naive concatenation from a production-grade one is four specific decisions, each with a real failure mode if you skip it:

1. **Grounding instructions.** Explicitly tell the model to answer *only* from the provided context and to say so if the context doesn't contain the answer. Skip this and the model will silently blend retrieved context with its own parametric knowledge — which is exactly the hallucination-under-a-confident-tone failure mode that makes RAG bugs hard to catch by eye.
2. **Source attribution scaffolding.** Number or label each retrieved chunk (`[Source 1: deploy.md]`) so the model can cite which source backs which claim, and so you can show citations to the user — turning "trust the answer" into "verify the answer" is a real production requirement, not a nice-to-have.
3. **Context ordering.** Put the most relevant chunk closest to the question, not first in an arbitrary list — long-context models measurably under-attend to information buried in the middle of a long prompt (the "lost in the middle" effect, covered fully in Lesson 10). For a handful of short chunks this barely matters; it matters a lot once you're stuffing 15+ chunks in.
4. **Token budget.** Retrieved context + system prompt + question must fit inside the model's context window with room left for the answer. At small `k` this is rarely the constraint — it becomes one the moment you widen retrieval (Lesson 6's "wide net" pattern) without a reranking step to narrow back down before generation.

**Beginner approach:** f-string concatenation, no grounding instruction, no citations. Works for a demo, fails an evaluation the moment you check faithfulness (Lesson 9).

**Production approach:** a structured prompt template (`ChatPromptTemplate`) with an explicit grounding instruction and numbered sources, composed as an LCEL chain (`retriever | format | prompt | llm | parser`) so each stage is independently swappable and testable.

**Enterprise approach:** dynamic prompt selection based on query type (a "what's the policy on X" question needs different framing than "walk me through how to do X"), streaming generation with incremental citation resolution, and a guardrail pass that checks the generated answer's claims against the retrieved context before returning it to the user (a second, cheaper LLM call or a rules-based check — effectively a lightweight, real-time version of Lesson 9's faithfulness metric).

### 🛠️ What To Build
- `generation/prompt.py` — a `ChatPromptTemplate` with a grounding-instruction system message and a human message template that takes formatted, numbered context plus the question.
- `generation/chain.py` — the LCEL chain wiring retrieval → formatting → prompt → `ChatOpenAI` → string output.

### 💡 Core Pattern
```python
# The point of this snippet: the grounding instruction is not
# decorative — it is the single highest-leverage sentence in this
# entire course for reducing hallucination. Cut it and faithfulness
# scores in Lesson 9 drop noticeably on ambiguous questions.
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """You are an internal developer-platform assistant.
Answer ONLY using the numbered sources below. If the sources don't
contain the answer, say "I don't have that in the knowledge base"
instead of guessing. Cite sources inline like [1], [2]."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Sources:\n{context}\n\nQuestion: {question}"),
])

def format_docs(scored_docs: list[tuple]) -> str:
    return "\n\n".join(
        f"[{i+1}] (source: {doc.metadata['source']})\n{doc.page_content}"
        for i, (doc, _score) in enumerate(scored_docs)
    )

llm = ChatOpenAI(model="gpt-4.1", temperature=0)
generation_chain = prompt | llm | StrOutputParser()
```

### 🤖 AI Build Prompt
```text
Using langchain-core and langchain-openai, generate:
1. src/rag/generation/prompt.py — SYSTEM_PROMPT (grounding instruction
   as shown above, adapted for a DevPortal assistant persona) and a
   ChatPromptTemplate with a "context" and "question" input variable.
2. src/rag/generation/chain.py:
   - format_docs(scored_docs: list[tuple[Document, float]]) -> str,
     numbering each source and labeling it with its metadata "source"
     field.
   - answer_question(vector_store, question: str, k: int = 5,
     team: str | None = None, doc_type: str | None = None) -> dict —
     calls retrieve() from Lesson 6, formats the docs, invokes the
     prompt | ChatOpenAI(model=settings.CHAT_MODEL, temperature=0) |
     StrOutputParser() chain, and returns
     {"answer": str, "sources": [source filenames used],
      "raw_chunks": scored_docs} so the caller can inspect what was
     retrieved, not just the final text.
3. A __main__ demo asking three questions: one clearly answerable from
   the docs, one clearly NOT in the docs (to verify the model refuses
   instead of guessing), and one that spans two source documents.
```

### ✅ Done When
All three demo questions produce sensible output: the answerable one cites the right source, the unanswerable one triggers the "I don't have that" refusal rather than a fabricated answer, and the cross-document one cites more than one source.

### 🔑 Concepts You Must Be Able to Explain
Why the grounding instruction is the highest-leverage sentence in the prompt. What "lost in the middle" means and why it's a context-ordering problem, not a model-capability problem. Why returning `raw_chunks` alongside the answer (not just the final string) is a production requirement — you cannot debug or evaluate a RAG answer without knowing what it was grounded in.

### ⏭️ Deferred (Production Extension)
Streaming responses with incremental citations; a real-time faithfulness guardrail pass; dynamic prompt selection by query type; multi-turn conversational RAG (this lesson answers one question at a time, stateless — combining this with your memory crash course's thread/summary machinery is exactly how you'd add conversation history on top of this).

### ⏱️ ~20 minutes

---

## 8. Lesson 8 — Wiring It Together: End-to-End RAG API

### 🎯 Objective
Expose ingestion and querying as a small FastAPI service — the only lesson in this course that touches a web framework.

### 🧠 Why This Matters
Every prior lesson works as a standalone script, which is deliberate: it means you've validated chunking, embedding, indexing, retrieval, and generation independently, in isolation, before combining them behind an HTTP boundary. This lesson is *thin* on purpose — the two endpoints below are almost entirely a pass-through to functions you've already built and tested. If your API code ends up doing anything nontrivial here, that logic belongs one layer down, not in the route handler.

### 📥 Dependencies
```bash
uv add "fastapi[standard]"
```

### 🛠️ What To Build
`api/main.py` with two endpoints:
- `POST /ingest` — re-runs the Lesson 3→5 pipeline (load → chunk → embed → index) on demand. In a real system this would be triggered by a doc-change webhook, not called synchronously per-request — flagged below.
- `POST /query` — takes `{question, k?, team?, doc_type?}`, runs Lesson 6→7's retrieve-then-generate chain, returns `{answer, sources}`.

### 💡 Core Pattern
```python
# The point of this snippet: the route handler has almost no logic of
# its own — it validates input shape and delegates. That's the signal
# you got the layering right in Lessons 3-7.
from fastapi import FastAPI
from pydantic import BaseModel

from rag.generation.chain import answer_question
from rag.indexing.embed_and_index import index_chunks
from rag.ingestion.chunker import chunk_documents
from rag.ingestion.loader import load_documents
from rag.retrieval.retriever import get_vector_store

app = FastAPI(title="DevPortal RAG API")
vector_store = get_vector_store()

class QueryRequest(BaseModel):
    question: str
    k: int = 5
    team: str | None = None
    doc_type: str | None = None

@app.post("/ingest")
async def ingest():
    docs = load_documents()
    chunks = chunk_documents(docs)
    index_chunks(chunks)
    return {"chunks_indexed": len(chunks)}

@app.post("/query")
async def query(req: QueryRequest):
    result = answer_question(
        vector_store, req.question, k=req.k, team=req.team, doc_type=req.doc_type,
    )
    return {"answer": result["answer"], "sources": result["sources"]}
```

### 🤖 AI Build Prompt
```text
Using fastapi[standard], generate src/rag/api/main.py exactly as
scoped above: POST /ingest (re-runs load_documents -> chunk_documents
-> index_chunks, returns chunk count) and POST /query (Pydantic
QueryRequest with question, k, team, doc_type; calls answer_question
from Lesson 7's chain.py; returns answer + sources only, not
raw_chunks — keep the wire response lean). Instantiate the vector
store connection ONCE at module load, not per-request. Add a GET
/health returning {"status": "ok"}. Do not add authentication, rate
limiting, request logging middleware, or CORS config — explicitly out
of scope for this lesson.
```

### ✅ Done When
`uv run fastapi dev src/rag/api/main.py`, then `POST /ingest` returns a chunk count, and `POST /query` with `{"question": "how do I roll back a deployment?"}` returns a grounded answer citing `deploy.md`.

### 🔑 Concepts You Must Be Able to Explain
Why the vector store connection is instantiated once at startup, not per-request (connection overhead, and Pinecone's client is safe to reuse across requests). Why `/ingest` as a synchronous request/response endpoint is a demo simplification — for any real corpus, ingestion is a background job (queue-triggered or scheduled), because embedding hundreds of documents inside an HTTP request timeout window doesn't scale and blocks the caller for no reason.

### ⏭️ Deferred (Production Extension)
Auth, rate limiting, async background ingestion (Celery/RQ/a queue), request logging and tracing, streaming `/query` responses (server-sent events), CORS — all standard FastAPI production concerns, none specific to RAG, all skipped here to keep the lesson about the pipeline, not the framework.

### ⏱️ ~20 minutes

---

## 9. Lesson 9 — Retrieval Evaluation

### 🎯 Objective
Stop eyeballing whether answers "look right" and measure retrieval and generation quality with actual numbers, using Ragas.

### 🧠 Why This Matters
Every lesson so far has been validated by you reading output and deciding "yeah, that looks right." That doesn't scale, doesn't catch regressions when you change chunk size or `k`, and — critically — can't tell you *which stage* is wrong when an answer is bad. Ragas gives you separable metrics for exactly the two failure modes Lesson 2 named: retrieval quality and generation faithfulness.

```text
Context Precision   Of the chunks retrieved, how many were actually
                     relevant to the question? Low score = retrieval
                     is pulling noise (tune k down, or add filtering).

Context Recall      Of the chunks that WOULD have answered the
                     question, how many did retrieval actually find?
                     Low score = retrieval is missing the answer
                     entirely (tune chunk size, k up, or embedding
                     model — a generation-prompt fix cannot help this).

Faithfulness        Of the claims in the generated answer, how many
                     are actually supported by the retrieved context?
                     Low score with high context recall = the RIGHT
                     chunks were retrieved but the model still
                     hallucinated — a generation/prompt problem, not
                     a retrieval problem.

Response Relevancy  Does the generated answer actually address the
                     question asked, independent of faithfulness? A
                     faithful-but-off-topic answer scores low here.
```

The reason these are separate metrics, not one "RAG score," is the same reason Lesson 2 insisted on naming pipeline stages precisely: **faithfulness and context recall can move independently, and they imply completely different fixes.** High recall + low faithfulness means your retrieval is fine and your prompt or model is the problem. Low recall means no prompt fix will ever help — the answer genuinely isn't in what got retrieved.

**Beginner approach:** skip evaluation, ship, find out retrieval is bad from user complaints.

**Production approach:** a small (10–30 question) hand-labeled eval set run against Ragas before every meaningful pipeline change (chunk size, `k`, embedding model, prompt wording), tracked over time so you can see whether a change helped or hurt.

**Enterprise approach:** the eval set grows continuously from real production queries (with PII scrubbed and human-reviewed labels), evaluation runs in CI on every pipeline-affecting PR, and dashboards track these four metrics over time in production as a leading indicator of quality drift — not just a pre-deploy gate.

### 📥 Dependencies
```bash
uv add ragas
```

### 🛠️ What To Build
- `evaluation/eval_dataset.py` — 6–8 hand-written `{question, ground_truth}` pairs against your DevPortal docs (e.g. "What's the on-call escalation path?" with a known-correct answer you wrote by reading `on_call.md` yourself).
- `evaluation/run_eval.py` — runs each question through your full retrieve → generate pipeline, assembles a Ragas `EvaluationDataset`, and runs `evaluate()` with the four metrics above.

### 💡 Core Pattern
```python
# The point of this snippet: you evaluate the pipeline you actually
# built, not a mocked version of it — retrieved_contexts comes from
# the SAME retrieve() call your API uses, not a hand-picked "ideal"
# context list, or you're evaluating a system you don't run.
from ragas import EvaluationDataset, evaluate
from ragas.metrics import ContextPrecision, ContextRecall, Faithfulness, ResponseRelevancy

def build_eval_dataset(vector_store, qa_pairs: list[dict]) -> EvaluationDataset:
    rows = []
    for pair in qa_pairs:
        result = answer_question(vector_store, pair["question"])
        rows.append({
            "user_input": pair["question"],
            "response": result["answer"],
            "retrieved_contexts": [doc.page_content for doc, _ in result["raw_chunks"]],
            "reference": pair["ground_truth"],
        })
    return EvaluationDataset.from_list(rows)

results = evaluate(
    dataset=build_eval_dataset(vector_store, qa_pairs),
    metrics=[ContextPrecision(), ContextRecall(), Faithfulness(), ResponseRelevancy()],
)
print(results)
```

### 🤖 AI Build Prompt
```text
Using ragas, generate:
1. src/rag/evaluation/eval_dataset.py — a list of 6-8 dicts with
   "question" and "ground_truth" keys, each answerable from exactly
   one of the six DevPortal docs (write the ground_truth yourself by
   reading the doc; don't invent facts not present in it).
2. src/rag/evaluation/run_eval.py — build_eval_dataset() as shown
   above (reusing answer_question from Lesson 7, NOT reimplementing
   retrieval/generation), then evaluate() with ContextPrecision,
   ContextRecall, Faithfulness, and ResponseRelevancy. Print a summary
   table: metric name, score, one-line interpretation of what a low
   score on that specific metric would mean for THIS pipeline.
```

### ✅ Done When
`uv run python -m rag.evaluation.run_eval` completes and prints all four scores. Faithfulness should score high (near 1.0) if Lesson 7's grounding instruction is working — if it's noticeably low, that's a real signal to go back and check your prompt, not a metric to ignore.

### 🔑 Concepts You Must Be Able to Explain
Why faithfulness and context recall are separate metrics with different fixes, not two readings of "quality." Why the eval harness must call your actual pipeline functions (not a hand-crafted mock) to be trustworthy. What a low context-precision-with-high-recall combination means (retrieval finds the answer but also pulls a lot of noise alongside it — a `k`/filtering tuning problem, not a missing-data problem).

### ⏭️ Deferred (Production Extension)
CI-gated evaluation on every pipeline change; a growing, production-sourced eval set; automated chunk-size/k sweeps scored against this harness; monitoring these metrics (or cheaper proxies for them) on live traffic, not just a static eval set.

### ⏱️ ~15 minutes

---

## 10. Lesson 10 — Common RAG Pitfalls & Optimization

### 🎯 Objective
Name the failure modes you're now equipped to recognize, and add the two highest-leverage production upgrades: reranking and hybrid search.

### 🧠 Why This Matters
This lesson is conceptual-heavy and code-light on purpose — most of what makes RAG "production-grade" isn't a new component, it's knowing which of the pieces you already built to tune, and in what order, when quality isn't good enough.

### 📋 Common Pitfalls (and what actually fixes each one)

| Pitfall | Symptom | Root cause | Fix |
|---|---|---|---|
| **Lost in the middle** | Answer ignores a clearly-relevant chunk that WAS retrieved | LLMs attend less to context buried mid-prompt, more to the start/end | Fewer, higher-quality chunks (rerank down to k=3-5); order by relevance, most-relevant closest to the question |
| **Chunk-boundary information loss** | Answer is partial or misses a qualifier ("...unless X") that got split into the next chunk | Chunk size/overlap too aggressive for this content | Increase overlap; use structure-aware splitting (Lesson 3) |
| **Embedding/query length mismatch** | Short, terse queries retrieve poorly even when the answer chunk is well-written | A 5-word query and a 200-word chunk don't embed into directly comparable regions of the space as reliably as two similarly-sized texts | Query rewriting/expansion, or HyDE (below) |
| **Stale index** | Answers cite outdated info even after the source doc was updated | Ingestion wasn't re-run after the doc changed | A re-indexing trigger (webhook, schedule) — not a RAG-specific problem, a data-freshness problem |
| **Retrieval-generation mismatch** | Confidently wrong answer despite irrelevant retrieved chunks | Weak or missing grounding instruction (Lesson 7) | Re-check the system prompt; verify with Lesson 9's faithfulness metric, not by eye |
| **Over-restrictive metadata filter** | Zero results, or a refusal, on a question that IS answerable | Filter combination too narrow for the corpus | Loosen filters progressively; log zero-result queries |
| **Full re-embedding on every change** | Ingestion cost/time scales with total corpus size instead of change size | No content-hash check before re-embedding | Hash each chunk's content; skip embedding+upsert for unchanged hashes |

### 🚀 Optimization: Reranking

Retrieval and reranking solve different problems. Retrieval (Lesson 6) has to be fast enough to search millions of vectors — it uses a cheap bi-encoder (embed query and chunk separately, compare vectors). A **reranker** is a slower, more accurate cross-encoder that looks at the query and each candidate chunk *together* and scores relevance directly — too slow to run over a whole index, but cheap enough to run over the 15–25 candidates your retriever already narrowed things down to. This is the standard **two-stage retrieval** pattern: cast a wide net cheaply, then rerank down to the few chunks that actually go in the prompt.

```python
# Pinecone's hosted reranker — no separate API key needed, same
# Pinecone client you already have. bge-reranker-v2-m3 is a
# cross-encoder: it scores (query, chunk) pairs jointly, which is why
# it's more accurate than pure vector similarity for the final cut.
def rerank(pc: Pinecone, query: str, scored_docs: list[tuple], top_n: int = 5) -> list[tuple]:
    docs_only = [doc.page_content for doc, _score in scored_docs]
    result = pc.inference.rerank(
        model="bge-reranker-v2-m3",
        query=query,
        documents=docs_only,
        top_n=top_n,
        return_documents=False,
    )
    return [scored_docs[r.index] for r in result.data]
```

Wire this between Lesson 6's `retrieve(k=20)` and Lesson 7's `format_docs` — retrieve wide, rerank narrow, generate from the narrow set.

### 🚀 Optimization: Hybrid Search

Pure dense (embedding) search is weak on exact matches — a chunk containing the literal string `RATE_LIMIT_EXCEEDED` or an internal ticket ID doesn't necessarily embed "close" to a query containing that same string, because embeddings capture meaning, not exact tokens. **Hybrid search** combines dense vectors with a sparse (keyword/BM25-style) representation, so exact terms get exact-match credit while the dense side still handles paraphrased questions. Pinecone supports this via sparse-dense indexes (`metric="dotproduct"`) with both `values` and `sparse_values` on each vector — worth reaching for the moment your corpus includes error codes, product names, or IDs users will paste verbatim into a query, which this course's thin DevPortal corpus deliberately doesn't need.

### 🔑 Concepts You Must Be Able to Explain
Why a reranker can afford to be slower and more accurate than the initial retriever — because it runs over 20 candidates, not 20 million. Why "lost in the middle" is a reason to rerank down to fewer chunks, not just a reason to write a better prompt. When hybrid search earns its complexity (exact-match-sensitive corpora) versus when it doesn't (this course's corpus).

### ⏭️ Deferred (Production Extension)
Query rewriting and HyDE (Hypothetical Document Embeddings — ask an LLM to draft a hypothetical answer first, then embed *that* instead of the raw query, which often retrieves better because it's closer in style/length to what's actually indexed) — genuinely useful, deliberately cut here to keep this course's total time honest. Semantic caching of repeated queries. Full hybrid sparse-dense indexing.

### ⏱️ ~15 minutes

---

## 11. Lesson 11 — Recap, Comparison, and What's Next

### 🎯 Objective
Consolidate what you built into language you can defend in a design review or interview, and know exactly what to build next.

### 🧠 Full System Recap
```text
data/docs/*.md          → source of truth, never embedded directly
Document (loader.py)     → doc-level metadata attached
Chunk (chunker.py)       → retrievable unit, metadata inherited
Embedding (OpenAIEmbeddings) → chunk meaning as a vector
Pinecone index            → ANN-searchable vector storage, dimension
                             locked to your embedding model
retrieve() (retriever.py) → query embedding + vector search +
                             metadata filter -> scored candidate chunks
rerank() (Lesson 10)       → cross-encoder narrows candidates
format_docs + prompt        → augmentation: numbered, grounded context
ChatOpenAI                   → generation, conditioned on that context
Ragas eval                    → separates retrieval quality from
                                 generation faithfulness, numerically
```

### 📊 Naive vs. Production vs. Enterprise RAG — When to Choose Which

| | Naive RAG | Production RAG (this course) | Enterprise RAG |
|---|---|---|---|
| Chunking | Fixed character count | Recursive, structure-aware | Semantic/layout-aware, size auto-tuned against eval |
| Retrieval | Single-stage top-k | Wide retrieval + metadata filter | + reranking + hybrid dense/sparse |
| Access control | None | Caller-supplied filter (demo-safe only) | Session-derived, server-enforced filter |
| Generation | Unstructured prompt, no grounding instruction | Grounding instruction + numbered citations | + real-time faithfulness guardrail pass |
| Evaluation | None ("looks right") | Static hand-labeled eval set, run manually | CI-gated, production-sourced, drift-monitored |
| Indexing | Full re-embed every run | Idempotent upsert via deterministic IDs | Content-hash incremental indexing, versioned migrations |
| Multi-tenancy | N/A | N/A | Namespace-per-tenant isolation |

None of the rows are "wrong" in isolation — naive RAG is the right choice for a one-off internal script, and this course deliberately stops at the "Production RAG" column because that's the version worth understanding deeply before reaching for enterprise complexity you may not need yet.

### 🌉 Bridge: What This Course Deliberately Left Out
| Topic | Why deferred | Where to go next |
|---|---|---|
| Agentic RAG / query routing | Needs multiple retrievers or tools and a decision layer — that's the domain of the graph/agent frameworks, not RAG mechanics itself | LangGraph — combine this course's `retrieve()`/`answer_question()` as tools inside a graph node, and reuse your **memory crash course**'s checkpointing/summarization for multi-turn conversations grounded in this index |
| Query rewriting / HyDE | Genuinely useful, cut here to protect the time budget | One new function ahead of `retrieve()`: LLM call to rewrite the query before embedding it |
| Hybrid dense+sparse search | This course's corpus doesn't have exact-match-sensitive content to justify it | Pinecone sparse-dense indexes, `metric="dotproduct"` |
| Production API concerns (auth, rate limiting, streaming, background ingestion) | Standard FastAPI concerns, not RAG-specific | Any FastAPI production guide — nothing here changes based on RAG |
| CI-gated evaluation, production monitoring of retrieval/faithfulness drift | Needs a deployed system with real traffic to be meaningful | Wire Lesson 9's `run_eval.py` into your CI pipeline as a first step |
| GraphRAG / knowledge-graph-augmented retrieval | A meaningfully different retrieval paradigm (graph traversal, not pure vector similarity), not a small extension | Worth a dedicated deep-dive once vector-based RAG's limits are actually the bottleneck you're hitting — don't reach for it earlier |

### ⏱️ ~10 minutes

---

## Appendix — What This Crash Course Never Builds (By Design)

Authentication, a persistent application database, multi-tenant namespace isolation, streaming responses, background job infrastructure, CI/CD, Kubernetes, agentic query routing, knowledge graphs, fine-tuned embedding models, and a frontend. All legitimate production concerns — none of them RAG mechanics, which is the entire scope of this course.
