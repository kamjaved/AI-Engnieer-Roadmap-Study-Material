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

## Lesson 5 — Vector Store & Indexing (the write path)

### Q1. Why must a Pinecone index's `dimension` exactly match the embedding model's output size, and what concretely happens if it doesn't?

**Answer:** Pinecone pre-allocates storage for a fixed vector length set at index-creation time. Upsert a vector of a different length (e.g. 3072-dim into a 1536-dim index) and Pinecone rejects it immediately — a loud, hard error, nothing gets stored. The more dangerous case is a same-dimension mismatch: switching to a different model that happens to output the same length passes every check and stores fine, but the vectors now represent an incompatible coordinate space — similarity search runs without error and quietly returns meaningless results.

**Key points:**
- Dimension is fixed and pre-allocated at index-creation time, not adjustable per-upsert
- Wrong dimension → Pinecone rejects the upsert outright (loud, immediate failure)
- Same dimension, different model → passes every check, but vectors are geometrically incompatible
- That second case is silent: no crash, just quietly wrong retrieval results
- Always derive dimension from the embedding model in use via a lookup table — never hardcode it

**Common mistake:** Assuming any error at all means "safe" — the scarier failure mode (different model, same dimension) produces no error whatsoever.

---

### Q2. Why is a deterministic vector ID (like a content-derived `chunk_id`) a production requirement rather than a nicety?

**Answer:** Without a deterministic ID, re-running ingestion generates a fresh random ID for every chunk each time, so unchanged content gets inserted as brand-new vectors on every run — duplicates pile up forever. A deterministic ID (e.g. `f"{source}::{index}"`) means the same chunk always maps to the same vector ID, so re-running ingestion overwrites existing vectors in place instead of duplicating them. This is also what makes safe incremental updates possible: re-index just one changed document without deleting and rebuilding the entire index.

**Key points:**
- No deterministic ID → every re-run creates fresh random IDs → duplicate vectors pile up
- Deterministic ID → same chunk always maps to the same vector ID → re-run overwrites in place
- This is what makes idempotent, safe re-runs of ingestion possible
- Also enables incremental updates: re-index one changed doc without rebuilding the whole index
- Avoids the cost and downtime of a full index rebuild on every content change

**Common mistake:** Thinking deterministic IDs are only about avoiding duplicate rows — the bigger production payoff is enabling safe incremental re-indexing.

---

### Q3. What is a Pinecone namespace, and when would you reach for one instead of a metadata filter?

**Answer:** A namespace is a hard partition inside a single Pinecone index — vectors in one namespace are structurally unreachable from a query scoped to another namespace, similar to a separate schema per tenant in Postgres. A metadata filter (e.g. `team`/`doc_type`) is different: it's a `WHERE`-clause-style constraint applied at query time over one shared pool of vectors, so its correctness depends on every query remembering to apply it. Reach for namespaces when isolation must be guaranteed even against a missed filter (true multi-tenant SaaS); metadata filtering suits single-tenant categorization, like one company's internal docs split by team.

**Key points:**
- Namespace = structural partition inside one index; a query scoped to one namespace cannot see another's vectors, even by accident
- Metadata filter = `WHERE`-clause-style constraint over a shared pool; correctness depends on the query always applying it
- Pinecone applies a default namespace automatically when none is specified
- Namespaces suit true multi-tenant isolation (a data leak there is a security incident)
- Metadata filters suit single-tenant categorization (e.g. one company's docs split by `team`/`doc_type`)

**Common mistake:** Relying on metadata filters alone for true multi-tenant data isolation — a single missed filter in one code path means one tenant's data leaks into another's search results.

---
## Lesson 6 — Retrieval & Metadata Filtering (the read path)

### Q1. Why does metadata filtering happen at the vector-search layer (`filter=` inside the similarity search call), instead of retrieving a wide set of results first and filtering them afterward with plain Python?

**Answer:** Filtering inside the vector search means the "top-K" is chosen only from candidates that already match the filter, so relevant results aren't crowded out by irrelevant ones before scoring even happens — important at scale, where a truly relevant result might not appear anywhere near the top of an unfiltered ranking. It's also cheaper: narrowing the search space first avoids ranking across an entire index only to discard most of the results. And it's the real enforcement point for access control — a filter baked into the query can't be skipped, unlike a post-hoc check every future code path has to remember to add.

**Key points:**
- Filtering pre-narrows the candidate pool before ranking, so top-K slots go to in-scope results, not irrelevant ones
- At scale, a genuinely relevant result could rank far outside a small top-K if filtered only afterward
- Pre-filtering is cheaper — avoids ranking across the whole index just to discard most results
- Filtering inside the query is the actual access-control enforcement point — can't be accidentally skipped downstream
- Post-hoc filtering means every future code path touching results must remember to reapply the check

**Common mistake:** Assuming post-hoc filtering gives "the same result, just done later" — at scale it can silently drop genuinely relevant results that never made it into an unfiltered top-K in the first place.

---

### Q2. A retrieved chunk comes back with `score=0.2244`. Is that "22% confident this is the right answer"? Why or why not?

**Answer:** No. Cosine similarity is just the angle between two vectors — nothing about how it's computed was ever trained against real correctness labels, so there's no universal scale where a given number means a fixed "% correct." A 0.73 on one query might be a strong match, while a 0.6 on a completely different query might already be the best match available in the whole index. Scores are meaningful when compared *within* the same query (e.g. filtered vs. unfiltered runs) — treating one score in isolation as a confidence percentage is not.

**Key points:**
- Cosine similarity = geometric angle between two vectors, not a probability
- Never calibrated against ground-truth correctness — no classifier trained it to mean "% likely correct"
- No universal threshold (e.g. "0.7 = good") — the meaningful scale depends on the query and domain
- Valid use: comparing scores *within* one query's results (e.g. filtered vs. unfiltered), not across queries or in isolation
- A high score can still be the wrong chunk (similar wording, wrong content); a lower score can still be the right one (same fact, different phrasing)

**Common mistake:** Presenting a raw similarity score to end users as a "% match" or confidence value — it has no calibrated relationship to actual correctness.

---

### Q3. Production retrieval often uses a "wide retrieval, then narrow" pattern — e.g. retrieve `k=15–25`, then cut down to a handful before generation. How is that different from just calling `retrieve()` with `k=5` directly?

**Answer:** It's two different tools doing two different jobs, not just "get more, then pick fewer." The first stage (vector search) is optimized for speed and recall at scale — fast, approximate nearest-neighbor search across a potentially huge index. The second stage (a reranker) is optimized for precision on a small set — it can afford to be slower and more accurate specifically because it's only evaluating 15–25 candidates, not the whole index. Calling `retrieve()` with `k=5` directly relies on a single fast-but-approximate pass to also be maximally precise, risking missed relevant results a wider first pass would have caught.

**Key points:**
- Two-stage pattern = two different tools, each suited to its own job, not one tool doing double duty
- Stage 1 (wide vector search): optimized for recall and speed at scale
- Stage 2 (narrow/rerank): optimized for precision, affordable specifically because the candidate set is already small
- Direct `k=5` risks missing a relevant chunk that would have ranked outside the top 5 but inside the top 20
- The reranker's extra cost is only viable because it never runs against the full index — just the narrowed candidate set

**Common mistake:** Treating "wide then narrow" as equivalent to just picking a smaller `k` upfront — the point is using a cheap-and-wide tool first, then a slow-and-accurate tool second, not skipping straight to precision with one pass.

---
