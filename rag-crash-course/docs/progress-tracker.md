# Progress Tracker — Modern RAG Crash Course

> Source of truth for what's actually done vs. pending. A box is checked **only** after Kamran has explicitly confirmed it — never inferred from context. If you're a fresh Claude session picking this up: trust this file over anything implied elsewhere, and don't mark anything complete without asking first.

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

**Note (added 2026-07-31) — Domain pivot:** Kamran requested a full domain swap, replacing the original "DevPortal" knowledge base with a fictional company, **Turab Industries Pvt. Ltd.** (see the updated roadmap). The 1.9 and 1.10 rows above now reflect the *current* state: the original six DevPortal docs (`deploy.md`, `auth.md`, `rate_limits.md`, `on_call.md`, `migrations.md`, `incident_response.md`) have been deleted from `data/docs/` and replaced with the six Turab Industries docs listed in 1.9; `loader.py`'s `DOC_METADATA` was rewritten to match (six markdown entries now; two PDF entries — `corporate_gifts_price_list.pdf`, `company_overview.pdf` — are commented-in as a preview, to be added for real in Lesson 2.5, not before). `.env`'s `PINECONE_INDEX_NAME` should read `turab-industries` (not `devportal-kb`, and not `turab_industries` — Pinecone index names can't contain underscores) — update this yourself if you haven't yet. Lesson 1's original build (against the DevPortal domain) genuinely happened and is preserved as-is in `lesson-notes.md`, with its own supersession note added there rather than rewritten.

---

## Lesson 2 — The RAG Mental Model — ⏳ NOT STARTED
*(conceptual lesson — granular checklist added when this lesson starts)*

## Lesson 3 — Documents → Chunks — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 4 — Embeddings: The Vector Space Mental Model — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 5 — Vector Store & Indexing — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

## Lesson 6 — Retrieval & Metadata Filtering — ⏳ NOT STARTED
*(granular checklist added when this lesson starts)*

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

**Rule for whoever (or whichever AI session) updates this file:** expand a lesson's placeholder into a full granular checklist (matching Lesson 1's density above) only when that lesson is actually started — not in advance. Check a box only after Kamran has explicitly confirmed that item is done. If in doubt, ask before checking.
