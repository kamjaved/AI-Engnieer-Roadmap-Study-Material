# Python Interview Prep — Progress Tracker

**Companion to:** `roadmap.md` (30 questions)
**Started:** 2026-08-25
**Rule:** A question is only marked ✅ after Kamran explicitly says he is done and the solution
has been reviewed. Never inferred.

---

## Status legend

| Symbol | Meaning |
|---|---|
| ⬜ | Not started |
| 🟡 | In progress / attempted, needs another pass |
| ✅ | Solved and reviewed |
| 🔁 | Marked for revision (got it, but shakily) |

---

## Checklist

### Level 1 — Beginner

| # | Question | Status | Date | Revisit? |
|---|---|---|---|---|
| Q1 | Reverse string + reverse word order | ✅ | 2026-08-25 | |
| Q2 | Character frequency with a plain dict | ✅ | 2026-08-25 | 🔁 missed "ignore case"; redo `get()`/`setdefault()` variants |
| Q3 | Second largest without sorting | ✅ | 2026-08-25 | 🔁 needed a second attempt — first try ignored the constraints |
| Q4 | Remove duplicates preserving order | ✅ | 2026-08-25 | 🔁 Method 1 had an aliasing bug + O(n²) `in`-on-list — fix before reusing this pattern |
| Q5 | Build dict from two lists with `zip()` | ✅ | 2026-08-25 | |
| Q6 | All indices of a target with `enumerate()` | ✅ | 2026-08-25 | 🔁 SRP note — function does two unrelated jobs, revisit when it recurs in Q22 |
| Q7 | Clean/filter messy strings with a comprehension | ⬜ | | |

### Level 2 — Easy

| # | Question | Status | Date | Revisit? |
|---|---|---|---|---|
| Q8 | Word frequency + top N (`Counter`) | ⬜ | | |
| Q9 | Two-sum with a dictionary | ⬜ | | |
| Q10 | Anagram check — two approaches | ⬜ | | |
| Q11 | Set operations across two collections | ⬜ | | |
| Q12 | Sort records by field with `key=lambda` | ⬜ | | |
| Q13 | Flatten a nested list (1 level + arbitrary) | ⬜ | | |
| Q14 | **Debug:** mutating a list while iterating | ⬜ | | |

### Level 3 — Intermediate

| # | Question | Status | Date | Revisit? |
|---|---|---|---|---|
| Q15 | Group items by computed key (`defaultdict`) | ⬜ | | |
| Q16 | Multi-key sort with mixed directions | ⬜ | | |
| Q17 | First non-repeating character | ⬜ | | |
| Q18 | Merge overlapping intervals | ⬜ | | |
| Q19 | Binary search + `bisect` | ⬜ | | |
| Q20 | Split a list into batches of N | ⬜ | | |
| Q21 | Longest substring without repeating chars | ⬜ | | |
| Q22 | Flatten a nested dict into dotted keys | ⬜ | | |
| Q23 | **Debug:** mutable default + shallow/deep copy | ⬜ | | |

### Level 4 — Advanced-Intermediate

| # | Question | Status | Date | Revisit? |
|---|---|---|---|---|
| Q24 | Stream a large JSONL file with a generator | ⬜ | | |
| Q25 | Retry decorator with exponential backoff | ⬜ | | |
| Q26 | Caching layer / memoization + `lru_cache` | ⬜ | | |
| Q27 | Text chunking with overlap (no LangChain) | ⬜ | | |
| Q28 | Cosine similarity + top-K from scratch | ⬜ | | |
| Q29 | Safe JSON extraction + validation | ⬜ | | |
| Q30 | Context manager for timing / token tracking | ⬜ | | |

**Completed:** 6 / 30

---

## Learning notes

One entry per question, added **after** the review step. Keep it short — this file is for
re-reading the night before an interview, not for storing full solutions.

### Template

