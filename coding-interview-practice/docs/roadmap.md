# Python Interview Preparation Roadmap — 30 Questions

**Target profile:** Python developer / AI–GenAI engineer, ~2–3 years of practical Python experience
**Goal:** Pass coding rounds, live-coding screens, snippet/debug rounds and "practical Python" challenges
**Created:** 2026-08-25 · **Updated:** 2026-08-26 (added starter skeletons + per-question sources, loosened constraints)
**Rule:** No solutions in this file. Solve first, review after.

**How to read the constraints below:** where a question says "avoid X" or "without Y," that
restriction exists to force practice of a specific mechanism — it is the point of the exercise,
not a rule I'm grading you against. Solve it however makes sense to you; if you take a different
route than the one described, that's a legitimate answer and we'll compare trade-offs in review,
not treat it as wrong. The one thing I will push back on is skipping the constraint *silently* —
say out loud (or in a comment) if you deliberately went a different way and why.

**Starter skeletons:** every question below has a fixed function name and signature so you don't
burn time deciding names or argument order. Everything inside the function — helper functions,
loop structure, which built-ins you reach for — is entirely yours. Treat the skeleton as the
interface an interviewer would hand you on a shared doc, not as a specification of the algorithm.

**Sources:** every question has a `Source:` line. Where I found a specific, documented company
attribution (a real interview report, a company-tagged problem list), it's named explicitly with
a link. Where a pattern is common across many general "Python interview questions" lists but I
could not verify a specific company asked *this exact* framing, I say so plainly instead of
inventing one — treat those as "commonly recommended practice," not "confirmed asked at X."

---

## How this roadmap was built (research notes)

This is not a list generated from assumption. It was assembled after reviewing what is
actually being asked right now:

- **General Python coding rounds (2–3 YOE):** interview banks from InterviewBit, DataCamp,
  CodingInterview.com, PythonGuides and DataInterview consistently repeat the same core set —
  frequency counting with dicts/`Counter`, first non-repeating character, group anagrams,
  top-K frequent, two-sum with a hash map, dedup preserving order, flatten nested lists,
  merge dictionaries, custom sorting with `key=lambda`, and `zip()`/`enumerate()` usage.
- **Python "trap" / snippet rounds:** mutable default arguments, `is` vs `==`, shallow vs deep
  copy, generators vs lists, decorators, and mutation-during-iteration show up in almost every
  experienced-candidate list. These are debugging questions, not algorithm questions.
- **AI / GenAI engineer loops specifically:** published interview playbooks and question banks
  (dev.to AI Engineer Interview Playbook, GenAI question banks, GitHub AI-engineer interview
  repos) list the same "AI-flavoured warm-ups": implement cosine similarity from scratch,
  implement text chunking with overlap without LangChain, token counting, batching, retry with
  exponential backoff, structured/JSON output validation, streaming, and caching. These are
  ordinary Python problems wearing an AI costume — which is exactly why they belong here.
