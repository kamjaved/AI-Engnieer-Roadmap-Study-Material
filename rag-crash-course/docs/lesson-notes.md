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