```
### Qn — <title>          [date]

**My first instinct:** what I reached for before thinking.
**What I got wrong:** the actual bug or missed edge case.
**Key Python thing learned:** the built-in, method or mechanism.
**Complexity:** time / space, and why.
**Better/Pythonic version:** the one-liner or idiom I should have known.
**Interview soundbite:** the one sentence I'd say out loud to explain this.
```

<!-- Add entries below this line, newest at the bottom. -->

### Q1 — Reverse string + reverse word order          [2026-08-25]

**My first instinct:** `text[::-1]` for characters — correct immediately.
For words: `input.split(" ").reverse()`.

**What I got wrong:** `list.reverse()` mutates in place and returns `None`, so the function
returned `None`. Also returned a list where the signature promised `str`.

**Key Python thing learned:** the in-place vs new-object naming convention.
`list.reverse()`, `list.sort()`, `list.append()` mutate and return `None`.
`sorted()`, `reversed()`, slicing all return a new object.
Bigger discovery: `split()` and `split(" ")` are **different algorithms**, not a default value.
`"a    b".split(" ")` → `['a','','','','b']` (empty strings!);
`"a    b".split()` → `['a','b']` and it also strips leading/trailing whitespace and handles
tabs/newlines for free.

**Complexity:** both O(n) time, O(n) space. Strings are immutable, so there is no O(1)-space
reverse in Python. `join()` is O(n) because it pre-computes the total length and allocates once;
`result += word` in a loop would be O(n²).

**Better/Pythonic version:** `" ".join(reversed(sentence.split()))` avoids building a second
list (`reversed` is a lazy iterator, `[::-1]` is a copy). Irrelevant at sentence scale, matters
at 10M elements — same materialise-vs-stream idea as generators in Q24.

**Interview soundbite:** "I used bare `split()` so repeated whitespace collapses, and `join()`
instead of `+=` in a loop to avoid quadratic string building."

---

### Q2 — Character frequency with a plain dict          [2026-08-25]

**My first instinct:** `list(word)` then an `if key in result / else` loop. Logic correct.

**What I got wrong:**
1. **Missed the "ignore case" requirement** — `"Hello"` returned `{'H':1,...}` instead of
   `{'h':1,...}`. Read the spec, not just the example.
2. `list(word)` is redundant — strings are already iterable; `for ch in word` works directly.
3. Skipped the part of the task asking for the `get()` and `setdefault()` variants.
4. Typo in the annotation: `dict['str', int]` (quoted) — Python treats a quoted name as a
   forward reference, so it silently does NOT resolve to `str`. Type checkers flag it; the
   interpreter does not.

**Key Python thing learned:** four ways to write the same counter —
`if/else`, `dict.get(k, 0) + 1`, `setdefault(k, 0)`, `defaultdict(int)` — and `Counter` as the
one-liner. `d[k] += 1` fails on a missing key because `+=` reads before it writes.

**Complexity:** O(n) time, O(k) space where k = distinct characters (bounded, so effectively
O(1) for ASCII). The `if key in result` test is O(1) average because dicts hash.

**Better/Pythonic version:** `Counter(text.lower())`. Note `Counter` **is** a dict subclass —
`dict(...)` around it is only needed if you specifically want to drop the `Counter` behaviour.

**Interview soundbite:** "A dict lookup is O(1) average, which is what turns this from a nested
scan into a single pass — the same move that solves two-sum and group-anagrams."

---

### Q3 — Second largest without sorting          [2026-08-25]

**My first instinct:** `sorted(set(numbers))[-2]`. Correct output, but it violated all three
stated constraints (no sort, no set shortcut, single pass). Needed a second attempt.

**What I got wrong (attempt 1):** didn't read the constraints — solved the example instead of
the spec. See Recurring Mistakes.

**What I got right (attempt 2):** the two hard parts, first try.
1. `num < largest` in the `elif` — without it, `[22, 22, 7]` wrongly returns 22, because the
   duplicate 22 beats 7 and slides into second place.
2. Demote before overwrite: `second = largest` must come **before** `largest = num`, or the old
   champion is lost.

