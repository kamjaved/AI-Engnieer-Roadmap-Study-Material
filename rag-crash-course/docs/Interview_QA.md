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
