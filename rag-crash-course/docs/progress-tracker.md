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

**Note (added 2026-07-31) — Domain pivot:** Kamran requested a full domain swap, replacing the original "DevPortal" knowledge base with a fictional company, **Turab Industries Pvt. Ltd.** (see the updated roadmap). The 1.9 and 1.10 rows above now reflect the *current* state: the original six DevPortal docs (`deploy.md`, `auth.md`, `rate_limits.md`, `on_call.md`, `migrations.md`, `incident_response.md`) have been deleted from `data/docs/` and replaced with the six Turab Industries docs listed in 1.9; `loader.py`'s `DOC_METADATA` was rewritten to match (six markdown entries, plus the two PDF entries — `corporate_gifts_price_list.pdf`, `company_overview.pdf` — already added for real, ahead of Lesson 2.5, since Kamran had both PDFs ready early; only the actual PyPDFLoader dispatch logic that *uses* those two keys is still Lesson 2.5's work). `.env`'s `PINECONE_INDEX_NAME` is confirmed set to `turab-industries` (hyphenated, correct). Lesson 1's original build (against the DevPortal domain) genuinely happened and is preserved as-is in `lesson-notes.md`, with its own supersession note added there rather than rewritten.

---

## Lesson 2 — The RAG Mental Model — 🔄 IN PROGRESS

- [ ] 2.1 Can explain why RAG exists at all — the fine-tuning vs. RAG tradeoff, and that RAG doesn't make the model "smarter," it gives the model's existing reasoning the right facts to work with
- [ ] 2.2 Can explain the six core pipeline concepts in your own words: Document, Chunk, Embedding, Vector index, Retrieval, Augmentation, Generation
- [ ] 2.3 Can explain the core relationship: "retrieval quality caps generation quality" — why a perfect prompt can't rescue chunks that don't contain the answer
- [ ] 2.4 Can explain **Naive RAG**: the straight-line chunk→embed→retrieve→generate pipeline and its known failure modes (vocabulary mismatch, noisy retrieval, no recovery from a bad first attempt)
- [ ] 2.5 Can explain **Advanced RAG**: the two specific upgrade points (pre-retrieval, post-retrieval) and why the pipeline's overall *shape* doesn't change
- [ ] 2.6 Can explain **Agentic RAG**: what extra decision-making it adds (whether/how many times/with what query to retrieve) and why this course deliberately doesn't build it
- [ ] 2.7 Can recognize **Modular RAG** and **GraphRAG** by name and state what each is for, even though neither is built in this course
- [ ] 2.8 Self-check Q1 answered: "if a RAG app confidently answers a question wrong, list the distinct pipeline stages that could be the root cause, and a symptom that isolates each"
- [ ] 2.9 Self-check Q2 answered: "why does Advanced RAG's definition specifically split into pre-retrieval and post-retrieval fixes, rather than just being 'any RAG system with more features bolted on'?"

*(No AI Build Prompt or Done-When check for this lesson — it's conceptual, no code. 2.8/2.9 are this lesson's equivalent verification: Kamran answers each self-check question, Claude confirms or corrects, and the item is only checked off after that exchange, not just after reading the roadmap section.)*

---

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