**Still to fix:** returned an f-string sentence instead of the number. A function returns data;
the caller formats it. Third time a stated requirement was dropped.

**Key Python thing learned:**
- **Chained comparison:** `second < num < largest` evaluates `num` once and short-circuits;
  `num < largest and num > second` evaluates it twice. Python does this properly, JS does not.
- **Chained assignment:** `largest = second = float("-inf")` binds both names to one object.
  Safe for immutables, a trap for mutables — `a = b = []` gives two names for the *same* list.
- **In-band vs out-of-band sentinels:** `float("-inf")` means both "unset" and a possible real
  value. Fine for `list[int]`; breaks for floats (`[5, -inf]` wrongly returns None). `None` is
  the out-of-band alternative — costs wordier comparisons (`if largest is None or ...`).
  Same family of bug as returning `-1` for "not found" when `-1` could be real data.

**Complexity:**
- Single pass: **O(n)** time, **O(1)** space — two variables regardless of input size.
- `sorted(set(...))`: **O(n log n)** time, **O(n)** space.
The O(1) space is the real prize, not the time.

**Better/Pythonic version:** in *production* the three-liner `sorted(set(numbers))[-2]` is the
better function — obviously correct, nothing to misread. The single-pass version earns its
keep only when the input is a **stream** (generator, file, socket) that can't be materialised.
Same streaming-vs-materialising idea as `reversed()` in Q1, and the reason `heapq.nlargest`
exists for Q28's top-K.

**Interview soundbite:** "In production I'd write `sorted(set(...))[-2]` — O(n log n) but
obviously correct. If the input were a stream or n were huge, here's the O(n) constant-memory
single-pass version." Showing both beats showing either.

---

### Q4 — Remove duplicates preserving order          [2026-08-25]

**My first instinct:** wrote three versions unprompted — a hand-rolled list-based check, a
set-based `seen` check, and `dict.fromkeys()`. Good range, but the first one hid two separate
bugs behind special-cased short lists.

**What I got wrong:**
1. **Aliasing bug.** In the `len(array)==1` branch: `result = array; return result`. This does
   NOT copy — `result` becomes a second name for the *same* list object. Proved it:
   `out = rmv_duplicate(["a"]); out.append("X")` mutated the caller's original list too. The
   constraint said "return a new list" and this special case silently violated it. The bug was
   invisible because it only triggers on length-1 input, which normal testing glosses over.
   Fix: delete the special case — the general loop already handles length 0 and 1 correctly.
   Never special-case something the general code already covers; the special case is where bugs
   hide.
2. **O(n²) from checking membership against a list.** `if item not in result` where `result` is
   a `list` — Python scans linearly, and the list grows every iteration, so total work is
   1+2+...+n. Benchmarked on 40k items: **2.03s** vs **0.0037s** for the set-based version —
   ~1,500x slower. One word (`list` vs `set`) changed the complexity class with identical logic
   around it.

**Key Python thing learned:**
- **`in` is not one operation** — its cost depends entirely on the container on the right:
  O(n) against a `list`/`tuple`, O(1) average against a `set`/`dict`. Same syntax, different
  algorithm. This is the single most reusable fact from this question.
- **`set` iteration order ≠ insertion order**, and never was guaranteed to be — that's why
  `list(set(items))` reorders. `dict` insertion-order IS a guarantee since 3.7. Same hash-table
  machinery underneath, different contracts.
- **Hashability**: sets/dict-keys require immutable-ish elements. `seen.add({"id": "d1"})` →
  `TypeError: unhashable type: 'dict'`. To dedupe a list of dicts, dedupe by a hashable proxy
  (e.g. `item["id"]`) while still appending the original dict.

**Complexity:**
- List-based `in` check: **O(n²)** worst case, O(n) space.
- Set-based `in` check / `dict.fromkeys()`: **O(n)** average time, O(n) space (unavoidable —
  output size unknown until the pass completes).

**Better/Pythonic version:**
```python
def remove_duplicates(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def remove_duplicates_fast(items: list) -> list:
    return list(dict.fromkeys(items))
```

