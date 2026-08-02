# Interview Q&A — Modern RAG Crash Course

> A running interview-revision guide, built one assessed question at a time as the course progresses. By the end of the course this should read as a clean, standalone revision sheet — not a transcript of how we got there.

## Instructions for the AI (read this before writing anything here)
- Add an entry here only for questions Kamran was actually asked and answered as part of a lesson's self-check / concept-check (e.g. Lesson 2's 2.8/2.9, Lesson 2.5's 2.5.6) — not for material that was only explained, with no question actually posed and answered.
- For each question, record **only**: the question, the final correct answer (max 100 words), 3–6 key points, and — optionally — a common interview mistake. Do **not** record Kamran's incorrect attempts, the back-and-forth, or how many tries it took to land — that history belongs in `lesson-notes.md`'s "Self-check / confirmation results" section, not here. This file is a clean revision guide only.
- Group entries under `## Lesson N — <Title>` headings, in lesson order, matching `progress-tracker.md`.
- Update this file at the same time as `progress-tracker.md` and `lesson-notes.md` — once, at lesson end, not after every individual question.
- Style: plain engineering language, practical intuition over jargon — Kamran reads this to build an accurate mental model fast, not to see technical vocabulary.

---

## Lesson 2.5 — PDF Ingestion (Tier 1)

### Q1. Why is `PyPDFLoader` page-granular instead of file-granular, and what does that mean for how you apply metadata? How does that compare to how `RecursiveCharacterTextSplitter` handles metadata during chunking?

**Answer:** `PyPDFLoader` returns one `Document` per PDF page, not one per file, because that's how the underlying PDF library reads pages. Every page from the same file needs the same `team`/`doc_type`, but each keeps its own page number, so metadata must be attached manually, per page, in a loop — `PyPDFLoader` doesn't know your custom fields. By contrast, `RecursiveCharacterTextSplitter` (used later for chunking) copies existing metadata onto every chunk automatically, because by then the source `Document` already carries metadata from loading — regardless of whether it originally came from a markdown file or a PDF page.

**Key points:**
- `PyPDFLoader` → 1 `Document` per page (not per file) — a real structural difference from markdown loading
- `team`/`doc_type` must be attached manually, per page, in a loop
- Merge with `.update()`, don't overwrite — or you lose `PyPDFLoader`'s own `page` field
- This manual work happens only at the **loading** stage, not chunking
- At the **chunking** stage, metadata copying is automatic for *every* `Document`, no matter its original format

**Common mistake:** Assuming metadata propagation is "automatic" everywhere in a RAG pipeline. It's automatic at chunking (splitting an existing `Document`) but manual at loading (creating `Document`s from raw files) — two different stages, two different rules.

---

### Q2. Why does dispatching by file suffix inside `loader.py` mean `chunker.py` and every stage after it never needs to know or care that some source documents are PDFs?

**Answer:** `loader.py`'s job is to turn every input file, regardless of format, into the same shape: a `Document` with text and metadata (`source`, `team`, `doc_type`). Once that conversion happens, every later stage — chunking, embedding, indexing, retrieval — only ever works with `Document` objects. None of them branch on file type or know a PDF was ever involved. This isolates format-specific logic (`PyPDFLoader` vs. a plain text read) to a single place, so adding a new format later, like `.docx`, only means changing `loader.py`, not every stage after it.

**Key points:**
- `loader.py` normalizes every format into the same `Document` shape
- Downstream stages only ever see `Document` objects, never raw files
- Format-specific logic stays isolated in one place, not scattered across the pipeline
- Adding a new file format later only touches `loader.py`
- This is a general software design principle (separation of concerns), not RAG-specific

**Common mistake:** Sprinkling "if it's a PDF, do X" checks across multiple pipeline stages instead of isolating format handling at one boundary (the loader) — makes the codebase harder to extend and test.

---

### Q3. Where does "Tier 1" (PDF ingestion as built in this lesson) stop, and "Tier 2/3" begin — and why is the boundary drawn at "known file, no client" vs. "arbitrary file, from a client"?