- **Company attribution pass (2026-08-26 update):** a second research pass specifically hunted
  for verified company tags — real onsite/OA reports, company-tagged problem databases (Hello
  Interview, 1Point3Acres, jointaro, igotanoffer's Glassdoor-sourced Amazon list), and named
  interview playbooks (Amazon GenAI, Anthropic AI engineering). Where a question in this roadmap
  matches one of those verified reports closely, the company is named in that question's
  `Source:` line. Most Level 1–2 questions are foundational patterns that appear everywhere and
  are not tied to one company's leaked interview — that's stated honestly rather than guessed.

The 30 questions below are ordered so each one reuses something you built in an earlier one.

**General sources:** [InterviewBit](https://www.interviewbit.com/python-interview-questions/) ·
[DataCamp](https://www.datacamp.com/blog/top-python-interview-questions-and-answers) ·
[CodingInterview.com](https://www.codinginterview.com/guide/python-coding-interview-questions-and-answers/) ·
[DataInterview – Top 100 Python Questions](https://www.datainterview.com/blog/top-100-python-interview-questions) ·
[Generalist Programmer – 20 Worked Examples](https://generalistprogrammer.com/tutorials/python-interview-questions) ·
[The AI Engineer Interview Playbook (dev.to)](https://dev.to/truongpx396/the-ai-engineer-interview-playbook-45pb) ·
[GenAI Engineer Interview Questions 2026](https://cloudsoftsol.com/blog/genai-engineer-interview-questions-2026/) ·
[Let's Data Science – 50 AI Engineer Questions](https://letsdatascience.com/blog/50-llm-and-ai-engineer-interview-questions-for-2026) ·
[AI-Engineer-Interview-Questions (GitHub)](https://github.com/ombharatiya/AI-Engineer-Interview-Questions) ·
[Hello Interview – Two Sum](https://www.hellointerview.com/community/questions/leetcode-two-sum/cm5eh7nrh04n1838os7sfzdx9) ·
[igotanoffer – 49 confirmed Amazon coding interview questions](https://igotanoffer.com/blogs/tech/amazon-coding-interview-questions) ·
[fastprep.io – Group Anagrams (Amazon onsite)](https://www.fastprep.io/problems/amazon-group-anagrams) ·
[openagenthub.io – Coding Rounds by company](https://openagenthub.io/interview/coding-rounds/) ·
[velocode.ai – Anthropic retry/backoff question](https://velocode.ai/practice/resilient-llm-api-calls-with-exponential-backoff-retry-logic)

---

## Difficulty map

| Level | Questions | Theme |
|---|---|---|
| **Beginner** | Q1 – Q7 | Strings, lists, dicts, `zip`, `enumerate`, comprehensions |
| **Easy** | Q8 – Q14 | `Counter`, sets, hash-map patterns, sorting with `key`, first debug question |
| **Intermediate** | Q15 – Q23 | Grouping, multi-key sort, sliding window, recursion, intervals, search, the classic Python traps |
| **Advanced-Intermediate** | Q24 – Q30 | Generators, decorators, caching, and the AI/GenAI-flavoured practical problems |

Work top to bottom. Do not skip the Beginner block — the interviewer's first question is
usually one of those, and fumbling it sets the tone for the whole round.

---

# LEVEL 1 — BEGINNER (Q1 – Q7)

Foundation block. These must become muscle memory: you should be able to write them
while talking, without pausing to think about syntax.

---

## Q1. Reverse a string, then reverse the word order of a sentence

**Difficulty:** Beginner

**Problem statement**
Write two small functions. The first reverses the characters of a string. The second reverses
the *order of words* in a sentence, keeping each word itself intact. Do not use any external
library.

**Example**
```
Input:  "genai"
Output: "ianeg"

Input:  "I build production AI systems"
Output: "systems AI production build I"
```

**Expected task**
Implement both. Then answer out loud: what happens with multiple spaces between words
(`"a    b"`), and with leading/trailing whitespace?

**Starter skeleton**
```python
def reverse_string(text: str) -> str:
    """Reverse the characters of a string."""
    ...


def reverse_word_order(sentence: str) -> str:
    """Reverse the order of words in a sentence."""
    ...
```

**Concept / pattern tested**
String slicing with a negative step, `str.split()`, `str.join()`, immutability of strings.

**Why it's asked**
This is the most common opening warm-up in Python screens. Interviewers use it to check
whether you reach for `[::-1]` and `split()/join()` naturally, or start writing a manual
index loop like a C programmer. In AI work you touch text constantly — clean string handling
is the base layer under every prompt builder, parser and chunker.

**Source:** General warm-up pattern appearing across nearly every "Python interview questions,
2–3 years experience" list reviewed — [InterviewBit](https://www.interviewbit.com/python-interview-questions/),
[DataCamp](https://www.datacamp.com/blog/top-python-interview-questions-and-answers). Not tied
to one specific company's leaked interview in the sources found — treat as a universal warm-up
rather than a company-confirmed question.

---

## Q2. Count character frequency using a plain dictionary

**Difficulty:** Beginner

**Problem statement**
Given a string, return a dictionary mapping each character to the number of times it appears.
Ignore case. Try it first **without** `collections.Counter` — write the counting loop by hand;
that's the actual point of this one.

**Example**
```
Input:  "Hello"
Output: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

**Expected task**
Solve it with `dict.get()` and then again with `dict.setdefault()`. Explain the difference
between the two, and why `dict[key] += 1` fails on a missing key.

**Starter skeleton**
```python
def char_frequency(text: str) -> dict[str, int]:
    """Count characters case-insensitively, without Counter."""
    ...


def char_frequency_stdlib(text: str) -> dict[str, int]:
    """Same result using collections.Counter."""
    ...
```

**Concept / pattern tested**
Dictionary as a counter, `get()` vs `setdefault()` vs `KeyError`, O(1) average hash lookup.

**Why it's asked**
Frequency counting is the single most reused pattern in Python interviews — anagrams,
first-unique-character, top-K, word counts and duplicate detection are all this loop in
disguise. Interviewers deliberately ban `Counter` first, then ask you to redo it with `Counter`,
to see if you understand what the library is doing for you.

**Source:** General pattern — "count frequency of elements" appears as a named item across
[DataInterview's Top 100](https://www.datainterview.com/blog/top-100-python-interview-questions)
and [InterviewBit](https://www.interviewbit.com/python-interview-questions/). Not company-tagged
in the sources reviewed.

---

## Q3. Find the second largest number in a list without sorting

**Difficulty:** Beginner

**Problem statement**
Given a list of integers, return the second largest **distinct** value. The interesting version
of this exercise avoids `sorted()`, `list.sort()`, and converting to a set — a single pass with
two running variables is the mechanism being practiced. If you reach for `sorted(set(...))`
first, that's a legitimate production answer (see Q3's review notes on when each is right) —
just also do the single-pass version, since that's what a live round will actually ask for.

**Example**
The function returns the **number itself**, not a formatted sentence.

```
Input:  [10, 5, 22, 22, 7]   ->  10      # 22 is largest, so the answer is 10
Input:  [4, 4, 4]            ->  None    # no second distinct value
Input:  [3, 1]               ->  1
Input:  [-5, -2, -9]         ->  -5      # -2 is largest, -5 is second
```

**Expected task**
Handle these edge cases explicitly: empty list, single element, all elements equal,
negative numbers.

**Starter skeleton**
```python
def find_second_largest(numbers: list[int]) -> int | None:
    """Return the second largest distinct value, or None if there isn't one."""
    ...
```

**Concept / pattern tested**
Single-pass scanning, tracking two running values, edge-case discipline, why
`float('-inf')` is a safer initial value than `0`.

**Why it's asked**
It is the classic "can you think without reaching for a built-in" question. Most candidates
sort in O(n log n); the interviewer wants the O(n) single pass. The real signal is whether you
volunteer the edge cases before being asked — that is what separates 2–3 years of experience
from a fresher.

**Source:** General pattern, widely recommended across Python/DSA prep sites as a "no built-in
shortcut" warm-up. No specific company attribution found in the sources reviewed for this exact
framing.

---

## Q4. Remove duplicates from a list while preserving original order

**Difficulty:** Beginner

**Problem statement**
Given a list that may contain duplicates, return a new list with duplicates removed, keeping
the order of first appearance.

**Example**
```
Input:  ["doc3", "doc1", "doc3", "doc2", "doc1"]
Output: ["doc3", "doc1", "doc2"]
```

**Expected task**
Write it with an explicit `seen` set first. Then write the idiomatic one-liner using
`dict.fromkeys()`. Explain why `list(set(items))` is the wrong answer here.

**Starter skeleton**
```python
def remove_duplicates(items: list) -> list:
    """Remove duplicates, preserving first-seen order. Does not mutate the input."""
    ...


def remove_duplicates_fast(items: list) -> list:
    """Same result, idiomatic one-liner."""
    ...
```

**Concept / pattern tested**
Set membership as O(1) lookup, insertion-ordered dicts (Python 3.7+), the order-vs-speed
trade-off.

**Why it's asked**
Interviewers love this one because the naive answer (`list(set(...))`) is *almost* right and
silently destroys ordering. In a RAG pipeline you dedupe retrieved chunk IDs constantly, and
order there is relevance order — losing it is a real production bug, not a trivia point.

**Source:** Listed directly as item #1 in [DataInterview's Top 100 Python Interview
Questions](https://www.datainterview.com/blog/top-100-python-interview-questions) ("How do you
remove duplicates from a list while maintaining order?"). Not tied to a specific company report
in the sources reviewed.

---

## Q5. Build a dictionary from two lists using `zip()`

**Difficulty:** Beginner

**Problem statement**
Given a list of keys and a list of values, build a dictionary pairing them up.
Then extend it: what should happen when the two lists have different lengths?

**Example**
```
keys   = ["model", "temperature", "max_tokens"]
values = ["gpt-4o", 0.2, 512]

Output: {"model": "gpt-4o", "temperature": 0.2, "max_tokens": 512}
```

**Expected task**
Implement with `dict(zip(...))`. Then demonstrate what `zip()` does on unequal lengths, and
show how `zip(..., strict=True)` (Python 3.10+) turns a silent truncation into a loud error.

**Starter skeleton**
```python
def combine_key_value(keys: list, values: list) -> dict:
    """Pair keys with values positionally. Decide how to handle a length mismatch."""
    ...
```

**Concept / pattern tested**
`zip()` semantics, lazy iterators, `dict()` construction from pairs, fail-fast design.

**Why it's asked**
`zip()` is a top-5 "do you actually write Python" tell. The `strict=True` follow-up is the
modern part most candidates miss — silent truncation of mismatched data is exactly the kind of
bug that corrupts an embedding batch where vectors and IDs get out of alignment.

**Source:** General pattern — `dict(zip(keys, values))` is used as the canonical example in
[PythonGuides' 200+ Python Interview Questions](https://pythonguides.com/python-interview-questions-and-answers/)
(#44). `zip(..., strict=True)` is a Python 3.10+ language feature, documented in the
[official Python docs](https://docs.python.org/3/library/functions.html#zip); no company
attribution found for this specific framing.

---

## Q6. Use `enumerate()` to find every index of a target value

**Difficulty:** Beginner

**Problem statement**
Given a list and a target value, return a list of **all** indices where the target appears.
Then produce a human-readable numbered listing starting at 1. These are two separate outputs —
you decide whether that means two separate functions or one function returning both; there's a
real design opinion buried in that choice (see the Q6 review notes on single responsibility).

**Example**
```
Input:  ["a", "b", "a", "c", "a"], target = "a"
Output: [0, 2, 4]

Numbered listing:
1. a
2. b
3. a
4. c
5. a
```

**Expected task**
Solve with `enumerate()` inside a list comprehension. Use the `start=` parameter for the
numbered listing. Explain why `for i in range(len(items))` is considered unidiomatic.

**Starter skeleton**
```python
def find_all_indices(items: list, target) -> list[int]:
    """Return every index where items[i] == target."""
    ...


def numbered_listing(items: list, start: int = 1) -> str:
    """Format items as a 1-indexed, newline-joined listing."""
    ...
```

**Concept / pattern tested**
`enumerate()` including its `start` argument, comprehension with a condition, index-vs-value
iteration.

**Why it's asked**
`list.index()` only returns the first match — interviewers use this to see if you notice that.
`enumerate` also appears in nearly every real loop you'll write over chunks, messages or
retrieved documents where you need both the position and the item.

**Source:** `enumerate()` and its `start` parameter are covered as a named topic across general
Python interview lists (e.g. [DataInterview](https://www.datainterview.com/blog/top-100-python-interview-questions),
item #2: "What is the purpose of the `enumerate()` function?"). Not tied to a specific company
report.

---

## Q7. Clean and filter a messy list of strings with a comprehension

**Difficulty:** Beginner

**Problem statement**
You receive a list of raw user-supplied tags. Produce a cleaned list: strip whitespace,
lowercase everything, drop empty/whitespace-only entries, and drop anything shorter than
2 characters.

**Example**
```
Input:  ["  RAG ", "", "LangGraph", "   ", "a", "Vector DB  "]
Output: ["rag", "langgraph", "vector db"]
```

**Expected task**
Write it as a single list comprehension. Then write the same thing as an explicit `for` loop
and say which version you would put in a production codebase and why.

**Starter skeleton**
```python
def clean_tags(tags: list[str]) -> list[str]:
    """Strip, lowercase, and drop empty or too-short tags. Single comprehension."""
    ...


def clean_tags_loop(tags: list[str]) -> list[str]:
    """Same logic as an explicit for loop."""
    ...
```

**Concept / pattern tested**
List comprehension with transform + filter, order of operations inside a comprehension,
readability limits of comprehensions.

**Why it's asked**
Comprehensions are the number-one thing interviewers scan for. But the real question underneath
is judgement: a candidate who crams four transformations into one unreadable comprehension is
showing off, not engineering. Say the trade-off out loud.

**Source:** General pattern. Comprehension fluency is called out explicitly as the top thing
interviewers scan for in [Generalist Programmer's worked-examples
guide](https://generalistprogrammer.com/tutorials/python-interview-questions). Not tied to a
specific company report.

---

# LEVEL 2 — EASY (Q8 – Q14)

Now you start combining the Level 1 building blocks and meeting the standard library.

---

## Q8. Word frequency and the top N most common words

**Difficulty:** Easy

**Problem statement**
Given a paragraph of text, return the N most frequent words with their counts, sorted by count
descending. Normalise case and strip basic punctuation.

**Example**
```
Input:  "The cat sat. The cat ran! the DOG sat.", n = 2
Output: [("the", 3), ("cat", 2)]
```

**Expected task**
Solve it twice: once with a plain dict (reusing your Q2 pattern), once with
`collections.Counter` and `most_common(n)`. Then handle the tie-break question: if two words
have the same count, what order do they come out in, and how would you force alphabetical order
on ties?

**Starter skeleton**
```python
def top_n_words(text: str, n: int) -> list[tuple[str, int]]:
    """Return the n most frequent words as (word, count) pairs, descending by count."""
    ...
```

**Concept / pattern tested**
`Counter`, `most_common()`, text normalisation, tie-breaking in sorts.

**Why it's asked**
This is the most-repeated "practical Python" question across every interview bank. For AI roles
it doubles as a stand-in for token/term statistics — the same shape as counting tokens, building
a BM25 term index, or profiling a corpus before chunking it.

**Source:** General pattern, related closely to LeetCode's numeric "Top K Frequent Elements,"
which [InterviewBit](https://www.interviewbit.com/python-interview-questions/) presents as item
#7 with a `Counter.most_common(k)` solution. This word-frequency variant is the text-flavored
twin of that same idea; no company tag found for the word-frequency framing specifically.

---

## Q9. Two-sum using a dictionary

**Difficulty:** Easy

**Problem statement**
Given a list of integers and a target, return the indices of the two numbers that add up to
the target. Assume exactly one valid answer.

**Example**
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

**Expected task**
Write the brute-force O(n²) version, state its complexity out loud, then rewrite it as a single
pass using a dictionary of `value -> index`. Explain what the dictionary is actually storing.

**Starter skeleton**
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """Return the indices of two numbers that add up to target."""
    ...
```

**Concept / pattern tested**
The complement / hash-map lookup pattern, trading space for time, O(n²) → O(n).

**Why it's asked**
It is the canonical demonstration that a dict turns a nested loop into a single pass. Almost
every "optimise this" follow-up in a Python round is a variation of this same move, so
interviewers use it as a baseline check. Narrating the brute force *and then* improving it is
half the grade.

**Source:** This is LeetCode #1, one of the most extensively company-documented questions that
exists. Confirmed asked at **Google, Amazon, Microsoft, and Meta**
([YouTube walkthrough citing all four](https://www.youtube.com/watch?v=wU6xQSRoobg)), plus
recent 2026 reports at **Brex, JPMorgan Chase, and ServiceNow**
([Hello Interview's tracked question timeline](https://www.hellointerview.com/community/questions/leetcode-two-sum/cm5eh7nrh04n1838os7sfzdx9)).
igotanoffer's dataset of 250+ real Glassdoor Amazon interview reports also lists it as
[confirmed Amazon question #1](https://igotanoffer.com/blogs/tech/amazon-coding-interview-questions).
A Reddit thread from r/leetcode independently corroborates it as a common FAANG warm-up with
follow-ups into 3Sum/4Sum.

---

## Q10. Anagram check — two valid approaches with different trade-offs

**Difficulty:** Easy

**Problem statement**
Given two strings, determine whether they are anagrams of each other (same characters, same
counts, ignoring case and spaces).

**Example**
```
Input:  "Listen", "Silent"   -> True
Input:  "hello",  "world"    -> False
```

**Expected task**
Implement it with sorting, and again with frequency counting. Then compare: time complexity,
space complexity, and which you would choose for very long strings versus a huge number of
short strings.

**Starter skeleton**
```python
def is_anagram_sorted(a: str, b: str) -> bool:
    """Anagram check via sorting."""
    ...


def is_anagram_counting(a: str, b: str) -> bool:
    """Anagram check via frequency counting."""
    ...
```

**Concept / pattern tested**
`sorted()` on strings, `Counter` equality, O(n log n) vs O(n) reasoning.

**Why it's asked**
The point of this question is not the answer — it's the comparison. Interviewers ask it to hear
you weigh two correct solutions, which is exactly the "discuss trade-offs" signal they are
grading experienced candidates on.

**Source:** The pairwise anagram check is the simpler building block behind LeetCode's "Group
Anagrams," which is independently confirmed asked at **Amazon, Google, Facebook (Meta), and
Microsoft** — see Q15's sources below for the direct company evidence. No separate company
attribution found for the standalone pairwise-check framing used here.

---

## Q11. Set operations across two collections

**Difficulty:** Easy

**Problem statement**
Given two lists, return: (a) items present in both, (b) items only in the first, (c) items in
exactly one of the two. Preserve nothing about order — but then answer the follow-up: how would
you preserve the order of the first list in the result?

**Example**
```
a = ["doc1", "doc2", "doc3", "doc4"]
b = ["doc3", "doc4", "doc5"]

common     -> {"doc3", "doc4"}
only_in_a  -> {"doc1", "doc2"}
symmetric  -> {"doc1", "doc2", "doc5"}
```

**Expected task**
Use `&`, `-`, `^` (and their method equivalents `intersection`, `difference`,
`symmetric_difference`). Then explain why a list of dictionaries cannot go into a set directly.

**Starter skeleton**
```python
def compare_collections(a: list, b: list) -> dict[str, set]:
    """Return {'common': ..., 'only_in_a': ..., 'symmetric_diff': ...}."""
    ...
```

**Concept / pattern tested**
Set algebra, hashability, why sets are unordered, converting back to an ordered list.

**Why it's asked**
Set operations are the fastest correct answer to a whole family of "compare two collections"
questions, and candidates who loop manually instead stand out badly. The hashability follow-up
(`unhashable type: 'dict'`) is a very common live-coding stumble.

**Source:** General pattern. Set algebra operators (`&`, `-`, `^`) are documented Python
language features covered across general interview prep content; no specific company
attribution found for this exact framing.

---

## Q12. Sort a list of records by a field using `key=lambda`

**Difficulty:** Easy

**Problem statement**
Given a list of dictionaries representing retrieved documents, sort them by their `score`
in descending order.

**Example**
```
docs = [
    {"id": "d1", "score": 0.72},
    {"id": "d2", "score": 0.91},
    {"id": "d3", "score": 0.65},
]
Output order: d2, d1, d3
```

**Expected task**
Use `sorted()` with `key=` and `reverse=True`. Then rewrite the key using
`operator.itemgetter`. State the difference between `sorted()` and `list.sort()`, and what each
one returns.

**Starter skeleton**
```python
def sort_by_score(docs: list[dict], descending: bool = True) -> list[dict]:
    """Sort documents by their 'score' field. Returns a new list."""
    ...
```

**Concept / pattern tested**
`key=` functions, `lambda`, `reverse=`, `operator.itemgetter`, in-place vs new list.

**Why it's asked**
Custom sorting is asked in some form in nearly every Python round. The `sorted()` vs `.sort()`
return-value gotcha (`.sort()` returns `None`) catches a surprising number of experienced
candidates. Ranking retrieved chunks by score is also the single most common sort you'll write
in a RAG system.

**Source:** General pattern, covered extensively in
[freeCodeCamp's "Lambda Sorted in Python"](https://www.freecodecamp.org/news/lambda-sort-list-in-python)
and this heavily-upvoted
[Stack Overflow thread on sorting with lambda](https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python).
Not tied to a specific company report.

---

## Q13. Flatten a nested list

**Difficulty:** Easy

**Problem statement**
Part A: flatten a list of lists exactly one level deep.
Part B: flatten a list nested to *arbitrary* depth.

**Example**
```
Part A: [[1, 2], [3, 4], [5]]        -> [1, 2, 3, 4, 5]
Part B: [1, [2, [3, [4, 5]], 6], 7]  -> [1, 2, 3, 4, 5, 6, 7]
```

**Expected task**
Solve Part A with a nested comprehension and again with `itertools.chain.from_iterable`.
Solve Part B with recursion. Then discuss: what breaks if the nesting is 10,000 levels deep?

**Starter skeleton**
```python
def flatten_one_level(nested: list[list]) -> list:
    """Flatten a list of lists exactly one level."""
    ...


def flatten_deep(nested: list) -> list:
    """Flatten a list nested to arbitrary depth, recursively."""
    ...
```

**Concept / pattern tested**
Nested comprehensions and their reading order, `itertools.chain`, recursion, Python's recursion
limit (~1000 frames).

**Why it's asked**
Part A tests comprehension fluency; Part B tests whether you can write a clean recursive
function under pressure. The recursion-limit follow-up is how the interviewer distinguishes
"knows recursion" from "knows recursion has a cost".

**Source:** Listed directly as item #4 in [DataInterview's Top 100 Python Interview
Questions](https://www.datainterview.com/blog/top-100-python-interview-questions) ("How do you
flatten a nested list in Python?"). Not tied to a specific company report.

---

## Q14. Debug: mutating a list while iterating over it

**Difficulty:** Easy

**Problem statement**
The following function is supposed to remove every even number from a list. It doesn't.

```python
def remove_evens(numbers):
    for n in numbers:
        if n % 2 == 0:
            numbers.remove(n)
    return numbers

print(remove_evens([1, 2, 4, 6, 7]))
```

**Example**
```
Expected: [1, 7]
Actual:   [1, 4, 7]
```

**Expected task**
Explain *precisely* why the output is wrong — trace the index pointer step by step. Then give
two correct fixes: one that builds a new list, and one that mutates the original list in place
(the caller may be holding a reference to it).

**Starter skeleton**
```python
def remove_evens_new_list(numbers: list[int]) -> list[int]:
    """Fix #1: return a new list, don't touch the original."""
    ...


def remove_evens_in_place(numbers: list[int]) -> None:
    """Fix #2: mutate the caller's list in place via slice assignment."""
    ...
```

**Concept / pattern tested**
Iterator invalidation, how `for` loops track position by index internally, `list.remove()` being
O(n) and value-based, in-place mutation via slice assignment (`numbers[:] = ...`).

**Why it's asked**
Your first debugging-round question. Interviewers ask this because the bug is silent — no
exception, just wrong data. Being able to *trace* rather than *guess* is the whole point, and
"build a new list vs mutate in place" is a genuine API-design decision, not a style preference.

**Source:** This exact trap — mutating a list while iterating over it — is a widely documented
Python pitfall (noted in [Python's own tutorial on data
structures](https://docs.python.org/3/tutorial/datastructures.html) as a reason to copy before
mutating) and appears in "tricky Python questions" interview content such as
[dev.to's Tricky Python Questions](https://dev.to/tomeraitz/tricky-python-questions-45gg). The
specific `remove_evens` example here is illustrative, not pulled from one company's leaked
interview.

---

# LEVEL 3 — INTERMEDIATE (Q15 – Q23)

Real interview territory. Expect these in a 45-minute live-coding screen.

---

## Q15. Group items by a computed key

**Difficulty:** Intermediate

**Problem statement**
Part A: given a list of words, group them so that all anagrams of each other end up in the same
group.
Part B: given a list of document dicts each with a `source` field, group the documents by
source.

**Example**
```
Part A:
Input:  ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat","tea","ate"], ["tan","nat"], ["bat"]]

Part B:
Input:  [{"id":"d1","source":"pdf"}, {"id":"d2","source":"web"}, {"id":"d3","source":"pdf"}]
Output: {"pdf": [d1, d3], "web": [d2]}
```

**Expected task**
Solve with `dict.setdefault()`, then with `collections.defaultdict(list)`. Then look at
`itertools.groupby` and explain the trap: why does it give the wrong answer on unsorted input?

**Starter skeleton**
```python
def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams of each other."""
    ...


def group_by_field(records: list[dict], field: str) -> dict[str, list[dict]]:
    """Group dict records by the value of a given field."""
    ...
```

**Concept / pattern tested**
The group-by-key pattern, `defaultdict`, choosing a canonical key (sorted string / tuple),
`itertools.groupby` requiring pre-sorted input.

**Why it's asked**
"Group anagrams" is a top-10 Python interview question, and the general grouping pattern is
something you write weekly in real work — grouping chunks by document, messages by session,
errors by type. The `groupby` trap is a favourite follow-up because so many people assume it
behaves like SQL `GROUP BY`.

**Source:** "Group Anagrams" (LeetCode #49) is confirmed asked at **Amazon** via a real onsite
interview report on [fastprep.io](https://www.fastprep.io/problems/amazon-group-anagrams) and
independently logged on [1Point3Acres' Amazon question
tracker](https://www.1point3acres.com/interview/problems/company/amazon/group-anagrams-lc-49)
(last reported asked 2026-08-14). More broadly tagged as asked at **Amazon, Google, Facebook,
and Microsoft** by [TechInView](https://www.techinview.dev/practice/group-anagrams) and
[jointaro.com](https://www.jointaro.com/interviews/questions/group-anagrams/?company=amazon).
The Part B "group by field" variant is a general practical pattern with no separate company tag.

---

## Q16. Multi-key custom sort with mixed directions

**Difficulty:** Intermediate

**Problem statement**
Sort a list of search results by `score` **descending**, and for equal scores by `title`
**ascending** (alphabetical). Do it in a single `sorted()` call.

**Example**
```
Input:
[{"title": "zebra", "score": 0.9},
 {"title": "apple", "score": 0.9},
 {"title": "mango", "score": 0.95}]

Output order: mango (0.95), apple (0.9), zebra (0.9)
```

**Expected task**
Build a tuple key. Handle the hard part: you cannot pass `reverse=True` because only one of the
two fields is reversed — find the two standard ways around this. Then explain what "stable sort"
means and how stability lets you solve this with two passes instead.

**Starter skeleton**
```python
def sort_results(results: list[dict]) -> list[dict]:
    """Sort by score descending, then title ascending on ties."""
    ...
```

**Concept / pattern tested**
Tuple keys, negating a numeric key vs relying on sort stability, `functools.cmp_to_key` as the
escape hatch, Timsort stability guarantees.

**Why it's asked**
Single-key sorting is Easy; mixed-direction multi-key sorting is where candidates actually
struggle. It's also a genuinely common requirement — reranking retrieved results by relevance
then recency is exactly this shape.

**Source:** General pattern. Multi-key sorting with mixed directions is a well-documented Python
technique (see [GeeksforGeeks on sorting by multiple
keys](https://www.geeksforgeeks.org/python/python-program-to-sort-the-list-according-to-the-column-using-lambda)),
but no specific company attribution was found for this exact framing.

---

## Q17. First non-repeating character in a string

**Difficulty:** Intermediate

**Problem statement**
Return the first character in a string that appears exactly once. Return `None` (or `-1` for
the index variant) if there is no such character.

**Example**
```
Input:  "swiss"    -> "w"
Input:  "aabbcc"   -> None
Input:  "leetcode" -> "l"  (index 0)
```

**Expected task**
Solve in two passes: count, then scan. Explain why one pass is not enough. Then answer: does
your solution still work correctly if the input is a generator instead of a string, and why not?

**Starter skeleton**
```python
def first_unique_char(text: str) -> str | None:
    """Return the first character that appears exactly once, or None."""
    ...
```

**Concept / pattern tested**
Two-pass counting, dict insertion order guaranteeing "first", the difference between a
re-iterable sequence and a one-shot iterator.

**Why it's asked**
It looks like Q2 but adds an ordering requirement that trips people up. The generator follow-up
is how interviewers check whether you understand iterator exhaustion — which matters directly
when you're streaming LLM tokens and try to loop over the stream twice.

**Source:** Listed directly as item #5 ("First Non-Repeating Character") in
[InterviewBit's Python Interview Questions](https://www.interviewbit.com/python-interview-questions/),
with the exact two-pass dictionary approach shown. Not tied to a specific company report.

---

## Q18. Merge overlapping intervals

**Difficulty:** Intermediate

**Problem statement**
Given a list of `[start, end]` intervals, merge all overlapping ones and return the merged list.

**Example**
```
Input:  [[1,3], [2,6], [8,10], [15,18]]
Output: [[1,6], [8,10], [15,18]]

Input:  [[1,4], [4,5]]
Output: [[1,5]]        # touching counts as overlapping
```

**Expected task**
Sort by start, then sweep. Handle: unsorted input, intervals that touch exactly at a boundary,
and one interval fully contained inside another.

**Starter skeleton**
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge all overlapping intervals, returning them sorted by start."""
    ...
```

**Concept / pattern tested**
Sort-then-sweep, tracking a running "current" interval, `max()` on the end boundary,
inclusive-vs-exclusive boundary reasoning.

**Why it's asked**
The most-asked non-trivial list problem in Python rounds, and the closest thing to real DSA in
this roadmap — included because it appears constantly. The boundary-condition discussion
(does `[1,4]` overlap `[4,5]`?) is where interviewers separate careful engineers from fast ones.

**Source:** "Merge Intervals" (LeetCode #56) appears as **confirmed Amazon interview question
#12** in [igotanoffer's dataset of 250+ real Glassdoor-sourced Amazon interview
reports](https://igotanoffer.com/blogs/tech/amazon-coding-interview-questions). Also presented
with a worked solution as item #1 in
[InterviewBit's Python Interview Questions](https://www.interviewbit.com/python-interview-questions/).

---

## Q19. Binary search, then `bisect`

**Difficulty:** Intermediate

**Problem statement**
Part A: implement binary search on a sorted list, returning the index of the target or `-1`.
Part B: given a sorted list of scores and a threshold, find the insertion point for that
threshold — i.e. how many items are below it — without a linear scan.

**Example**
```
Part A: search([1, 3, 5, 7, 9], 7)  -> 3
Part A: search([1, 3, 5, 7, 9], 4)  -> -1
Part B: scores = [0.1, 0.4, 0.6, 0.9], threshold = 0.5  -> insertion point 2
```

**Expected task**
Write the loop yourself first. Get the `mid` calculation and the `while low <= high` boundary
right — this is where everyone introduces an off-by-one. Then replace Part B with
`bisect.bisect_left` / `bisect_right` and explain the difference between them.

**Starter skeleton**
```python
def binary_search(sorted_items: list[int], target: int) -> int:
    """Return the index of target in a sorted list, or -1 if absent."""
    ...


def insertion_point(sorted_scores: list[float], threshold: float) -> int:
    """Return how many scores are strictly below threshold, using bisect."""
    ...
```

**Concept / pattern tested**
Binary search invariants, off-by-one discipline, the `bisect` module, O(log n) vs O(n).

**Why it's asked**
Binary search is the one search algorithm you're expected to write from memory at 2–3 years.
The `bisect` half tests standard-library breadth — knowing it exists is a strong "experienced
Python developer" signal, since most candidates hand-roll it.

**Source:** General fundamental — binary search is listed among core "algorithms" categories in
[CodingInterview.com's Python coding interview
guide](https://www.codinginterview.com/guide/python-coding-interview-questions-and-answers/).
It is a near-universal DSA requirement rather than a question tied to one company's specific
leaked interview; no single-company attribution found in this research pass.

---

## Q20. Split a list into batches of size N

**Difficulty:** Intermediate

**Problem statement**
Write a function that splits a list into consecutive chunks of at most N items. The final chunk
may be smaller.

**Example**
```
Input:  [1,2,3,4,5,6,7], n = 3
Output: [[1,2,3], [4,5,6], [7]]
```

**Expected task**
Implement with slicing and `range(0, len(items), n)`. Then write a **generator** version that
yields batches lazily instead of building the whole list. Then discuss: what should happen for
`n = 0` or a negative `n`?

**Starter skeleton**
```python
def batch(items: list, n: int) -> list[list]:
    """Split items into chunks of at most n, building the full list of batches."""
    ...


def batch_lazy(items: list, n: int):
    """Same idea, but yield each batch lazily instead of building them all."""
    ...
```

**Concept / pattern tested**
Strided `range`, list slicing (and why slicing past the end doesn't raise), generator functions,
input validation.

**Why it's asked**
Batching is one of the most common practical tasks in AI engineering — you batch documents for
an embeddings API, batch rows for a vector-DB upsert, batch requests to stay under rate limits.
The generator version is the follow-up that shows you're thinking about memory, and it sets up
Q24. (Python 3.12+ has `itertools.batched` — knowing that exists is a bonus point.)

**Source:** General practical pattern from data/ML pipeline coding tasks, not tied to a specific
company in the sources reviewed. Thematically adjacent to coding challenge #11 ("Rate Limiter &
Retry — token bucket, exponential backoff with jitter") in the [AI-Engineer-Interview-Questions
repo](https://github.com/ombharatiya/AI-Engineer-Interview-Questions), which covers the same
"process items in controlled groups" family of problems.

---

## Q21. Longest substring without repeating characters

**Difficulty:** Intermediate

**Problem statement**
Given a string, return the length of the longest substring that contains no repeated character.

**Example**
```
Input:  "abcabcbb" -> 3   ("abc")
Input:  "bbbbb"    -> 1   ("b")
Input:  "pwwkew"   -> 3   ("wke")
```

**Expected task**
Start with the brute force and state its complexity. Then build the sliding window with a
`seen` dict mapping character → last index. The hard part: when you find a repeat, where exactly
does the left pointer move to, and why can it never move backwards?

**Starter skeleton**
```python
def longest_unique_substring(text: str) -> int:
    """Return the length of the longest substring with no repeated character."""
    ...
```

**Concept / pattern tested**
Sliding window with two pointers, using a dict for last-seen positions, maintaining a window
invariant, O(n) with O(k) space.

**Why it's asked**
The archetypal sliding-window question and the most common "medium" in Python screens. Sliding
windows also show up directly in GenAI work — every rolling context window and every overlapping
text chunker is this pattern, which is why it sits right before Q27.

**Source:** This is LeetCode #3, one of the most frequently cited "top medium" questions across
general DSA prep content. This research pass did not turn up a specific verified company
attribution for it (unlike Q9, Q15, and Q18) — treat it as a widely-recommended fundamental
rather than a company-confirmed report.

---

## Q22. Flatten a nested dictionary into dotted keys

**Difficulty:** Intermediate

**Problem statement**
Given an arbitrarily nested dictionary (think: a parsed JSON config or an LLM's structured
output), produce a flat dictionary whose keys are the full paths joined by dots.

**Example**
```
Input:
{
  "model": {"name": "gpt-4o", "params": {"temperature": 0.2}},
  "retries": 3
}

Output:
{
  "model.name": "gpt-4o",
  "model.params.temperature": 0.2,
  "retries": 3
}
```

**Expected task**
Write it recursively with a `prefix` accumulator. Then handle the follow-up: what do you do
when a value is a *list* of dicts? Decide on a convention (e.g. `items.0.name`) and justify it.
Bonus: write the inverse function that un-flattens.

**Starter skeleton**
```python
def flatten_dict(nested: dict, prefix: str = "") -> dict:
    """Flatten a nested dict into dotted-path keys."""
    ...


def unflatten_dict(flat: dict) -> dict:
    """Bonus: invert flatten_dict."""
    ...
```

**Concept / pattern tested**
Recursion over dicts, accumulator parameters, `isinstance` type dispatch, designing a key
convention.

**Why it's asked**
Config flattening and JSON path extraction come up constantly in real Python work, and in AI
engineering specifically when you're normalising provider responses, logging structured traces,
or writing nested model output to a flat metrics store. It also tests recursion on a shape
that isn't a list.

**Source:** General practical pattern seen in config-handling and JSON-normalisation coding
tasks. Not tied to a specific company report in the sources reviewed.

---

## Q23. Debug: mutable default argument + shallow vs deep copy

**Difficulty:** Intermediate

**Problem statement**
Two related snippets. Predict the output of each, explain the mechanism, and fix both.

```python
# Snippet A
def add_message(text, history=[]):
    history.append(text)
    return history

print(add_message("hi"))
print(add_message("hello"))


# Snippet B
import copy
default_config = {"model": "gpt-4o", "tools": ["search", "calc"]}

user_config = copy.copy(default_config)
user_config["tools"].append("email")
user_config["model"] = "gpt-4o-mini"

print(default_config)
```

**Example**
```
Snippet A expected: ["hi"] then ["hello"]
Snippet A actual:   ["hi"] then ["hi", "hello"]

Snippet B: what exactly does default_config look like at the end, and why is
           "model" unaffected while "tools" is not?
```

**Expected task**
For A: explain *when* default arguments are evaluated, and give the `None`-sentinel fix.
For B: explain reference semantics one level down, and when `copy.deepcopy` is the right call
versus when it's an expensive mistake.

**Starter skeleton**
```python
def add_message_fixed(text: str, history: list[str] | None = None) -> list[str]:
    """Fixed version of Snippet A — no shared mutable default."""
    ...
```
*(Snippet B is a predict-and-explain exercise — no function to write, just trace it and say
what you'd change.)*

**Concept / pattern tested**
Function-definition-time vs call-time evaluation, the `None` sentinel idiom, shallow vs deep
copy, mutable vs immutable values, reference sharing.

**Why it's asked**
These two are on essentially every "experienced Python candidate" question list, and they are
not trivia — a shared mutable default in a conversation-history helper or an agent state object
leaks data between users. That is a real production incident, and interviewers know it.

**Source:** Both traps are presented as the first two "Conceptual Round" questions in
[Generalist Programmer's 20 Worked
Examples](https://generalistprogrammer.com/tutorials/python-interview-questions) — question #1
("Why are mutable default arguments dangerous?") and question #4 ("Shallow copy vs deep copy?"),
with nearly identical code shown. Widely echoed across other general Python interview lists;
not tied to one specific company's leaked interview.

---

# LEVEL 4 — ADVANCED-INTERMEDIATE (Q24 – Q30)

Everything here is Python you would actually ship. Q26–Q30 are the AI/GenAI-flavoured
questions that show up in LLM/AI engineer loops as "practical warm-ups".

---

## Q24. Stream a large file lazily with a generator

**Difficulty:** Advanced-Intermediate

**Problem statement**
You have a 5 GB JSONL file (one JSON object per line) that will not fit in memory. Write a
generator that yields one parsed record at a time. Skip malformed lines instead of crashing,
but keep a count of how many were skipped. Then use it to count records matching a condition.

**Example**
```
records = read_jsonl("events.jsonl")     # returns a generator, reads nothing yet
first = next(records)                    # now exactly one line has been read
count = sum(1 for r in records if r["status"] == "error")
```

**Expected task**
Use `yield`. Prove to yourself that nothing is read until you iterate. Then answer: how do you
return the skipped-line count from a generator, given that `return` inside a generator doesn't
work the way you'd expect? Also explain why you cannot iterate the same generator twice.

**Starter skeleton**
```python
def read_jsonl(path: str):
    """Yield one parsed JSON record at a time; skip malformed lines."""
    ...
```

**Concept / pattern tested**
Generator functions, lazy evaluation, O(1) memory, generator exhaustion, `StopIteration.value`
vs a mutable stats object vs a class with `__iter__`, error handling inside a stream.

**Why it's asked**
"How do you handle a file too large for memory?" is a standard question, and generators are the
answer. In AI pipelines this is the ingestion path for every corpus you'll ever index — and
streaming LLM responses are generators too, so the mental model transfers directly.

**Source:** General pattern — "how do you handle large files without loading them into memory"
is listed as item #20 in [DataInterview's Top 100 Python Interview
Questions](https://www.datainterview.com/blog/top-100-python-interview-questions). The same
"stream large data lazily" theme also underlies coding challenge #13 ("Streaming Parser — SSE
parser, incremental tool-call argument assembly") in the [AI-Engineer-Interview-Questions
repo](https://github.com/ombharatiya/AI-Engineer-Interview-Questions), though that challenge is
SSE-specific rather than JSONL-specific. No single-company attribution found for this exact
JSONL framing.

---

## Q25. Write a retry decorator with exponential backoff

**Difficulty:** Advanced-Intermediate

**Problem statement**
Write a decorator `@retry(max_attempts=3, base_delay=1.0)` that retries the wrapped function
when it raises a specified exception type, waiting `base_delay * 2**attempt` seconds between
attempts, and re-raising the original exception if all attempts fail.

**Example**
```python
@retry(max_attempts=3, base_delay=0.5, exceptions=(TimeoutError,))
def call_llm(prompt: str) -> str:
    ...

# attempt 1 fails -> sleep 0.5s
# attempt 2 fails -> sleep 1.0s
# attempt 3 fails -> raise the original TimeoutError
```

**Expected task**
Build it as a decorator factory (three nested functions — this is the part people get wrong).
Use `*args, **kwargs` so it wraps any signature, and `functools.wraps` so the wrapped function
keeps its name and docstring. Then discuss: why add random jitter, and why should you *not*
retry on a 400-level error?

**Starter skeleton**
```python
def retry(max_attempts: int = 3, base_delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator factory: retry the wrapped function with exponential backoff."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            ...
        return wrapper
    return decorator
```

**Concept / pattern tested**
Closures, decorator factories (decorator with arguments), `*args/**kwargs`, `functools.wraps`,
exception handling, exponential backoff and jitter.

**Why it's asked**
Decorators are the number-one "advanced Python" interview topic, and retry-with-backoff is the
exact example AI interview guides list as a standard coding warm-up. Every LLM API call in
production sits behind one, because providers rate-limit and time out constantly. Knowing
*which* errors are worth retrying is the senior part of the answer.

**Source:** Explicitly documented as a **real Anthropic AI engineering interview question**
("LLM APIs are unreliable in production — they return rate limit errors (429)...") on
[velocode.ai](https://velocode.ai/practice/resilient-llm-api-calls-with-exponential-backoff-retry-logic).
Also appears as coding challenge #11 ("Rate Limiter & Retry — token bucket, exponential backoff
with jitter") in the [AI-Engineer-Interview-Questions
repo](https://github.com/ombharatiya/AI-Engineer-Interview-Questions), and as an explicit item
in [GenAI Engineer Interview Questions 2026](https://cloudsoftsol.com/blog/genai-engineer-interview-questions-2026/)
(Section 18, "How do you implement retries?").

---

## Q26. Build a caching layer for expensive calls

**Difficulty:** Advanced-Intermediate

**Problem statement**
Part A: write a memoization decorator that caches a function's return value keyed by its
arguments.
Part B: replace it with `functools.lru_cache` and explain what `maxsize` does.
Part C: your cached function takes a `dict` of options as an argument and `lru_cache` raises
`TypeError: unhashable type: 'dict'`. Explain why, and give two ways to fix it.

**Example**
```python
@lru_cache(maxsize=128)
def embed(text: str) -> tuple[float, ...]:
    ...   # expensive API call

embed("hello")   # calls the API
embed("hello")   # returns from cache, no API call
```

**Expected task**
Implement Part A by hand with a dict. Then answer the production questions: what happens to
memory if `maxsize=None`, why is caching a method on `self` a memory-leak risk, and what makes
caching an *LLM* call different from caching a pure function.

**Starter skeleton**
```python
def memoize(func):
    """Part A: hand-rolled memoization decorator."""
    cache = {}
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

**Concept / pattern tested**
Memoization, `functools.lru_cache` / `cache`, hashability of cache keys, cache eviction,
unbounded-cache memory growth.

**Why it's asked**
Caching is listed explicitly in GenAI coding-round question banks ("implement caching for LLM
responses"), and it's the cheapest single lever for cutting LLM cost. The unhashable-argument
problem is a real thing you will hit within a week of using `lru_cache`.

**Source:** Listed verbatim as item #18 ("Implement caching for LLM responses") in Section 17 of
[GenAI Engineer Interview Questions 2026](https://cloudsoftsol.com/blog/genai-engineer-interview-questions-2026/).
No specific company attribution found for this exact framing, though caching is called out
generally as a top-priority topic across multiple GenAI interview guides reviewed.

---

## Q27. Chunk text with overlap (no LangChain)

**Difficulty:** Advanced-Intermediate

**Problem statement**
Write a function `chunk_text(text, chunk_size, overlap)` that splits text into chunks of
`chunk_size` words with `overlap` words repeated between consecutive chunks.

**Example**
```
text = "a b c d e f g h i j"
chunk_text(text, chunk_size=4, overlap=2)

-> ["a b c d",
    "c d e f",
    "e f g h",
    "g h i j"]
```

**Expected task**
Get the step size right (`chunk_size - overlap`) and make sure the loop terminates — if
`overlap >= chunk_size` you get an infinite loop, so validate the inputs. Handle text shorter
than one chunk. Then discuss: why overlap at all, what breaks when you split mid-sentence, and
how a token-based splitter differs from a word-based one.

**Starter skeleton**
```python
def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into word-based chunks with overlapping words between them."""
    ...
```

**Concept / pattern tested**
Windowing with a stride, off-by-one and termination conditions, input validation, reusing your
Q20/Q21 instincts.

**Why it's asked**
"Implement basic text chunking without LangChain" appears verbatim in GenAI coding question
banks. It is the single most representative AI-engineer warm-up: trivial-looking, easy to get
subtly wrong, and it opens straight into the RAG trade-off discussion (fixed-size vs sentence
vs semantic vs structure-aware chunking) that interviewers actually want to have.

**Source:** Listed verbatim as item #4 ("Implement basic text chunking without LangChain") in
Section 17 of [GenAI Engineer Interview Questions
2026](https://cloudsoftsol.com/blog/genai-engineer-interview-questions-2026/). Also appears as a
dedicated coding challenge — [`09_text_chunking.py`
](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/12-coding-challenges/09_text_chunking.py)
("Fixed, sliding-window, recursive, sentence chunkers") in the AI-Engineer-Interview-Questions
repo, which aggregates public interview material across 25 companies including Anthropic,
OpenAI, and Google DeepMind.

---

## Q28. Cosine similarity and top-K retrieval from scratch

**Difficulty:** Advanced-Intermediate

**Problem statement**
Part A: implement cosine similarity between two vectors using **pure Python only** — no NumPy.
Part B: given a query vector and a dict of `doc_id -> vector`, return the top K most similar
documents with their scores, sorted by score descending.

**Example**
```
a = [1, 0, 1]
b = [1, 1, 0]
cosine_similarity(a, b) -> 0.5

query = [1, 0, 1]
docs  = {"d1": [1, 0, 1], "d2": [0, 1, 0], "d3": [1, 1, 1]}
top_k(query, docs, k=2) -> [("d1", 1.0), ("d3", 0.816...)]
```

**Expected task**
Handle the zero-vector case (division by zero) explicitly. Reuse your Q12 sorting pattern for
top-K, then improve it with `heapq.nlargest` and explain when that's actually better than
sorting. Finally: state the NumPy one-liner and explain why it's faster.

**Starter skeleton**
```python
def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors, pure Python (no NumPy)."""
    ...


def top_k(query: list[float], docs: dict[str, list[float]], k: int) -> list[tuple[str, float]]:
    """Return the k most similar doc_ids to query, sorted by score descending."""
    ...
```

**Concept / pattern tested**
`zip()` + `sum()` for dot products, `math.sqrt`, guarding division by zero, sorting vs heap for
top-K (O(n log n) vs O(n log k)), vectorisation.

**Why it's asked**
This is named explicitly as a warm-up in published AI-engineer interview loops (Amazon GenAI
among them). Interviewers use it to check that you understand what a vector database is doing
underneath rather than only knowing which SDK method to call — and the follow-up is always
"when would you use dot product or Euclidean instead, and why is cosine the default?"

**Source:** Explicitly documented — **Amazon GenAI pairs a standard LeetCode problem with
cosine-similarity in NumPy** as part of its coding round, per
[openagenthub.io's company-by-company coding round breakdown](https://openagenthub.io/interview/coding-rounds/).
Also appears as coding challenge #08 ("Semantic Search / RAG — embed, index, cosine retrieval,
context assembly") in the [AI-Engineer-Interview-Questions
repo](https://github.com/ombharatiya/AI-Engineer-Interview-Questions), and listed as item #2
("Implement cosine similarity in Python") in Section 17 of
[GenAI Engineer Interview Questions 2026](https://cloudsoftsol.com/blog/genai-engineer-interview-questions-2026/).

---

## Q29. Safely extract and validate JSON from an unreliable text response

**Difficulty:** Advanced-Intermediate

**Problem statement**
An LLM was asked to return JSON but sometimes returns it wrapped in prose or a markdown code
fence, and sometimes returns malformed JSON. Write a function that extracts and parses the JSON
object, validates that the required fields are present and correctly typed, and raises a clear,
custom exception when it cannot.

**Example**
```
Input:  'Sure! Here you go:\n```json\n{"name": "Kamran", "score": 9}\n```'
Output: {"name": "Kamran", "score": 9}

Input:  'Here you go: {"name": "Kamran", "score": "nine"}'
Output: raises ValidationError("score must be an int, got str")

Input:  'I could not answer that.'
Output: raises ParseError("no JSON object found in response")
```

**Expected task**
Extract the candidate JSON substring, parse with `json.loads` inside a narrow `try/except
json.JSONDecodeError`, then validate. Define your own exception classes. Then discuss the
production answer: why hand-rolled validation loses to Pydantic v2 / the provider's structured
output mode, and what your retry-repair strategy should be when parsing fails.

**Starter skeleton**
```python
class ParseError(Exception):
    """Raised when no JSON object can be found in the response."""


class ValidationError(Exception):
    """Raised when the parsed JSON doesn't match the expected shape."""


def extract_and_validate_json(response_text: str, required: dict[str, type]) -> dict:
    """Extract a JSON object from a messy LLM response and validate its fields."""
    ...
```

**Concept / pattern tested**
`json` module, `try/except` scoping (catch narrow, not bare `except`), custom exception
hierarchies, exception chaining with `raise ... from e`, defensive parsing of untrusted input.

**Why it's asked**
"Implement structured JSON output validation" is a listed GenAI coding-round task, and treating
the LLM as a flaky external dependency is the mindset interviewers are probing for. Bare
`except:` in your answer is an instant red flag — expect to be asked why.

**Source:** Listed verbatim as item #15 ("Implement structured JSON output validation") in
Section 17 of [GenAI Engineer Interview Questions
2026](https://cloudsoftsol.com/blog/genai-engineer-interview-questions-2026/). No specific
company attribution found for this exact framing, though "how do you get structured/JSON output
reliably" is called out as a standard question across multiple GenAI interview guides reviewed
(e.g. the [AI Engineer Interview Playbook](https://dev.to/truongpx396/the-ai-engineer-interview-playbook-45pb), Q39).

---

## Q30. Write a context manager for timing and usage tracking

**Difficulty:** Advanced-Intermediate

**Problem statement**
Build a context manager `track("embed_batch")` that records how long the block took and
accumulates token counts reported inside it, printing a summary on exit — and doing so even
when the block raises.

**Example**
```python
with track("embed_batch") as t:
    t.add_tokens(1200)
    result = call_api(...)
    t.add_tokens(340)

# on exit: [embed_batch] 1.83s, 1540 tokens
# if call_api raises: still logs, then the exception propagates
```

**Expected task**
Implement it as a class with `__enter__` / `__exit__` first. Understand exactly what `__exit__`
receives, and what returning `True` from it does (and why that's usually a bug). Then rewrite it
using `contextlib.contextmanager` with `try/finally`, and say which version you'd prefer and why.

**Starter skeleton**
```python
class track:
    """Context manager: time a block and accumulate token counts."""

    def __init__(self, label: str):
        ...

    def __enter__(self):
        ...
        return self

    def add_tokens(self, count: int) -> None:
        ...

    def __exit__(self, exc_type, exc_val, tb):
        ...
```

**Concept / pattern tested**
The context-manager protocol, `__enter__` return value, `__exit__(exc_type, exc_val, tb)`,
exception suppression, `contextlib.contextmanager` and the `yield` inside `try/finally`,
guaranteed cleanup.

**Why it's asked**
Context managers are the standard "do you understand Python's resource model" question, and this
version doubles as an observability question — tracking latency and token cost per operation is
core AI-engineering work. The `return True` trap is the specific thing interviewers are waiting
to ask about.

**Source:** General pattern for the context-manager mechanics themselves (widely documented,
e.g. in the `with` statement item of
[DataInterview's Top 100](https://www.datainterview.com/blog/top-100-python-interview-questions)).
The token/latency-tracking framing specifically reflects a priority repeatedly named across
GenAI interview guides — e.g.
["observability (tokens/latency/costs)" is called out as improving senior-interview chances](https://www.stackoverflowtips.com/posts/top-50-genai-llm-interview-questions-answers-2025) —
but this exact `track()` question was constructed for this roadmap rather than pulled from one
company's leaked interview; treat it as a realistic composite, not a confirmed report.

---

## After you finish all 30

You should be able to do these without notes:

- Turn any O(n²) nested loop into O(n) with a dict or set, and say the complexity out loud.
- Write `Counter`, `defaultdict`, `zip`, `enumerate`, `sorted(key=...)`, `bisect` and
  `heapq.nlargest` without looking them up.
- Explain mutable defaults, shallow vs deep copy, generator exhaustion and iterator invalidation
  by mechanism, not by memorised definition.
- Write a decorator with arguments, a generator, and a context manager from a blank file.
- Implement chunking, cosine similarity, retry/backoff, caching and JSON validation from scratch
  — and then explain why you'd use a library for each in production.

Progress and notes: see `progress-tracker.md` in this folder.