**Interview soundbite:** "`x in some_list` is O(n); `x in some_set` is O(1) average — same
syntax, different container, different complexity class. That's usually the whole optimization."

---

### Q5 — Build dict from two lists with `zip()`          [2026-08-25]

**My first instinct:** `dict(zip(keys, values, strict=True))` — went straight to the safe
version without being asked, which is the right default once you know `strict` exists.

**What I got wrong:** skipped demonstrating the unsafe baseline. Proved it myself: plain
`zip(keys, short_values)` silently drops `"max_tokens"` with no error, no `None`, nothing —
the key just isn't in the output. That silent-truncation behavior is *why* `strict=True`
matters; reciting "it raises an error" without having seen the failure it prevents is a weaker
answer than showing both.

**Key Python thing learned:**
- `zip()` stops at the **shortest** input, silently. `strict=True` (3.10+) raises `ValueError`
  on either direction of mismatch (too short OR too long), naming which argument was wrong.
- `zip()` is a **one-shot iterator**, same family as `reversed()` (Q1) and generators (Q24).
  `list(z)` twice on the same zip object gives `[]` the second time — no error, just empty.
- Choosing `dict()` vs `list()` around a zip is a semantic choice: key→value mapping vs a
  sequence of paired items. Worth stating which one you mean and why.

**Complexity:** O(n) time and space, n = length of the shorter input (or either, once `strict`
guarantees equal length). `zip()` itself is O(1) per step; the O(n) cost is `dict()` building
the hash table.

**Interview soundbite:** "Zipping a list of IDs with a list of embeddings and having one
silently shorter than the other is a real bug — `strict=True` turns a silently-corrupted
dict into a loud error at the exact line where the mismatch happened."

---

### Q6 — All indices of a target with `enumerate()`          [2026-08-25]

**My first instinct:** one loop, `enumerate(items, start=1)` for a 1-based display listing,
subtracting 1 to recover 0-based indices for the actual answer — computed both outputs in a
single pass. Genuinely good `enumerate()` fluency.

**What I got wrong (round 1):** `return index_of_target, formatted_listing` comma-packs into a
`tuple`, but the signature said `-> dict[int, str]`. Three different things disagreed: returned
a tuple, annotated a dict, task asked for a list. A wrong-but-plausible annotation is worse than
no annotation — a reader would reasonably try `.items()` or `result[0]` expecting a KeyError
guard, and both are wrong for a 2-tuple. Fixed in round 2: `-> tuple[list[int], str]`, verified
against the actual runtime type.

**Design note (not a bug, flagged for later):** the function does two unrelated jobs — finding
indices, and building a formatted listing string — bolted together because the roadmap example
showed them side by side. "The example showed two things" isn't a reason to return two things.
Cost isn't aesthetic: when a future requirement touches one job (e.g. "make it case-insensitive"
or "also return the count"), a split function only needs one function edited; a combined one
needs careful surgery inside a shared loop. Watch for this recurring in Q22 (recursion should
only recurse, not also format).

**Key Python thing learned:** `return a, b` is comma-packing into a tuple — always confirm what
a multi-value return actually produces before trusting the annotation next to it.

**Complexity:** O(n) time, O(n) space — one pass, two lists built alongside it.

**Interview soundbite:** "A function that does two unrelated things is fine until the interviewer
asks for one small change — then you're editing shared state instead of one clean function."

---

## Built-ins & idioms cheat sheet

Grow this list as it comes up. If something here still feels unfamiliar, it's not learned yet.