**Answer:** Tier 1 covers ingesting files you already know and trust — pre-created, placed on disk yourself, no external upload path. Tier 2 adds a real upload endpoint accepting files from a client over the network. Tier 3 adds production-grade validation and security for those client files: checking actual file bytes instead of trusting the extension, enforcing size limits, scanning for malware, and using safe, non-filename-derived storage paths to avoid path-traversal attacks. The boundary matters because trust changes completely once a stranger can supply the file — you no longer know what's actually inside it.

**Key points:**
- Tier 1: known, pre-created files, no client involved — full trust
- Tier 2: a real HTTP upload endpoint accepting client-supplied files
- Tier 3: production security for those uploads — byte-level validation, size limits, malware scanning, non-filename-derived storage
- Core risk without Tier 3: a malicious filename used to build a file path is a real path-traversal vulnerability
- The boundary is about *who supplied the file* (self vs. a stranger), not file type or size

**Common mistake:** Treating "we check the file extension" as sufficient upload security — extensions are trivially spoofable; real validation checks the file's actual bytes/content.

---

## Lesson 3 — Documents → Chunks

### Q1. Why is `chunk_size` something you have to tune per-corpus, not a fixed "correct" number? What goes wrong if it's too small, and what goes wrong if it's too big?

**Answer:** Chunk size balances two competing needs. Smaller chunks give retrieval a sharper, more specific embedding — better precision — but risk cutting a complete idea across a boundary, losing meaning. Larger chunks give generation more surrounding context, but dilute the embedding (mixing multiple ideas into one vector) and can bury the real answer in irrelevant text, wasting tokens and risking the "lost in the middle" effect. There's no universal correct size — it depends on how self-contained a single idea is in your content, tuned empirically against real queries, not guessed from document length.

**Key points:**
- Small chunks → precise, focused embeddings → sharper retrieval matches
- Small chunks risk cutting a complete idea in half, losing meaning
- Large chunks → more context for generation, but dilute the embedding by averaging multiple ideas
- Large chunks waste prompt budget and risk the "lost in the middle" effect
- Tune based on content structure/density, not raw document length
- Validate empirically against real queries — don't guess once and stop

**Common mistake:** Assuming "bigger chunks are always better for generation." Oversized chunks hurt both retrieval precision and generation quality, not just retrieval.

---

### Q2. Why does metadata (`source`/`team`/`doc_type`) have to be attached to a `Document` before it gets split into chunks, rather than after? What would break if you tried to attach it after chunking instead?

**Answer:** LangChain's text splitters copy a parent `Document`'s existing metadata onto every chunk they produce — a copy operation, not something invented at split time. If metadata isn't attached before splitting, there's nothing to copy, and you'd have to manually reconstruct which source file every one of dozens of chunks came from — exactly the bookkeeping automatic propagation gives you for free. Attaching metadata after chunking also breaks source citation: without it, a retrieved answer can't be traced back to the document it came from.

**Key points:**
- `split_documents()` copies existing metadata forward — a copy, not an invention
- Nothing to copy from if metadata isn't attached before splitting
- Attaching after would mean manually mapping each of dozens of chunks back to its source
- Direct consequence of skipping this: losing the ability to cite sources in answers
- This attachment happens at the loading stage, before any splitter runs

**Common mistake:** Assuming metadata can be "cleaned up" after chunking — by then the natural one-to-one link between a chunk and its original document is gone.

---

### Q3. In `RecursiveCharacterTextSplitter`, what is the splitter actually recursing over?

**Answer:** The recursion is over the separator priority list, applied within a single piece of text — not recursion over your list of documents (processing multiple documents is a plain loop). The splitter tries the first separator (paragraph breaks, `\n\n`); if a resulting piece is still too big, it recursively applies the next separator (line breaks, then `". "`, then space) to that same piece, falling all the way to character-level splitting as a last resort. This produces cleaner cuts than a single fixed separator would.

**Key points:**
- Recursion = trying separators in priority order, not looping over documents
- Order: paragraph breaks → line breaks → sentence-ish breaks → spaces → raw characters
- Each fallback only applies to a piece still too big after the previous separator
- Character-level splitting is the last resort, used only when nothing else fits
- Produces cleaner chunk boundaries than a single fixed-separator splitter would

