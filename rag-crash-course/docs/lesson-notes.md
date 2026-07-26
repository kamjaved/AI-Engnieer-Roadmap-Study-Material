# Lesson Notes & Decision Log — Modern RAG Crash Course

> Retrospective notes, written at the end of each lesson: what we learned, what we decided and why, what broke and how it got fixed, and the exact commands used. Meant to stand on its own — if Kamran picks this project back up weeks later, or this is a new Claude session, start here before re-reading the full roadmap.

---

## Instructions for the AI (read this before writing anything here)

This file is intentionally empty of lesson content right now — nothing has started. Your job is to fill it in **one lesson at a time, retrospectively**, following the exact process and structure below. Do not pre-write notes for a lesson that hasn't happened yet, and do not summarize from the roadmap document alone — these notes are a record of what *actually* happened in *this* project's build, including the messy parts, not a restatement of the lesson plan.

### When to write a new lesson's entry
- Only after that lesson's Done-When check has been run and Kamran has explicitly confirmed it passed — check `progress-tracker.md` first; if the corresponding boxes there aren't checked yet, the lesson isn't done and doesn't get an entry here.
- One entry per lesson, appended in lesson order, using `## Lesson N — <Title>` as the heading (copy the exact title from the roadmap / progress tracker).
- Never retroactively edit a prior lesson's entry to "clean it up" once written — if something from an earlier lesson turns out to be wrong or incomplete, add a note under the *current* lesson pointing back to it, the same way Lesson 3's checkpoint-granularity discussion referenced back to Lesson 2. The log is a history, not a living summary.

### Structure every lesson entry must follow
Use exactly these five subheadings, in this order, every time — consistency here is what makes the file skimmable months later:

```markdown
## Lesson N — <Title>

### Key concepts learned
### Important decisions & why
### Bugs hit and fixes
### Commands used
### Self-check / confirmation results

---
```

**Key concepts learned** — bullet list, one concept per bullet, **bold the term**, then a plain-language explanation of what it actually is and why it matters — not a dictionary definition, the understanding as it actually landed for Kamran in this conversation. If an analogy was what made something click (e.g. a mental-model comparison), keep the analogy in the note verbatim — it's more useful to future-Kamran than a more "formal" rephrasing would be.

**Important decisions & why** — bullet list, one decision per bullet: **what was chosen**, in bold, followed by the reasoning and — where relevant — what the tradeoff or alternative was and why it lost. Only decisions with an actual "why," not restatements of the roadmap's defaults taken without discussion. If a decision was revisited or reversed in a later lesson, that update belongs in the later lesson's entry, not edited in here.

**Bugs hit and fixes** — numbered list. For each: the exact error message or symptom, the root cause (not just the fix — the *why* it happened), and the fix, with a code snippet if the fix was code. If a lesson had zero bugs, write that explicitly ("None this lesson — ...") rather than omitting the section, the way Lesson 3 did in the reference course. Flag anything likely to resurface in a later lesson.

**Commands used** — fenced code block, the actual commands run in this project, in the order they were run. Not a generic "here's how you'd do this" — the literal history, including OS-specific flags or workarounds if any came up.

**Self-check / confirmation results** — tie back explicitly to that lesson's Done-When check(s) and any "Concepts You Must Be Able to Explain" self-check from the roadmap. State what was asked, what Kamran answered, whether it was right on the first attempt or needed correction, and what the correction was if so. This is the section that most directly proves the lesson's objective was actually met, not just that code ran.

### Tone and level of detail
Match the density and directness of a senior engineer's own build log, not a tutorial recap — short, specific, technical, no motivational language, no restating things that are already fully explained in the roadmap document itself. Assume the reader already has the roadmap open in another tab; this file's job is to capture what the roadmap couldn't have known in advance: the specific bugs, the specific decisions made under this project's actual constraints, and the specific gaps in understanding that came up and got closed.

---

## Lesson 1 — Prerequisites & Lean Project Setup