| Tool | What it's for | First met in |
|---|---|---|
| `s[::-1]` | Reverse any sequence (str, list, tuple) | Q1 |
| `str.split()` | Split on whitespace *runs*, drop empties, strip ends — NOT `split(" ")` | Q1 |
| `str.join(iterable)` | Glue with a separator. Called on the separator. Items must already be `str` | Q1 |
| `reversed(seq)` | Lazy backwards iterator — no copy, one pass only | Q1 |
| `list.reverse()` / `.sort()` | Mutate **in place**, return `None` | Q1 |
| `dict.get(k, default)` | Read with a fallback, never raises | Q2 |
| `dict.setdefault(k, default)` | Read-or-insert in one step; returns the value | Q2 |
| `collections.Counter` | Frequency dict + `.most_common(n)`; a `dict` subclass | Q2 |
| `collections.defaultdict` | Auto-creates missing values via a factory | Q2 |
| `str.lower()` / `.casefold()` | Normalise case; `casefold()` is the aggressive Unicode version | Q2 |
| `float("-inf")` / `float("inf")` | Sentinel that loses every / wins every comparison | Q3 |
| `a < b < c` | Chained comparison — evaluates `b` once, short-circuits | Q3 |
| `a = b = value` | Chained assignment — one object, two names. Never with mutables | Q3 |
| `heapq.nlargest(k, iterable)` | Top-K without sorting everything — O(n log k) | Q3 (preview of Q28) |
| `x in list` vs `x in set/dict` | O(n) linear scan vs O(1) average hash lookup — same syntax | Q4 |
| `list.copy()` / `list(x)` / `x[:]` | Actually copy a list — `new = old` only aliases | Q4 |
| Hashability | Sets/dict-keys need immutable-ish elements; dicts/lists raise `TypeError` | Q4 |
| `zip(a, b, strict=True)` | Raise `ValueError` on length mismatch instead of silent truncation | Q5 |
| `return a, b` | Comma-packing → a `tuple`, not a `dict` or anything else — check before annotating | Q6 |

---

## Recurring mistakes

Anything you get wrong **twice** goes here. This is the highest-value section in the file.

| Mistake | Questions where it bit me | Fix / rule to remember |
|---|---|---|
| **Not reading the spec — solving the example instead of the requirements.** 3 hits in 3 questions. | Q2 (missed "ignore case"), Q3 (ignored all 3 constraints), Q3 v2 (still returned a sentence after being told to return the number) | **Habit:** type the constraints + edge cases as comments at the top of the function before writing a line. Delete them when done. Costs 15 seconds. Examples always under-specify. |
| Returning a formatted sentence instead of data | Q3 | A function returns data; the caller formats. A returned string can't be summed, sorted or compared. |
| Special-casing a short input (`len==1`) instead of trusting the general loop, then bugging the special case | Q4 (aliasing: `result = array` doesn't copy) | Before adding an edge-case branch, check whether the general code already handles it. Fewer branches = fewer places to hide a bug. |
| Checking membership (`in`) against a `list` when a `set` was available | Q4 (O(n²) vs O(n), ~1,500x slower at 40k items) | Ask "what container is on the right of `in`?" every time — it silently sets the complexity class. |
| Return-type annotation not matching what's actually returned | Q1, Q3, Q6 (three times now — a list, a string, a dict, each wrong in a different way) | After writing `return`, check the annotation against the *actual* runtime type before moving on. `return a, b` always packs a tuple. |
| One function doing two unrelated jobs because an example showed them together | Q6 | An example juxtaposing two things is not a spec for one function to do both. Ask: would every caller of A also want B? |
| camelCase names (JS/TS muscle memory) | Q1, Q2 | PEP 8: `snake_case` for functions and variables |
| Naming a variable for what it *becomes*, not what it *is* | Q1 (`words` held a sentence) | Name the parameter for the input |

---

## Decisions made during the course

Record any deviation from the roadmap — questions swapped, extra practice added, topics
deliberately skipped — with the reason.

| Date | Decision | Why |
|---|---|---|
| 2026-08-25 | Roadmap scoped to Python-specific + AI-flavoured practical problems, not general DSA | Target is Python/GenAI coding rounds at 2–3 YOE, where interviewers test built-in fluency and Python traps far more than graph/DP algorithms |
| 2026-08-25 | Two dedicated debugging questions (Q14, Q23) included instead of pure algorithm questions | Snippet/output/debug rounds are standard for experienced Python candidates |