**Common mistake:** Describing "recursive" as iterating over multiple documents — that part of the pipeline is a simple loop, not recursion.

---

### Q4. Parent-child chunking means storing two copies of your content instead of one. When is that extra storage and complexity worth paying for, and what specifically breaks if you use plain recursive chunking alone?

**Answer:** Parent-child chunking earns its cost for structured, dense content where an isolated chunk is misleading alone — a price-table row with no column headers, a form field with no label. Search runs against small, precise child chunks; a matching child promotes its linked, larger parent to the LLM, restoring surrounding context. It's not a guarantee, though — the parent splitter is still character-count-driven, so a table header can still fall outside even a wider window. Parent-child reduces the risk of losing context; it doesn't eliminate it.

**Key points:**
- Search targets small child chunks; a match promotes to its linked, larger parent
- Worth the extra storage for structured content (tables, forms) where isolated chunks lose meaning
- Not worth it for flowing prose, where one well-sized chunk is usually already self-contained
- Parent-child reduces the odds of losing context — it does not guarantee keeping it
- Real production fix for tables: denormalize headers into every row's own text, don't just rely on window size

**Common mistake:** Treating parent-child chunking as a guaranteed fix for context loss — it's a probability improvement, still blind to actual document structure.

---

## Lesson 4 — Embeddings: The Vector Space Mental Model

### Q1. Why is it non-negotiable that the same embedding model be used at index-time and query-time — and why does getting this wrong fail silently instead of throwing an error?

**Answer:** Each embedding model produces vectors in its own private geometric space — the same text embedded by two different models lands in different coordinates, so comparing vectors from different models is meaningless. This fails silently because vector databases only store arrays of numbers; they don't know or validate which model produced them. If the two models output different dimensions, the similarity math throws a hard shape-mismatch error. But if two different models happen to share a dimension, cosine similarity still returns a normal-looking number — the failure is semantic, not syntactic, so nothing crashes and retrieval quality just quietly gets worse.

**Key points:**
- An embedding model = a fixed, private vector-space geometry — not interchangeable with another model's
- Vector DBs (Pinecone, FAISS, etc.) store plain number arrays with no awareness of which model made them
- Different dimensions (3072 vs 1536 ) → hard crash (shape mismatch in the similarity math) 
e.g., text-embedding-3-large = 3072 numbers vs. text-embedding-3-small = 1536 numbers) → this actually does throw a hard, loud error. Your cosine_sim function would crash on the dot product — numpy can't multiply arrays of mismatched shape. You'd catch this in five seconds.
- Same dimensions, different model → silent failure — the math runs, the result is meaningless
- Changing `EMBEDDING_MODEL` requires a full re-index of every existing vector, not just a config edit

**Common mistake:** Assuming a config change to the embedding model is safe without re-indexing — old vectors silently become incompatible with new queries, and nothing errors to warn you.

---

### Q2. Why is cosine similarity specifically the right default for comparing text embeddings, rather than Euclidean distance?

**Answer:** Cosine similarity measures the angle between two vectors and ignores their length (magnitude). For text embeddings, direction encodes meaning, while magnitude often varies for reasons unrelated to meaning, like sentence length. Euclidean distance is sensitive to magnitude, so that noise can throw it off. OpenAI's embedding vectors happen to already be normalized to unit length, so for them cosine similarity and Euclidean distance are mathematically equivalent. Cosine remains the safer default anyway, because it stays correct even for embedding models that don't guarantee that normalization.

**Key points:**
- Cosine similarity = angle between two vectors; ignores magnitude/length entirely
- Direction encodes meaning; magnitude is often just noise (sentence length, tokenization quirks)
- Euclidean distance is sensitive to magnitude, so it can be misled by that noise
- OpenAI embeddings are pre-normalized to unit length — cosine and Euclidean give equivalent rankings for them specifically
- Cosine is still the safer default choice, since it doesn't depend on every embedding model guaranteeing normalization

**Common mistake:** Assuming cosine and Euclidean always rank results differently — for normalized vectors they don't; the real reason to default to cosine is not having to rely on that guarantee holding for every model.

---
