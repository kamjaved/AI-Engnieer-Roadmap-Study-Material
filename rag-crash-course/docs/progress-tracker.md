# Progress Tracker — Modern RAG Crash Course

> Source of truth for what's actually done vs. pending. A box is checked **only** after Kamran has explicitly confirmed it — never inferred from context. If you're a fresh Claude session picking this up: trust this file over anything implied elsewhere, and don't mark anything complete without asking first.

**Note (added 2026-07-31) — roadmap sync audit:** after finding Lesson 2.5 missing from this file, Kamran asked for a full pass comparing every lesson heading in `docs/modern-rag-crash-course-roadmap.md` against this tracker, so we don't hit the same surprise mid-lesson again. Full lesson list per the roadmap (13 lessons total, confirmed via every `## ` heading in the file, cross-checked against the intro's own "Verification Notes" and "Month 2 Roadmap" mapping sections): **1, 2, 2.5, 3, 4, 5, 6, 6.5, 7, 8, 9, 10, 11.** Two discrepancies found and fixed at that time: (1) Lesson 6.5 — Query Transformation & Hybrid Retrieval Awareness was entirely missing — added as a placeholder in its correct roadmap position, between Lesson 6 and Lesson 7. (2) Lesson 5's and Lesson 6's titles here were missing the roadmap's own parenthetical suffixes, "(the write path)" and "(the read path)" — corrected. The roadmap's "Month 2" references (e.g. "Lesson 5.2", "Lesson 6.3") are a *different, later, bigger course* this crash course is a foundation for, not additional lessons of this course.

---

## Lesson 1 — Prerequisites & Lean Project Setup — ✅ COMPLETE