### Key concepts learned
- **pydantic-settings as fail-fast config**: instead of `os.getenv()` calls scattered through the codebase (which fail silently, deep in some unrelated code path, when a var is missing or typo'd), `pydantic-settings` validates all required env vars into one typed class at import time. Missing a required field raises a `ValidationError` immediately, at startup — the failure happens at the door, not three calls deep.
- **`.env` is dev-only, not a production mechanism**: `SettingsConfigDict(env_file=".env")` is a local-dev convenience. In production, the platform (containers, k8s, cloud secrets manager) injects real env vars directly into the process — `pydantic-settings` reads `os.environ` either way, so the `.env` file is a fallback, not the primary mechanism.
- **`.gitignore` has to exist *before* `git init`/first commit, not just before pushing**: gitignore only stops *future* tracking. It has zero effect on a file already staged or committed — if `.env` (with live API keys) gets committed once before `.gitignore` exists, adding the ignore rule afterward doesn't untrack it; you'd have to purge it from history separately. This project's `.gitignore` was created before `git init` happened, avoiding the problem entirely.
- **`uv run` vs. bare `python`**: a bare `python -c "..."` invocation hits the global system interpreter, which has no idea this project or its `rag` package exists. `uv run` activates the project's own virtual environment *and* installs/syncs the local `src/`-layout package into it (editable install) before running anything — that's what "Installed 1 package" in the terminal output was doing. Bare `python` will reliably produce `ModuleNotFoundError` for any local package in a uv project.
- **Centralized metadata lookup (`DOC_METADATA`)**: a single `dict[str, dict[str, str]]` mapping filename → `{team, doc_type}`, kept separate from the (not-yet-written) loading logic. Adding a 7th doc later is a one-line addition to this dict, not a new branch inside file-loading code — and it's the first place to check if a chunk's metadata looks wrong at retrieval time in a later lesson.

### Important decisions & why
- **Confirmed 1.1–1.6 as already complete from disk evidence, rather than redoing them** — `uv init`, all core + dev dependencies, the full folder skeleton, and a populated `.env` were all already present on disk when this session started, from work done before this chat. Verified by inspecting the project folder directly, then explicitly confirmed by Kamran rather than inferred from the files existing — per the standing rule that nothing gets checked off without his explicit say-so.
- **Kept `OPENAI_API_KEY` / `PINECONE_API_KEY` as plain `str` in `Settings`, not `pydantic.SecretStr`** — `SecretStr` is the more secure choice (masks the value in logs/tracebacks/`repr()`), but the roadmap's later lessons (e.g. Lesson 5's `Pinecone(api_key=settings.PINECONE_API_KEY)`) expect a plain string. Switching now would mean unwrapping with `.get_secret_value()` at every downstream call site, diverging from the roadmap's prescribed code for no lesson-relevant benefit. Flagged as a real production practice to adopt in a non-learning codebase, not implemented here.
- **`DOC_METADATA` implemented as a hardcoded Python dict, not YAML frontmatter or a database-backed registry** — right-sized for a six-document, single-maintainer corpus where the dict is reviewed like any other code change. The frontmatter/database approach is the correct move once a second team or non-engineer starts contributing docs, since metadata should then live with the content, not in code only the engineer touches.

### Bugs hit and fixes
1. **Symptom**: `ModuleNotFoundError: No module named 'rag'` when running the Lesson 1 Done-When check.
   **Root cause**: the check was first run as a bare `python -c "from rag.config import settings; ..."`, which executes against the global/system Python interpreter — not the project's uv-managed virtual environment where the local `rag` package actually gets installed (editable install, `src/`-layout).
   **Fix**: re-ran the identical check prefixed with `uv run` (`uv run python -c "..."`), which activates the project venv and syncs/installs the local package first. Confirmed working — printed `devportal-kb` with no errors, both after 1.8 (`config.py` written) and again after 1.10 (`loader.py` changed, triggering an uninstall/reinstall of the local package).

### Commands used
```bash
# Run in a prior session before this chat (confirmed done, not re-run live):
uv init rag-crash-course --python 3.13
uv add langchain langchain-openai langchain-pinecone langchain-text-splitters pinecone pydantic-settings python-dotenv
uv add --dev ruff

# Run live during this lesson (first attempt failed, second succeeded):
python -c "from rag.config import settings; print(settings.PINECONE_INDEX_NAME)"   # ModuleNotFoundError: No module named 'rag'
uv run python -c "from rag.config import settings; print(settings.PINECONE_INDEX_NAME)"   # -> devportal-kb
```

### Self-check / confirmation results
- **Done-When check (1.11)**: `uv run python -c "from rag.config import settings; print(settings.PINECONE_INDEX_NAME)"` ran with no import errors and printed `devportal-kb` — confirmed via terminal screenshot, observed twice (post-1.8 and post-1.10).
- **Six seed docs present (1.9/1.11)**: all six files (`deploy.md`, `auth.md`, `rate_limits.md`, `on_call.md`, `migrations.md`, `incident_response.md`) confirmed present under `data/docs/` with real content — explicitly confirmed by Kamran ("Yes all saved").
- No separate "concepts" quiz this lesson — Lesson 1 is pure setup, so the understanding checks were folded into each item's inline explanation (pydantic-settings fail-fast validation, gitignore-before-git-init ordering, `uv run` vs. bare `python`, `DOC_METADATA` centralization) rather than a standalone Q&A at the end.

---