- [x] 1.1 Prerequisites confirmed (Python 3.13+ installed, `uv` installed, `OPENAI_API_KEY` obtained, `PINECONE_API_KEY` obtained)
- [x] 1.2 Project initialized (`uv init rag-crash-course --python 3.13`)
- [x] 1.3 Core dependencies installed via `uv add` (`langchain`, `langchain-openai`, `langchain-pinecone`, `langchain-text-splitters`, `pinecone`, `pydantic-settings`, `python-dotenv`)
- [x] 1.4 Dev dependency installed (`uv add --dev ruff`)
- [x] 1.5 Folder skeleton created — `src/rag/{ingestion,indexing,retrieval,generation,evaluation}` (each with `__init__.py`) and `data/docs/`
- [x] 1.6 `.env` created (`OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `EMBEDDING_MODEL`, `CHAT_MODEL`)
- [x] 1.7 `.gitignore` created (before any `git init`)
- [x] 1.8 `src/rag/config.py` written — pydantic-settings `BaseSettings` loading the five `.env` values, exporting a module-level `settings` instance
- [x] 1.9 Six seed markdown docs created under `data/docs/` (`hr_policies.md`, `employee_benefits_leave.md`, `travel_expense_policy.md`, `procurement_guidelines.md`, `product_catalog_faq.md`, `product_catalog_services_guide.md`)
- [x] 1.10 `DOC_METADATA` mapping stubbed in `src/rag/ingestion/loader.py` (each filename → `{"team": ..., "doc_type": ...}`)
- [x] 1.11 Done-When check: `uv run python -c "from rag.config import settings; print(settings.PINECONE_INDEX_NAME)"` runs with no import errors and prints the index name; all six markdown files confirmed present in `data/docs/`

**Note (added 2026-07-26):** 1.1–1.6 were found already physically set up on disk when this session picked up the course (pyproject.toml, uv.lock, .venv, full folder skeleton, and a populated `.env` all present). Kamran explicitly confirmed these as done rather than this being inferred. Full writeup — concepts, decisions, the `uv run` vs. bare `python` bug, exact commands — is in `lesson-notes.md`.

**Note (added 2026-07-31) — Domain pivot:** Kamran requested a full domain swap, replacing the original "DevPortal" knowledge base with a fictional company, **Turab Industries Pvt. Ltd.** (see the updated roadmap). The 1.9 and 1.10 rows above now reflect the *current* state: the original six DevPortal docs (`deploy.md`, `auth.md`, `rate_limits.md`, `on_call.md`, `migrations.md`, `incident_response.md`) have been deleted from `data/docs/` and replaced with the six Turab Industries docs listed in 1.9; `loader.py`'s `DOC_METADATA` was rewritten to match (six markdown entries, plus the two PDF entries — `corporate_gifts_price_list.pdf`, `company_overview.pdf` — already added for real, ahead of Lesson 2.5, since Kamran had both PDFs ready early). `.env`'s `PINECONE_INDEX_NAME` is confirmed set to `turab-industries` (hyphenated, correct). Lesson 1's original build (against the DevPortal domain) genuinely happened and is preserved as-is in `lesson-notes.md`, with its own supersession note added there rather than rewritten.

---

## Lesson 2 — The RAG Mental Model — ✅ COMPLETE

- [x] 2.1 Can explain why RAG exists at all — the fine-tuning vs. RAG tradeoff, and that RAG doesn't make the model "smarter," it gives the model's existing reasoning the right facts to work with
- [x] 2.2 Can explain the six core pipeline concepts in your own words: Document, Chunk, Embedding, Vector index, Retrieval, Augmentation, Generation
- [x] 2.3 Can explain the core relationship: "retrieval quality caps generation quality" — why a perfect prompt can't rescue chunks that don't contain the answer
- [x] 2.4 Can explain **Naive RAG**: the straight-line chunk→embed→retrieve→generate pipeline and its known failure modes (vocabulary mismatch, noisy retrieval, no recovery from a bad first attempt)
- [x] 2.5 Can explain **Advanced RAG**: the two specific upgrade points (pre-retrieval, post-retrieval) and why the pipeline's overall *shape* doesn't change
- [x] 2.6 Can explain **Agentic RAG**: what extra decision-making it adds (whether/how many times/with what query to retrieve) and why this course deliberately doesn't build it
- [x] 2.7 Can recognize **Modular RAG** and **GraphRAG** by name and state what each is for, even though neither is built in this course
- [x] 2.8 Self-check Q1 answered: "if a RAG app confidently answers a question wrong, list the distinct pipeline stages that could be the root cause, and a symptom that isolates each"
- [x] 2.9 Self-check Q2 answered: "why does Advanced RAG's definition specifically split into pre-retrieval and post-retrieval fixes, rather than just being 'any RAG system with more features bolted on'?"

**Note (added 2026-07-31) — closure process for this lesson:** 2.1–2.3 were taught and walked through live in this chat, with Kamran confirming each in turn before moving to the next. 2.4–2.9 were **not** walked through in this conversation — Kamran stated he'd already learned this theoretical material in advance and explicitly asked to mark the rest of the lesson complete and close the chapter. Recorded here rather than silently checked off. See `lesson-notes.md` for the full Lesson 2 entry.

---

## Lesson 2.5 — PDF Ingestion (Tier 1) — ✅ COMPLETE

- [x] 2.5.1 Dependencies installed: `uv add pypdf langchain-community`
- [x] 2.5.2 Confirmed `DOC_METADATA` already has entries for both PDFs — `corporate_gifts_price_list.pdf` → `{"team": "sales", "doc_type": "catalog"}`, `company_overview.pdf` → `{"team": "leadership", "doc_type": "guide"}`
- [x] 2.5.3 `ingestion/loader.py`'s `load_documents()` written — dispatches by file suffix: `.md` files get a plain raw-text read (one Document per file), `.pdf` files load via `PyPDFLoader(path).load()` (one Document per page) with `source` + `DOC_METADATA`'s `team`/`doc_type` merged onto every page-Document without overwriting `PyPDFLoader`'s own `page` field
- [x] 2.5.4 Preview `__main__` block written in `loader.py` — prints, for each of the two PDFs, total page count and the first page's metadata keys
- [x] 2.5.5 Done-When check: `uv run python -m rag.ingestion.loader` ran cleanly — `corporate_gifts_price_list.pdf` loaded 2 pages, `company_overview.pdf` loaded 1 page, every page's metadata included `source`/`team`/`doc_type`/`page`
- [x] 2.5.6 Concept check answered — page-granularity vs. file-granularity and manual-vs-automatic metadata propagation; why suffix-dispatch keeps downstream stages format-agnostic; the Tier 1 vs. Tier 2/3 boundary

**Note (added 2026-07-31):** this lesson was missing from the tracker entirely until caught mid-course (see Lesson 3's note below and the roadmap-sync note at the top of this file). Its build required writing `load_documents()` from scratch — the roadmap's own wording assumed a prior "Lesson 1 raw-read logic" that, on inspection, was never actually built (Lesson 1 only ever stubbed `DOC_METADATA`). A real `langchain-community` deprecation warning surfaced while running the Done-When check and was researched live rather than ignored — see `lesson-notes.md` for what was found. The concept check needed two clarification passes on Q1 (page-granularity vs. chunking's automatic metadata copy — an early explanation wrongly implied metadata copying was markdown-only) and a full plain-language re-explanation on Q3 (Tier 1/2/3), after which Kamran gave direct feedback that explanations should be simpler and less jargon-heavy going forward — teaching style adjusted accordingly from this point on. Full Q&A now also captured in `docs/Interview_QA.md`, started with this lesson.

---

## Lesson 3 — Documents → Chunks — 🔄 IN PROGRESS

- [ ] 3.1 `ingestion/chunker.py` written — `chunk_documents(docs)` using `RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=75, separators=["\n\n", "\n", ". ", " ", ""])`, propagating each parent `Document`'s existing metadata onto every chunk automatically, plus adding a new, deterministic `chunk_id` field (`f"{source}::{index}"`)
- [ ] 3.2 Ingest preview script written (`run_ingest_preview.py` or a `__main__` block) — calls `load_documents()` (from Lesson 2.5) then `chunk_documents()`, and prints the total chunk count plus, for the longest document, how many chunks it produced and their character lengths
- [ ] 3.3 Done-When check #1: preview script run — chunk count is reasonable (roughly 2–4 chunks per seed doc at this size, more for the two PDFs), every printed chunk's metadata includes `source`/`team`/`doc_type`/`chunk_id`, and by eye no chunk's `page_content` cuts off mid-sentence in a way that would lose meaning
- [ ] 3.4 `ingestion/parent_child_demo.py` written — standalone, **not** wired into indexing — `build_parent_child(docs)` (parent splitter `chunk_size=900/overlap=100`, child splitter `chunk_size=180/overlap=20`, `parent_id` linking child → parent) plus a `compare(term, ...)` function and a `__main__` block running it for the term `"steel water bottle"` against `corporate_gifts_price_list.pdf`
- [ ] 3.5 Done-When check #2: `parent_child_demo.py` run for `"steel water bottle"` — output visibly shows the recursive-chunking result (only the matching table row, or close to it) side by side with the parent-child result (the same small, precise child match, *plus* a larger parent chunk that includes the surrounding price-table headers)
- [ ] 3.6 Concept check answered: why chunk size is a tradeoff and not a constant; why metadata must be attached before splitting, not after; what "recursive" actually means in `RecursiveCharacterTextSplitter` (a priority-ordered fallback through separators, not recursion over documents); when parent-child chunking earns its extra storage-layer cost over recursive chunking alone, and what specifically breaks without it (tying back to the price-list comparison)

**Note (added 2026-07-31):** the original roadmap listing for Lesson 3's "What To Build" mentions `loader.py` as one of its outputs — that work is already done, as of Lesson 2.5 (see above), so it does not appear as a Lesson 3 checklist item here. Lesson 3 only needs `chunker.py` and `parent_child_demo.py`, both consuming `load_documents()`'s already-complete output.

*(Two Done-When checks this lesson — 3.3 covers the main loader→chunker→preview path, 3.5 covers the parent-child comparison script. 3.6 is the concept-level verification, same pattern as Lesson 2's and Lesson 2.5's self-checks: Kamran answers, Claude confirms or corrects, and the item is only checked off after that exchange. Also gets an entry in `docs/Interview_QA.md`.)*

---

## Lesson 4 — Embeddings: The Vector Space Mental Model — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 5 — Vector Store & Indexing (the write path) — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 6 — Retrieval & Metadata Filtering (the read path) — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 6.5 — Query Transformation & Hybrid Retrieval Awareness — ⏳ NOT STARTED
*(granular checklist added when this lesson starts. Covers HyDE (implemented), plus Query Expansion and Dense+Sparse/BM25/RRF hybrid search (explained but not implemented) — the "pre-retrieval" half of Advanced RAG; Lesson 10's reranking is the "post-retrieval" half.)*

## Lesson 7 — Prompt Augmentation & Generation — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 8 — Wiring It Together: End-to-End RAG API — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 9 — Retrieval Evaluation — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 10 — Common RAG Pitfalls & Optimization — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 11 — Recap, Comparison, and What's Next — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

---

**Rule for whoever (or whichever AI session) updates this file:** expand a lesson's placeholder into a full granular checklist (matching Lesson 1's density above) only when that lesson is actually started — not in advance. Check a box only after Kamran has explicitly confirmed that item is done. If in doubt, ask before checking. When starting a fresh chat or resuming this course, do a quick heading-count sanity check between this file and `docs/modern-rag-crash-course-roadmap.md` before trusting this file's lesson list is complete — this file is manually maintained and can drift, as it did once already. Also check `docs/Interview_QA.md` for prior assessed-question answers before re-asking a concept check this course has already covered.
