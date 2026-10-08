# Accenture AI Engineer HackerRank Assessment (India, 5–6+ YOE)

> **Prepared:** 7 Oct 2026 · **Process:** HackerRank Technical Assessment → Level 1 Skill Round → Final Round
> **Part 1** is the research report (what candidates actually reported). **Part 2** is a practice bank built from it, with verified Python/SQL solutions.

---

## Contents

- [Part 1 — Research report](#part-1--research-report)
  - [TL;DR](#tldr)
  - [Executive summary](#executive-summary)
  - [Evidence table](#evidence-table)
  - [Findings per question](#findings-per-question)
  - [Repeated patterns vs isolated claims](#repeated-patterns-vs-isolated-claims)
  - [Likely assessment blueprint](#likely-assessment-blueprint-ai-engineer-56-yoe-india)
  - [72-hour preparation priority list](#72-hour-preparation-priority-list)
  - [Gaps and uncertainties](#gaps-and-uncertainties)
  - [Sources](#sources)
- [Part 2 — Practice question bank](#part-2--practice-question-bank)
  - [2.0 Read this first: what is "actual" and what isn't](#20-read-this-first-what-is-actual-and-what-isnt)
  - [2.1 Exact coding problems reported by candidates](#21-exact-coding-problems-reported-by-candidates)
  - [2.2 Reported task types without published statements → practice equivalents](#22-reported-task-types-without-published-statements--practice-equivalents)
  - [2.3 Actual questions reported from Accenture AI/ML interview rounds](#23-actual-questions-reported-from-accenture-aiml-interview-rounds)
  - [2.4 Practice MCQs (36)](#24-practice-mcqs-36)
  - [2.5 Practice coding set (20 problems)](#25-practice-coding-set-20-problems)
  - [2.6 SQL practice set (9 queries)](#26-sql-practice-set-9-queries)
  - [2.7 pandas practice set](#27-pandas-practice-set)
  - [2.8 Hands-on "build" task: FastAPI CRUD](#28-hands-on-build-task-fastapi-crud)
  - [2.9 Two timed mock tests](#29-two-timed-mock-tests)

---

# Part 1 — Research report

## TL;DR

The most likely format is a short, auto-scored HackerRank test built around your skill tag, about **30–90 minutes**: some MCQs plus **one or two hands-on coding tasks, most likely in Python**. It is unlikely to be the freshers' 90-question aptitude test.

**Caveat:** no public first-hand report from 2024–2026 describes the HackerRank test for the "AI Engineer" title itself. The blueprint is built from Accenture's official assessment FAQ plus reports from nearby experienced-hire tracks, and each piece is labelled that way.

- **Format (official + adjacent roles):** HackerRank, one sitting, window typically 72 hours, about 30–90 minutes "depending on your proficiency level", auto-scored against a threshold, no external AI tools. Experienced candidates in adjacent roles report "MCQ and 1 coding question" (Databricks, 5.7 YOE) or two stack-specific coding tasks (Spring Boot, 3 YOE: Java comparator sort + CRUD API in 90 minutes).
- **Content is skill-tagged, not generic DSA.** For an AI Engineer tag, the best bet is Python coding (strings, arrays, dictionaries, OOP, maybe pandas), basic/medium SQL, and possibly ML/GenAI MCQs. **No public report confirms GenAI MCQs inside the HackerRank test itself.**
- **72-hour plan:** two timed 45-minute Python sessions on easy/medium array, string, dictionary and interval problems; revise SQL joins, GROUP BY and window functions; one block on ML, LLM and RAG fundamentals (definitely tested in the Level 1 and Final rounds); take the test in a quiet, well-lit room, webcam on, full-screen, nothing else running.

## Executive summary

Accenture's careers FAQ (India page, live in 2026) is the most reliable source. It confirms:

- The technical assessment runs on **HackerRank**, taken online in **one sitting** "within the timeframe specified, typically within 72 hours."
- Most assessments take "approximately **30–90 minutes**, depending on your proficiency level", in "a coding environment designed to reflect real engineering tasks."
- Scoring is automatic "against predefined criteria (such as test cases, answer keys, or scoring rules)." Candidates who reach "the validated threshold proceed to the next stage."
- A fail means a **90-day wait** before retaking the same assessment.
- It is calibrated "in line with your experience level." A built-in HackerRank AI Assistant may be enabled for some hands-on questions, but "use of external AI tools is not permitted."

First-hand evidence for the AI Engineer title is thin. Glassdoor's Accenture "AI Engineer" and "AI/ML Engineer" pages list "Skills test" as a common stage (50% and 33% of reviews), but the written reviews describe interviews, not HackerRank content.

The most useful first-hand data comes from experienced candidates in nearby tracks. Together they show a skill-tagged test, not a campus aptitude test:

- **Databricks, 5.7 YOE:** "Mcq and 1 coding question."
- **Spring Boot, 3 YOE:** "2 coding questions for 90 mins like one from java [comparator sort] other from springboot like curd operations."
- **FastAPI/Python developer:** a "pyspark/aws/coding/python assessment."

The 90-MCQ cognitive/technical + 2-coding-question format that dominates GeeksforGeeks and Naukri Code360 write-ups is the **freshers' campus process** and should not be treated as your format.

## Evidence table

| # | Source | Date | Role | Experience | What was reported | Confidence |
|---|---|---|---|---|---|---|
| 1 | [Accenture Careers FAQ (India)](https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture) (official) | Live 2026 | All roles with a technical assessment | All | HackerRank; one sitting; ~72h window; ~30–90 min by proficiency; auto-scored vs threshold; calibrated to experience; external AI banned; built-in AI Assistant may be on; 90-day retake wait | **High** |
| 2 | [Fishbowl/Glassdoor thread](https://www.fishbowlapp.com/post/hias-part-of-the-screening-process-for-accenture-i-received-a-hackerrank-assessment-for-a-databricks-role-requiring-5-7) | ~Mar 2026 | Databricks (adjacent) | 5.7 YOE | "Mcq and 1 coding question"; SQL-vs-Python follow-up unanswered | Medium |
| 3 | [Glassdoor Community](https://www.glassdoor.com.au/Community/interview-experience/hi-i-received-a-hackerrank-assessment-from-accenture-for-the-custom-software-engineer-spring-boot-role-with-3-years-experience) | ~mid-2026 | Custom Software Engineer, Spring Boot (adjacent) | 3 YOE | "2 coding questions for 90 mins … java [comparator sort] … springboot like curd operations" | Medium |
| 4 | [Fishbowl "Accenture confessions"](https://www.fishbowlapp.com/post/hi-folks-i-received-a-hackerrank-assessment-for-a-backend-role-at-accenture-45-yoe-has-anyone-taken-it-recently-would-love) ([Glassdoor mirror](https://www.glassdoor.co.in/Community/accenture-confessions/hi-folks-i-received-a-hackerrank-assessment-for-a-backend-role-at-accenture-45-yoe-has-anyone-taken-it-recently-would-love)) | Post ~Mar 2026, reply ~Jul 2026 | Backend 4–5 YOE; FastAPI Custom App Dev (replier) | 4–5 YOE | Assessment → technical → final → "once again pyspark/aws/coding/python assessment"; replier "was unable to clear" it | Medium-low |
| 5 | [Fishbowl, CL9 Spring Boot](https://www.fishbowlapp.com/post/what-is-the-format-of-accenture-online-assessment-for-level-9-spring-boot-developer-role-i-got-hackerrank-assessment) | Undated | Spring Boot, CL9 | CL9 | "First will be java coding question and second will be spring boot full code" | Low-medium |
| 6 | Glassdoor Community "Accenture confessions" (Oracle PL/SQL) | ~Sep 2026 | Oracle PL/SQL (adjacent) | Experienced | Online assessment to finish "within 72 hours" before any interview | Medium |
| 7 | [InterviewFox blog](https://interviewfox.ai/interview-questions/accenture-hackerrank/) | 15 Sep 2026 (test ~Feb 2026) | Custom Software Engineer, Java Full-Stack GenAI | Not stated | 2 Java problems in ~45 min (Minimum CPU Cores; Password Sanitizer); also Desired Array, Majority Element; Python block (strings, arrays, dicts, "tricky" OOP + basic SQL); Data Engineer block (Databricks MCQs, SQL window functions, PySpark) | **Low** (sells an AI-cheating tool; not India-specific) |
| 8 | [Glassdoor AI Engineer reviews](https://www.glassdoor.com/Interview/Accenture-AI-Engineer-Interview-Questions-EI_IE4138.0,9_KO10,21.htm) | Jun 2026 (Chennai); Jan 2026 (Dublin) | AI Engineer (target) | Not stated | Technical round "completely based on basics"; "Difference between Classification and regression", "evaluation matrix"; 50% list "Skills test" | Medium (interviews, not OA) |
| 9 | [Glassdoor AI/ML Engineer reviews](https://www.glassdoor.co.in/Interview/Accenture-AI-ML-Engineer-Interview-Questions-EI_IE4138.0,9_KO10,24.htm) | Sep 2026 (Pune); Feb 2026 (Pune) | AI/ML Engineer | Not stated | 45-min screen: Python fundamentals, FastAPI basics, 2 array/string problems (one list comprehension), Docker/K8s; prompt engineering → guardrails, evaluation, MCP servers, LLM-cost scenario; Azure AI services, Azure ML, RAG, MLOps, transfer learning, "What is vector embedding" | Medium-high (interview rounds) |
| 10 | [GfG: LLM Operations Engineer (Experienced)](https://www.geeksforgeeks.org/interview-experiences/accenture-final-interview-experience-for-llm-operations-engineer-experienced-selected/) | Dec 2025 | LLMOps Engineer | 2+ YOE | Skill round + Final (tech + managerial, Pune office, PAN ID check); RAG internals, vector DB, LangChain vs CrewAI, Transformers, MCP, Python `__init__`/OOP/inheritance, PUT vs PATCH | Medium-high |
| 11 | [GfG: Software Engineer](https://www.geeksforgeeks.org/interview-experiences/accenture-interview-experience-1/) | Oct 2024 | Software Engineer | Unclear | HackerRank: "two medium-difficulty coding problems" + CS-basics MCQs | Low-medium |
| 12 | Naukri Code360 / GfG campus write-ups ([e.g.](https://www.naukri.com/code360/interview-experiences/accenture-solutions-private-limited/accenture-interview-experience-on-campus-oct-2025)) | 2020–2025 | ASE / Advanced ASE | Freshers | 90 MCQs/90 min + 2 coding/45 min + communication test | High for freshers; **not applicable** to you |
| 13 | [Glassdoor Python Developer review](https://www.glassdoor.com.mx/Entrevista/Accenture-Entrevista-E4138-RVW97354753.htm) | May 2025 (Hyderabad) | Python Developer (adjacent) | Not stated | Interview on data structures, OOP, libraries, decorators, MRO, generators, pandas, args/kwargs, `namedtuple`, lambdas, exceptions | Medium (interview, not OA) |

## Findings per question

### 1. Format and number of questions
- **Official:** one sitting, ~72h window, ~30–90 min, total time shown before start, auto-submit on timeout.
- **Adjacent experienced roles:** "MCQ and 1 coding question" (Databricks); 2 coding questions in 90 min (Spring Boot); Java coding + Spring Boot "full code" (CL9).
- **Expect:** 2–3 sections — an MCQ block + 1–2 hands-on tasks, or 2 hands-on tasks with no MCQs. No AI Engineer report gives an exact MCQ count.

### 2. MCQs vs coding vs SQL/Python/AI/ML/GenAI
- Coding appears in every experienced report. MCQs in one adjacent report (Databricks). SQL only in the low-confidence InterviewFox page.
- **No public report confirms ML/LLM/RAG/LangChain MCQs inside the HackerRank test.** These topics are heavily confirmed in the *interview* rounds.

### 3. Language choice
- The FAQ names no languages. InterviewFox claims C, C++, Java, Python (+ .NET/C# on some tracks) — low confidence.
- Stack-specific tracks lock the language (Java/Spring for Spring Boot; PySpark/AWS/Python for FastAPI).
- **Assume Python** for an AI Engineer tag (inference, not confirmed).

### 4. Difficulty and duration
- Officially 30–90 min. One report: 90 min for 2 tasks; InterviewFox: ~45 min for 2 problems.
- Easy to medium ("not LeetCode-hard"), but experienced candidates do fail stack-specific tasks (the FastAPI candidate failed a PySpark-heavy test).
- Scored per hidden test case against an unpublished threshold.

### 5. Different for 5–6+ YOE vs freshers?
**Yes, high confidence.** Official wording: calibrated "in line with your experience level." Every experienced report describes skill-tagged tasks, not the freshers' aptitude/pseudocode/communication battery. No data separates CL8/CL9/CL10.

### 6. Reported questions and topics
- **Coding (low confidence, InterviewFox):** Minimum CPU cores (inclusive interval overlap); Password Sanitizer; Desired Array; Majority Element. → full statements in [§2.1](#21-exact-coding-problems-reported-by-candidates).
- **Coding (medium):** Java comparator sort; Spring CRUD API.
- **AI/ML (interview rounds, medium-high):** classification vs regression; evaluation metrics; RAG step by step; vector embeddings; vector DB contents; Transformers; transfer learning; Azure AI / Azure ML; MLOps; prompt engineering, guardrails, evaluation; MCP; LangChain vs CrewAI; parallel agents; LLM cost spikes; Python `__init__`/OOP/inheritance; list comprehension; FastAPI; Docker/K8s probes; PUT vs PATCH.

### 7. Role-specific or generic?
**Role/skill-specific.** Official: "tasks that reflect the kind of work you would do in the role." Every experienced report matches the applicant's stack.

### 8. Proctoring
- **Official:** "Assessment conditions and integrity measures may apply"; external AI banned; AI-enabled insights about your platform interaction may be reviewed.
- **HackerRank platform features (documented):** copy/paste tracking on every test; Tab Proctoring (off by default); Secure Mode (full-screen, tab-switch alerts, external copy/paste blocked); Proctor Mode (webcam image every 5 s, screenshot every 15 s). **Whether Accenture enables Secure/Proctor Mode is not confirmed.**
- No AI Engineer candidate report describes proctoring.

### 9. Subsequent rounds
- **Level 1 skill round (AI/ML, India 2025–26):** ~45-min technical interview — Python fundamentals, live array/string coding, project deep dive, then GenAI system design (RAG, embeddings, guardrails, evaluation, MCP, cost, Azure deployment).
- **Final:** technical + managerial; one LLMOps case was held from an Accenture office with a PAN ID check.
- **Re-assessment:** some candidates report a second assessment after interviews (one Fishbowl reply + InterviewFox).

## Repeated patterns vs isolated claims

**Repeated (multiple independent sources)**
- HackerRank, ~72h window, issued *before* interviews for experienced roles (FAQ, Oracle PL/SQL post, backend thread).
- Content tied to the applicant's stack (Databricks, Spring Boot ×2, FastAPI/PySpark).
- Small question count: 1–2 hands-on tasks with or without MCQs.
- AI/ML interviews in India focus on Python basics + RAG, embeddings, Azure AI, MLOps.

**Isolated or uncertain**
- Exact coding problems (CPU cores, password sanitizer): one commercial source with a conflict of interest.
- Python-track block "strings, arrays, dictionaries, tricky OOP + basic SQL": InterviewFox only.
- "Audit failed" retakes: InterviewFox only.
- Second assessment after interviews: one Fishbowl reply + InterviewFox.
- ML/GenAI MCQs inside the HackerRank test: **no direct evidence**.

## Likely assessment blueprint (AI Engineer, 5–6+ YOE, India)

| Aspect | Most likely |
|---|---|
| Platform/rules | HackerRank, one sitting, auto-submit at the limit shown on the start screen (likely 60–90 min). External AI banned. Webcam/full-screen proctoring possible, unconfirmed. |
| Core | 1–2 Python coding problems, easy/medium: strings, arrays, dicts, sorting/intervals, possibly OOP. Hidden test cases, partial credit. |
| Possible | One SQL or pandas data-manipulation task. |
| Possible (unverified) | MCQ block on Python, ML fundamentals, GenAI concepts. |
| Less likely | Framework "build" task (FastAPI endpoint or small LLM/RAG function), possibly with HackerRank's built-in AI Assistant. |
| Language | Python, required or available. |

## 72-hour preparation priority list

1. **Open the invite now and read the start screen** before starting the timer: total time, sections, allowed languages, AI Assistant on/off. Run HackerRank's sample test to learn the IDE.
2. **Python coding under time pressure (highest weight):** two timed 45-min sets of two problems (use [§2.9](#29-two-timed-mock-tests)). Arrays, strings, dict/`Counter`, custom-key sorting, interval overlap, validation/filtering. Watch edge cases (inclusive bounds, empty input) — scoring is per test case.
3. **Python fundamentals & OOP:** classes, `__init__`, inheritance, dunders, comprehensions, generators, `*args/**kwargs`, exceptions.
4. **SQL/pandas:** joins, GROUP BY/HAVING, ROW_NUMBER/RANK/DENSE_RANK; pandas `groupby`, `merge`, filtering.
5. **ML & GenAI fundamentals** (possible MCQs + Level 1 round): classification vs regression; precision/recall/F1; overfitting; embeddings and vector DBs; RAG end to end; transformers/attention; prompt engineering & guardrails; LangChain/agents & MCP; Azure OpenAI/Azure ML deployment; LLM cost control.
6. **Exam conditions:** stable internet, quiet bright room, close other apps/overlays, stay full-screen, no tab switching. Take it early in the window so there's time to report technical issues. A fail = 90-day wait.

## Gaps and uncertainties

- No public first-hand 2024–2026 report names the AI Engineer HackerRank content. Reddit, LinkedIn, AmbitionBox, YouTube and LeetCode Discuss returned nothing citable; many Glassdoor/Fishbowl answers are behind a login.
- The most detailed source (InterviewFox) sells an AI cheating tool and is not India-specific. Its claims are low confidence and its tool advice should be ignored — it breaks Accenture's explicit ban.
- Fishbowl/Glassdoor Community dates are relative and converted to approximate months.
- No data separates CL8, CL9 and CL10 difficulty.

## Sources

1. [Accenture Careers – Journey to Accenture FAQ (India)](https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture)
2. [Accenture Careers – Journey to Accenture FAQ (US)](https://www.accenture.com/us-en/careers/explore-careers/area-of-interest/journey-to-accenture)
3. [Glassdoor – Accenture AI Engineer interview questions](https://www.glassdoor.com/Interview/Accenture-AI-Engineer-Interview-Questions-EI_IE4138.0,9_KO10,21.htm)
4. [Glassdoor India – Accenture AI/ML Engineer interview questions](https://www.glassdoor.co.in/Interview/Accenture-AI-ML-Engineer-Interview-Questions-EI_IE4138.0,9_KO10,24.htm)
5. [Glassdoor – Accenture AI/ML Engineer interview questions (US)](https://www.glassdoor.com/Interview/Accenture-AI-ML-Engineer-Interview-Questions-EI_IE4138.0,9_KO10,24.htm)
6. [Fishbowl – Databricks role, 5–7 YOE HackerRank](https://www.fishbowlapp.com/post/hias-part-of-the-screening-process-for-accenture-i-received-a-hackerrank-assessment-for-a-databricks-role-requiring-5-7)
7. [Glassdoor Community – Spring Boot 3 YOE HackerRank](https://www.glassdoor.com.au/Community/interview-experience/hi-i-received-a-hackerrank-assessment-from-accenture-for-the-custom-software-engineer-spring-boot-role-with-3-years-experience)
8. [Fishbowl – Backend 4–5 YOE HackerRank](https://www.fishbowlapp.com/post/hi-folks-i-received-a-hackerrank-assessment-for-a-backend-role-at-accenture-45-yoe-has-anyone-taken-it-recently-would-love)
9. [Glassdoor India – Backend 4–5 YOE (mirror)](https://www.glassdoor.co.in/Community/accenture-confessions/hi-folks-i-received-a-hackerrank-assessment-for-a-backend-role-at-accenture-45-yoe-has-anyone-taken-it-recently-would-love)
10. [Fishbowl – Level 9 Spring Boot format](https://www.fishbowlapp.com/post/what-is-the-format-of-accenture-online-assessment-for-level-9-spring-boot-developer-role-i-got-hackerrank-assessment)
11. [InterviewFox – Accenture HackerRank questions 2026](https://interviewfox.ai/interview-questions/accenture-hackerrank/) (low confidence)
12. [GeeksforGeeks – LLM Operations Engineer (Experienced)](https://www.geeksforgeeks.org/interview-experiences/accenture-final-interview-experience-for-llm-operations-engineer-experienced-selected/)
13. [GeeksforGeeks – Accenture Software Engineer](https://www.geeksforgeeks.org/interview-experiences/accenture-interview-experience-1/)
14. [Glassdoor – Accenture Python Developer review, Hyderabad, May 2025](https://www.glassdoor.com.mx/Entrevista/Accenture-Entrevista-E4138-RVW97354753.htm)
15. Naukri Code360 campus write-ups (freshers only): [Oct 2025](https://www.naukri.com/code360/interview-experiences/accenture-solutions-private-limited/accenture-interview-experience-on-campus-oct-2025), [Oct 2023](https://www.naukri.com/code360/interview-experiences/accenture/accenture-interview-experience-on-campus-oct-2023), [Sep 2023](https://www.naukri.com/code360/interview-experiences/accenture/accenture-interview-experience-by-atharva-kulkarni-on-campus-sep-2023), [Oct 2021](https://www.naukri.com/code360/interview-experiences/accenture-solutions-private-limited/accenture-interview-experience-by-shivansh-jaitly-on-campus-oct-2021-1448)

---

# Part 2 — Practice question bank

## 2.0 Read this first: what is "actual" and what isn't

I went back through every source for verbatim questions. Here is the honest picture:

| Category | What exists publicly | Where it is in this doc | Label |
|---|---|---|---|
| Exact HackerRank coding problems | 4 problems with statements/examples, all from **one low-confidence source** (InterviewFox, Java full-stack GenAI track, not India-specific) | §2.1 | 🟠 **Reported** |
| HackerRank task types without statements | SQL join, sliding window, comparator sort, CRUD API, PySpark, "Python block" | §2.2 → practice equivalents | 🟡 **Type reported, question modelled** |
| Interview-round questions | Several verbatim/near-verbatim questions from Glassdoor and GfG (AI Engineer, AI/ML Engineer, LLMOps, Python Dev) | §2.3 | 🟢 **Actual (interview rounds)** |
| HackerRank MCQs | **No verbatim MCQ from any Accenture assessment is published.** Even InterviewFox only lists categories | §2.4 | 🔵 **Practice — written by me to match reported topics** |
| Coding/SQL/pandas/FastAPI sets | Not published | §2.5–2.8 | 🔵 **Practice — modelled on reported topics** |

Every solution in this part was **run and tested** (Python 3.13, pandas, SQLite 3.45, FastAPI 0.142 / Pydantic 2.13). The runnable files sit next to this document:

```bash
uv run python accenture_practice_solutions.py   # 20+ problems, all asserts
uv run --with pandas python sql_check.py         # SQL + pandas answers
uv run --with "fastapi[standard]" python crud_app.py   # CRUD build task + tests
```

**How to use it:** attempt each problem with a timer *before* opening the solution. In HackerRank, you'll usually implement a function stub and hidden test cases call it — so practise writing clean functions, not `input()` parsing. (If a problem gives you raw STDIN, read with `sys.stdin.read().split()`.)

---

## 2.1 Exact coding problems reported by candidates

🟠 Source for all four: [InterviewFox, 15 Sep 2026](https://interviewfox.ai/interview-questions/accenture-hackerrank/) — Custom Software Engineer, Java Full-Stack GenAI track. Problem 1 and 2 were said to be the two problems in one ~45-minute coding block. Statements are as reported; where the source left something unspecified I flag it as an **assumption**.

### A1. Minimum CPU Cores — *intervals / sweep line* · Medium

> "A list of processes, each with a start time and an end time … find the minimum number of CPU cores needed so no two processes ran at the same time." **"The end times were inclusive, so a process ending at time 3 and another starting at time 3 still overlapped."**

**Restated:** return the maximum number of processes active at any single instant, with closed intervals `[start, end]`.

| Input | Output | Why |
|---|---|---|
| `[(0,3), (3,5), (2,6)]` | `3` | At t=3 all three are active (inclusive end) |
| `[(1,2), (3,4), (5,6)]` | `1` | No overlap |
| `[(1,2), (2,3)]` | `2` | Touching = overlapping here |
| `[(1,10), (2,3), (4,5), (6,7)]` | `2` | Long job + one short job at a time |
| `[]` | `0` | Edge case |

**The trap:** most people know LeetCode "Meeting Rooms II", which uses *half-open* intervals (touching meetings don't clash). Here they do. If you copy that solution unchanged, the `[(1,2),(2,3)]`-style hidden cases fail.

<details><summary>Solution (two approaches) — O(N log N) time, O(N) space</summary>

```python
from __future__ import annotations

import heapq
from collections.abc import Sequence


def min_cpu_cores(processes: Sequence[tuple[int, int]]) -> int:
    """Sweep line. Inclusive end -> the core is freed at end + 1."""
    events: list[tuple[int, int]] = []
    for start, end in processes:
        events.append((start, +1))
        events.append((end + 1, -1))
    events.sort()  # at equal time (-1) sorts before (+1): free before allocate
    running = peak = 0
    for _, delta in events:
        running += delta
        peak = max(peak, running)
    return peak


def min_cpu_cores_heap(processes: Sequence[tuple[int, int]]) -> int:
    """Sort by start; min-heap holds end times of busy cores."""
    ends: list[int] = []
    for start, end in sorted(processes):
        if ends and ends[0] < start:      # STRICT <, because end is inclusive
            heapq.heapreplace(ends, end)  # reuse that core
        else:
            heapq.heappush(ends, end)     # need a new core
    return len(ends)
```

**Why `end + 1`:** converting closed intervals to half-open `[start, end+1)` lets you reuse the standard sweep. This only works for integer times — for float times, sort with starts before ends at equal timestamps instead: `events.sort(key=lambda e: (e[0], -e[1]))` using the raw `end`.
</details>

### A2. Password Sanitizer — *strings* · Easy

> "A single line of space-separated passwords … return the valid ones, also space-separated and in the same order. A password passed if it had **at least 5 characters**, was **not made up only of letters**, and was **not made up only of digits**."

| Input | Output |
|---|---|
| `"abc123 abcd 123456 Passw0rd abcdef"` | `"abc123 Passw0rd"` |
| `"a!b@c# 12345 hello"` | `"a!b@c#"` |
| `""` | `""` |

**Assumptions to check against the real statement:** (1) symbol-only passwords like `"!!!!!"` count as valid (not all letters, not all digits); (2) empty result → empty string (some versions want `"NONE"` or `-1` — read the output spec); (3) multiple spaces between tokens — `str.split()` with no argument handles that.

<details><summary>Solution — O(T) time, T = total characters</summary>

```python
MIN_PASSWORD_LEN = 5


def sanitize_passwords(line: str) -> str:
    valid = [
        p for p in line.split()
        if len(p) >= MIN_PASSWORD_LEN and not p.isalpha() and not p.isdigit()
    ]
    return " ".join(valid)
```

**Gotcha:** `str.isalpha()` / `isdigit()` are Unicode-aware (`"é".isalpha()` is `True`, `"²".isdigit()` is `True`). If the spec says "letters A–Z", use `p.isascii() and p.isalpha()` or a regex like `re.fullmatch(r"[A-Za-z]+", p)`.
</details>

### A3. Desired Array — *math / arrays* · Medium

> "Return the sum of the **k smallest positive integers that none of the array's elements divide**." Example: `k = 4, arr = [2,3,4,5,6]` → qualifying numbers `1, 7, 11, 13` → **32**.

| k | arr | Output | Numbers |
|---|---|---|---|
| 4 | `[2,3,4,5,6]` | `32` | 1, 7, 11, 13 |
| 3 | `[2]` | `9` | 1, 3, 5 |
| 2 | `[4,6]` | `3` | 1, 2 |

**Edge cases to raise/handle:** `1` in `arr` → no number qualifies (infinite loop if you don't guard); duplicates in `arr`; large `k`.

<details><summary>Solution — prune divisors, then scan</summary>

```python
from collections.abc import Sequence


def desired_array_sum(k: int, arr: Sequence[int]) -> int:
    divisors = sorted(set(arr))
    if 1 in divisors:
        raise ValueError("1 divides everything - no valid number exists")
    # 4 and 6 add nothing if 2 is present: keep only "primitive" divisors
    reduced: list[int] = []
    for d in divisors:
        if all(d % r for r in reduced):
            reduced.append(d)
    total = found = 0
    candidate = 1
    while found < k:
        if all(candidate % d for d in reduced):
            total += candidate
            found += 1
        candidate += 1
    return total
```

**Performance note:** pruning `[2,3,4,5,6]` → `[2,3,5]` cuts work per candidate. Worst case is still O(range × |reduced|); that's fine for typical HackerRank limits. Mention the inclusion–exclusion + binary search approach if asked for large `k`.
</details>

### A4. Majority Element — *arrays / Boyer–Moore* · Easy

> Find the value that appears **more than half** the time. Example `[2,2,1,1,1,2,2]` → `2`. Expected O(n) time, O(1) space.

<details><summary>Solution</summary>

```python
def majority_element(nums: Sequence[int]) -> int:
    candidate, count = 0, 0
    for n in nums:
        if count == 0:
            candidate = n
        count += 1 if n == candidate else -1
    return candidate
```

If the statement does **not** guarantee a majority exists, add a second pass: `return candidate if nums.count(candidate) > len(nums) // 2 else -1`. `Counter(nums).most_common(1)` is acceptable (O(n) space) if the problem doesn't demand O(1) space.
</details>

---

## 2.2 Reported task types without published statements → practice equivalents

🟡 These task *types* were reported; the actual statements were not published. Practise the matching items:

| Reported task type | Reported where | Practise |
|---|---|---|
| "Python block: strings, arrays, dictionaries, tricky OOP + basic SQL" | InterviewFox (low) | §2.5 B1–B17, §2.6 |
| "Backend sliding window" | InterviewFox (low) | §2.5 B4, B5, B20 |
| "Java comparator sort" | Glassdoor Spring Boot 3 YOE (medium) | §2.5 B6, B7 (Python `key=` equivalent) |
| "CRUD operations" build task | Glassdoor Spring Boot (medium), Fishbowl CL9 | §2.8 FastAPI CRUD |
| "SQL join query"; "medium SQL with ranks and window functions" | InterviewFox (low) | §2.6 |
| "pyspark/aws/coding/python" | Fishbowl FastAPI dev (medium-low) | §2.7 pandas (same mental model as PySpark DataFrames) |
| "2 coding problems on arrays and strings (one involved list comprehension)" | Glassdoor AI/ML Pune, Sep 2026 — **interview round** | §2.5 B1–B3, B10–B13 |

---

## 2.3 Actual questions reported from Accenture AI/ML interview rounds

🟢 These were really asked — but in the **Level 1 / Final interviews**, not confirmed in HackerRank. They're your best evidence for what MCQs (if any) would cover, and you'll need them in the next round anyway. Answer pointers are mine; keep answers to 60–90 seconds.

**Glassdoor — AI Engineer, Chennai, Jun 2026**
1. *Difference between classification and regression?* → Discrete class label vs continuous value; different losses (cross-entropy vs MSE/MAE) and metrics. Logistic regression is a classifier despite its name.
2. *Evaluation metrics ("evaluation matrix")?* → Classification: confusion matrix, accuracy, precision, recall, F1, ROC-AUC, PR-AUC (prefer PR-AUC on imbalanced data). Regression: MAE, RMSE, R². LLM apps: groundedness/faithfulness, answer relevance, context precision/recall, latency, cost per request.

**Glassdoor — AI/ML Engineer, Pune, Sep 2026**
3. *Python fundamentals + FastAPI basics* → path vs query params, Pydantic request/response models, `Depends` for DI, async vs sync endpoints, status codes, validation errors (422).
4. *Two coding problems on arrays and strings, one involving list comprehension* → §2.5.
5. *Docker / Kubernetes (probes)* → liveness (restart if dead) vs readiness (remove from load balancer until ready) vs startup probe (for slow model loading — relevant for LLM/embedding services).
6. *Prompt engineering → guardrails → evaluation → MCP servers* → system prompts, few-shot, structured output (JSON schema); input/output guardrails (PII, prompt-injection, topic filters, schema validation); offline eval sets + LLM-as-judge + online metrics; MCP as a standard client–server protocol to expose tools/resources/prompts to LLM apps.
7. *Scenario: LLM costs suddenly spike — what do you do?* → Observe first (per-route token usage, prompt length, retries, loops in agents); then fix: prompt caching, response caching, smaller/cheaper model routing, trimming context/RAG top-k, max-token caps, batching, rate limits and budgets/alerts.

**Glassdoor — AI/ML Engineer, Pune, Feb 2026**
8. *Azure AI services / Azure ML* → Azure OpenAI (deployments, quotas/TPM), Azure AI Search (hybrid + vector search for RAG), Azure ML (workspaces, compute, model registry, managed online endpoints), Key Vault for secrets, Managed Identity.
9. *RAG* → ingest → chunk → embed → index → retrieve (hybrid + rerank) → augment prompt → generate with citations → evaluate.
10. *MLOps* → versioned data/models, experiment tracking, CI/CD for models, registry, deployment strategies (canary/shadow), monitoring drift and quality.
11. *Transfer learning* → reuse a pre-trained model's representations; freeze-and-train-head vs full fine-tune vs parameter-efficient (LoRA).
12. *What is a vector embedding?* → dense fixed-length vector from a model where semantic similarity ≈ geometric closeness (cosine/dot product).

**GeeksforGeeks — LLM Operations Engineer (Experienced), Dec 2025**
13. *Explain RAG internals step by step.* (see 9)
14. *What exactly is stored in a vector DB?* → vectors + IDs + metadata (source, chunk text or pointer, timestamps, ACL tags) + an ANN index (HNSW/IVF).
15. *LangChain vs CrewAI?* → LangChain: general LLM app/tooling framework (LangGraph for stateful agent graphs); CrewAI: role-based multi-agent orchestration ("crew" of agents with tasks).
16. *Running agents in parallel* → fan-out/fan-in (LangGraph parallel branches, `asyncio.gather`), shared state and reducers, timeouts and partial failure handling.
17. *Transformers* → self-attention, multi-head attention, positional encoding, encoder vs decoder vs encoder–decoder.
18. *MCP* → host/client/server; servers expose tools, resources, prompts; transports stdio and streamable HTTP.
19. *Python `__init__`, OOP, inheritance* → §2.5 B15–B17 and MCQs Q4, Q13.
20. *REST: PUT vs PATCH* → PUT replaces the full resource (idempotent); PATCH applies a partial update. See §2.8.

**Glassdoor — Python Developer, Hyderabad, May 2025 (adjacent)**
21. Data structures, OOP, libraries, **decorators, MRO, generators**, pandas, functions, **`*args`/`**kwargs`**, **`collections.namedtuple`**, lambdas, exceptions → covered by MCQs Q1–Q13 and §2.5.

---

## 2.4 Practice MCQs (36)

🔵 **Not actual Accenture questions** — no verbatim MCQ has been published. I wrote these to match the reported topic areas (Python, SQL, ML, GenAI). All Python outputs were executed to confirm the answers.

### Python (Q1–Q13)

**Q1.**
```python
def f(x, acc=[]):
    acc.append(x)
    return acc
f(1)
print(f(2))
```
A) `[2]` B) `[1, 2]` C) `[[1], 2]` D) Error
<details><summary>Answer</summary>**B** — default arguments are evaluated once at definition time; the same list is reused. Use `acc: list[int] | None = None`.</details>

**Q2.**
```python
a = [1, 2, 3]; b = a; b += [4]
t = (1, 2);    u = t; u += (3,)
print(a, t)
```
A) `[1,2,3] (1,2)` B) `[1,2,3,4] (1,2,3)` C) `[1,2,3,4] (1,2)` D) `[1,2,3] (1,2,3)`
<details><summary>Answer</summary>**C** — `+=` mutates a list in place (shared reference) but creates a new tuple.</details>

**Q3.** `print([i * i for i in range(5) if i % 2])`
A) `[0, 4, 16]` B) `[1, 9]` C) `[1, 4, 9, 16]` D) `[0, 1, 4, 9, 16]`
<details><summary>Answer</summary>**B** — `i % 2` is truthy for odd `i` (1, 3).</details>

**Q4.**
```python
class A:
    def who(self): return "A"
class B(A):
    def who(self): return "B"
class C(A):
    def who(self): return "C"
class D(B, C): pass
print(D().who(), [k.__name__ for k in D.__mro__])
```
A) `A [D,A,B,C,object]` B) `B [D,B,C,A,object]` C) `C [D,C,B,A,object]` D) TypeError
<details><summary>Answer</summary>**B** — C3 linearisation: D → B → C → A → object.</details>

**Q5.** `g = (x for x in range(3)); print(list(g), list(g))`
A) `[0,1,2] [0,1,2]` B) `[0,1,2] []` C) `[] []` D) Error
<details><summary>Answer</summary>**B** — generators are single-pass iterators.</details>

**Q6.** `[1] == [1]` and `[1] is [1]` evaluate to:
A) True, True B) True, False C) False, False D) False, True
<details><summary>Answer</summary>**B** — `==` compares values; `is` compares identity (two distinct objects).</details>

**Q7.**
```python
import copy
o = [[1], [2]]; s = copy.copy(o)
s[0].append(9); s.append([3])
print(o)
```
A) `[[1],[2]]` B) `[[1,9],[2]]` C) `[[1,9],[2],[3]]` D) `[[1],[2],[3]]`
<details><summary>Answer</summary>**B** — shallow copy: new outer list, shared inner lists. Use `copy.deepcopy` for full independence.</details>

**Q8.** `def h(a, *args, **kw): return a, args, kw` — `h(1, 2, 3, x=4)` returns:
A) `(1, [2,3], {'x':4})` B) `(1, (2,3), {'x':4})` C) `((1,2,3), {'x':4})` D) TypeError
<details><summary>Answer</summary>**B** — `*args` collects a **tuple**, `**kwargs` a dict.</details>

**Q9.** `sorted(['b','A','a','B'], key=str.lower)` returns:
A) `['A','B','a','b']` B) `['A','a','b','B']` C) `['a','A','b','B']` D) `['A','a','B','b']`
<details><summary>Answer</summary>**B** — `'A'` and `'a'` tie on key `'a'`; sort is **stable**, so original relative order is kept (`'A'` before `'a'`, `'b'` before `'B'`).</details>

**Q10.** `-7 // 2` and `-7 % 3` are:
A) `-3, -1` B) `-4, 2` C) `-3, 2` D) `-4, -1`
<details><summary>Answer</summary>**B** — floor division rounds toward −∞; the result of `%` takes the divisor's sign.</details>

**Q11.** Average time complexity of `x in some_set` vs `x in some_list`:
A) O(1), O(1) B) O(log n), O(n) C) O(1), O(n) D) O(n), O(n)
<details><summary>Answer</summary>**C** — hash lookup vs linear scan. Common fix in "too slow" hidden test cases.</details>

**Q12.** In the default (GIL) CPython build, the best way to speed up a **CPU-bound** pure-Python task across cores is:
A) `threading` B) `asyncio` C) `multiprocessing` / `ProcessPoolExecutor` D) more `await`s
<details><summary>Answer</summary>**C** — threads and asyncio help I/O-bound work (e.g. concurrent LLM API calls). Python 3.13+ has an optional free-threaded build, but it isn't the default.</details>

**Q13.** Why use `functools.wraps` inside a decorator?
A) To make the decorator faster B) To preserve the wrapped function's `__name__`, `__doc__` etc. C) To allow the decorator to take arguments D) It's required for decorators to work
<details><summary>Answer</summary>**B**.</details>

### SQL (Q14–Q19)

**Q14.** Which clause filters **after** aggregation?
A) WHERE B) HAVING C) GROUP BY D) ON
<details><summary>Answer</summary>**B** — WHERE filters rows before grouping; HAVING filters groups.</details>

**Q15.** Column `c` has values `1, NULL, 3`. `COUNT(*)` and `COUNT(c)` return:
A) 3, 3 B) 2, 2 C) 3, 2 D) 2, 3
<details><summary>Answer</summary>**C** — `COUNT(col)` ignores NULLs.</details>

**Q16.** Salaries `100, 90, 90, 80` ordered DESC. For `80`, `RANK()` and `DENSE_RANK()` are:
A) 4, 3 B) 3, 3 C) 4, 4 D) 3, 4
<details><summary>Answer</summary>**A** — RANK leaves gaps after ties; DENSE_RANK doesn't. ROW_NUMBER would give 4 with arbitrary tie order.</details>

**Q17.** `SELECT * FROM departments d LEFT JOIN employees e ON e.dept_id = d.dept_id` — a department with no employees appears:
A) Not at all B) Once, with NULLs in the employee columns C) Once per employee table row D) Causes an error
<details><summary>Answer</summary>**B** — add `WHERE e.emp_id IS NULL` to get the anti-join.</details>

**Q18.** `SELECT * FROM t WHERE col = NULL` returns:
A) Rows where col is NULL B) No rows C) All rows D) Error
<details><summary>Answer</summary>**B** — comparisons with NULL yield UNKNOWN. Use `IS NULL`.</details>

**Q19.** Best way to get the top 3 earners **per department**:
A) `ORDER BY salary DESC LIMIT 3` B) `GROUP BY dept_id HAVING COUNT(*) <= 3` C) `DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)` then filter `<= 3` D) `MAX(salary)` per dept
<details><summary>Answer</summary>**C** (see §2.6 Q2).</details>

### ML fundamentals (Q20–Q25)

**Q20.** Fraud data is 1% positive. A model predicts "not fraud" for everything. Its accuracy and recall are:
A) 99%, 99% B) 99%, 0% C) 1%, 100% D) 50%, 50%
<details><summary>Answer</summary>**B** — why accuracy is misleading on imbalanced data; use recall, precision, F1, PR-AUC.</details>

**Q21.** Training accuracy 99%, validation accuracy 70%. Most likely:
A) Underfitting B) Overfitting C) Data is perfect D) Learning rate too low
<details><summary>Answer</summary>**B** — fix with regularisation, more data, simpler model, early stopping, augmentation.</details>

**Q22.** Predicting house price from features is:
A) Classification B) Regression C) Clustering D) Reinforcement learning
<details><summary>Answer</summary>**B**.</details>

**Q23.** Which is **data leakage**?
A) Using k-fold CV B) Fitting a scaler on the full dataset before the train/test split C) Stratified sampling D) Dropping duplicate rows
<details><summary>Answer</summary>**B** — test-set statistics leak into training. Fit transforms on train only (use a `Pipeline`).</details>

**Q24.** Precision is:
A) TP / (TP + FN) B) TP / (TP + FP) C) (TP + TN) / total D) TN / (TN + FP)
<details><summary>Answer</summary>**B** — A is recall, D is specificity.</details>

**Q25.** Main purpose of k-fold cross-validation:
A) Speed up training B) Get a more reliable estimate of generalisation performance C) Increase training data D) Remove outliers
<details><summary>Answer</summary>**B**.</details>

### GenAI / LLM / RAG (Q26–Q36)

**Q26.** Setting `temperature` close to 0 mainly:
A) Shortens responses B) Makes token selection more deterministic C) Lowers cost per token D) Increases the context window
<details><summary>Answer</summary>**B** — note: not a hard guarantee of identical outputs across runs on every provider.</details>

**Q27.** Cosine similarity of vectors `[1, 0]` and `[0, 1]` is:
A) 1 B) 0 C) −1 D) 0.5
<details><summary>Answer</summary>**B** — orthogonal.</details>

**Q28.** Why use **chunk overlap** in a RAG ingestion pipeline?
A) Reduce index size B) Keep meaning that spans chunk boundaries retrievable C) Speed up embedding D) Required by vector DBs
<details><summary>Answer</summary>**B** — trade-off: more overlap → more storage and duplicate hits. See §2.5 B18.</details>

**Q29.** Knowledge changes weekly and answers need source citations. Best first choice:
A) Fine-tune monthly B) RAG C) Larger model D) Higher temperature
<details><summary>Answer</summary>**B** — fine-tuning changes behaviour/format/style; RAG supplies fresh, attributable knowledge.</details>

**Q30.** Standard self-attention cost grows with sequence length *n* as:
A) O(n) B) O(n log n) C) O(n²) D) O(1)
<details><summary>Answer</summary>**C** — why long contexts are expensive.</details>

**Q31.** HNSW in a vector database is:
A) An embedding model B) A graph-based approximate nearest neighbour index C) A compression codec D) A reranker
<details><summary>Answer</summary>**B** — trades a little recall for big latency gains vs exact (flat) search.</details>

**Q32.** In RAG, a cross-encoder **reranker**:
A) Generates embeddings for the index B) Re-scores retrieved candidates by reading query and passage together C) Splits documents D) Replaces the LLM
<details><summary>Answer</summary>**B** — higher precision, more latency; apply only to the top-N candidates.</details>

**Q33.** Best defence against **indirect prompt injection** via retrieved documents:
A) Higher temperature B) Treat retrieved text as untrusted data, least-privilege tools, validate outputs/tool calls, human approval for risky actions C) Longer system prompt saying "ignore injections" D) Bigger model
<details><summary>Answer</summary>**B** — defence in depth; prompt wording alone is not a control.</details>

**Q34.** Context-window limits and API pricing are measured in:
A) Characters B) Words C) Tokens D) Sentences
<details><summary>Answer</summary>**C**.</details>

**Q35.** MCP (Model Context Protocol) is:
A) A vector DB B) An open protocol standardising how LLM apps connect to external tools/data via client–server C) A fine-tuning method D) A tokenizer
<details><summary>Answer</summary>**B**.</details>

**Q36.** Most effective way to reduce hallucinations in an enterprise Q&A bot:
A) Raise max tokens B) Ground answers in retrieved context, require citations, allow "I don't know", evaluate faithfulness C) Use only zero-shot prompts D) Increase temperature
<details><summary>Answer</summary>**B**.</details>

---

## 2.5 Practice coding set (20 problems)

🔵 Modelled on reported topics (strings, arrays, dicts, sorting, intervals, sliding window, OOP) plus two AI-flavoured tasks. Full solutions + tests: `accenture_practice_solutions.py`. Target: **≤ 20 min each** for Easy, **≤ 30 min** for Medium.

| # | Problem | Topic | Level | Example → expected |
|---|---|---|---|---|
| B1 | First non-repeating character index (−1 if none) | String, dict | Easy | `"loveleetcode"` → `2` |
| B2 | Group anagrams (keep first-seen order) | Dict, sorting | Easy | `["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"],["tan","nat"],["bat"]]` |
| B3 | Merge overlapping closed intervals | Intervals | Medium | `[(1,3),(2,6),(8,10),(15,18)]` → `[(1,6),(8,10),(15,18)]`; `[(1,4),(4,5)]` → `[(1,5)]` |
| B4 | Longest substring without repeating chars | Sliding window | Medium | `"abcabcbb"` → `3`; `"abba"` → `2` |
| B5 | Max sum of a size-k subarray | Sliding window | Easy | `[2,1,5,1,3,2], k=3` → `9` |
| B6 | Top-k frequent words (freq desc, then alphabetical) | Dict, custom sort | Medium | `["b","a","c","a","b"], k=2` → `["a","b"]` |
| B7 | Sort employees: dept asc, salary desc, name asc | Comparator sort | Easy | see test file |
| B8 | Count pairs (i<j) summing to target | Dict | Medium | `[1,5,7,-1,5], 6` → `3`; `[1,1,1,1], 2` → `6` |
| B9 | Balanced brackets | Stack | Easy | `"{[()]}"` → `True`; `"([)]"` → `False` |
| B10 | Run-length compression (return original if not shorter) | String | Easy | `"aabcccccaaa"` → `"a2b1c5a3"` |
| B11 | Product of array except self (no division) | Arrays, prefix/suffix | Medium | `[1,2,3,4]` → `[24,12,8,6]`; `[0,1,2]` → `[2,0,0]` |
| B12 | Second largest **distinct** value (None if absent) | Arrays | Easy | `[10,5,10,8]` → `8`; `[7,7]` → `None` |
| B13 | Move zeros to end in place, keep order | Arrays, two pointers | Easy | `[0,1,0,3,12]` → `[1,3,12,0,0]` |
| B14 | Error count per service from log lines (sorted count desc, name asc; skip malformed) | Parsing, regex, dict | Medium | see test file |
| B15 | LRU cache class (`get`/`put`, O(1)) | OOP, `OrderedDict` | Medium | cap 2: put 1, put 2, get 1, put 3 → get 2 = −1 |
| B16 | Shape ABC → Rectangle, Square(Rectangle), Circle; sortable by area | OOP, ABC, dunder | Easy | `sorted([Circle(1), Square(2), Rectangle(1,2)])` → Rectangle, Circle, Square |
| B17 | BankAccount with validation + custom `InsufficientFundsError` | OOP, exceptions, `@property` | Easy | deposit 50, withdraw 30 from 100 → 120 |
| B18 | Word chunker with overlap (RAG chunking) | AI-flavoured, strings | Medium | `"a b c d e f g", size=3, overlap=1` → `["a b c","c d e","e f g"]` |
| B19 | Top-k documents by cosine similarity (pure Python) | AI-flavoured, math, heap | Medium | query `[1,0.1]`, docs d1 `[1,0]`, d2 `[.7,.7]`, d3 `[0,1]`, k=2 → `["d1","d2"]` |
| B20 | Sliding-window rate limiter: ≤ `limit` requests per user per `window` s | Dict + deque | Medium | `[(1,u),(2,u),(3,u),(11,u),(3,v)]`, 2, 10 → `[T,T,F,T,T]` |

<details><summary>Selected solutions (full set in the .py file)</summary>

```python
from __future__ import annotations

import heapq
import math
from collections import Counter, OrderedDict, defaultdict, deque
from collections.abc import Sequence


# B4 - sliding window with last-seen index
def longest_unique_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if last_seen.get(ch, -1) >= left:   # only jump if the repeat is inside the window
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


# B6 - sort key tuple instead of a comparator
def top_k_frequent_words(words: Sequence[str], k: int) -> list[str]:
    counts = Counter(words)
    return sorted(counts, key=lambda w: (-counts[w], w))[:k]


# B7 - Java Comparator equivalent: negate numeric fields for descending
def sort_employees(rows: Sequence[tuple[str, str, int]]) -> list[tuple[str, str, int]]:
    return sorted(rows, key=lambda r: (r[1], -r[2], r[0]))


# B8 - one pass, count complements already seen
def count_pairs_with_sum(nums: Sequence[int], target: int) -> int:
    seen: Counter[int] = Counter()
    pairs = 0
    for n in nums:
        pairs += seen[target - n]
        seen[n] += 1
    return pairs


# B15 - LRU cache
class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._data: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self._data:
            return -1
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: int, value: int) -> None:
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self._capacity:
            self._data.popitem(last=False)   # evict least recently used


# B18 - RAG chunker
def chunk_words(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("need chunk_size > 0 and 0 <= overlap < chunk_size")
    words = text.split()
    step = chunk_size - overlap
    chunks: list[str] = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_size]))
        if start + chunk_size >= len(words):
            break   # avoid a trailing chunk fully contained in the previous one
    return chunks


# B19 - brute-force retrieval (what a vector DB does with an ANN index instead)
def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return 0.0 if norm == 0 else dot / norm


def top_k_similar(query: Sequence[float], docs: dict[str, Sequence[float]], k: int) -> list[str]:
    scored = ((cosine(query, vec), doc_id) for doc_id, vec in docs.items())
    return [doc_id for _, doc_id in heapq.nlargest(k, scored)]


# B20 - per-user sliding-window rate limiter
def rate_limit(requests: Sequence[tuple[int, str]], limit: int, window: int) -> list[bool]:
    history: dict[str, deque[int]] = defaultdict(deque)
    decisions: list[bool] = []
    for ts, user in requests:
        q = history[user]
        while q and q[0] <= ts - window:
            q.popleft()
        allowed = len(q) < limit
        if allowed:
            q.append(ts)
        decisions.append(allowed)
    return decisions
```
</details>

**Common hidden-test-case failures to check before submitting:** empty input; single element; all duplicates; negative numbers; inclusive vs exclusive bounds; ties in sorting; very large input (avoid O(n²) when n ≥ 10⁵ — use a set/dict/heap).

---

## 2.6 SQL practice set (9 queries)

🔵 Modelled on reported "SQL join" and "medium SQL with ranks and window functions". Outputs below are real results from SQLite (`sql_check.py`); the same SQL runs on PostgreSQL.

**Schema + data**
```sql
CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER,
                        manager_id INTEGER, salary INTEGER, hire_date TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, emp_id INTEGER, amount INTEGER, order_date TEXT);

INSERT INTO departments VALUES (1,'Engineering'),(2,'Sales'),(3,'HR'),(4,'Legal');
INSERT INTO employees VALUES
 (1,'Asha',1,NULL,200000,'2019-01-10'), (2,'Ravi',1,1,150000,'2020-03-01'),
 (3,'Meera',1,1,150000,'2021-07-15'),  (4,'Karan',1,2,160000,'2022-02-01'),
 (5,'Neha',2,1,90000,'2020-05-20'),    (6,'Vikram',2,5,95000,'2023-01-05'),
 (7,'Pooja',3,1,70000,'2021-11-11'),   (8,'Ravi',1,1,150000,'2020-03-01');
INSERT INTO orders VALUES
 (1,5,1000,'2026-01-05'),(2,5,1500,'2026-01-20'),(3,6,700,'2026-01-25'),
 (4,6,1200,'2026-02-02'),(5,5,300,'2026-02-10');
```

| # | Task | Expected result |
|---|---|---|
| Q1 | Second-highest **distinct** salary | `160000` |
| Q2 | Top 2 earners per department (ties share a rank) | Eng: Asha 200000, Karan 160000 · HR: Pooja 70000 · Sales: Vikram 95000, Neha 90000 |
| Q3 | Employees earning more than their manager | Karan > Ravi · Vikram > Neha |
| Q4 | Departments with average salary > 100000 (with headcount) | Engineering, 162000, 5 |
| Q5 | Departments with no employees | Legal |
| Q6 | Running total of order amount per employee by date | emp 5: 1000, 2500, 2800 · emp 6: 700, 1900 |
| Q7 | Find duplicate employee rows (same name, dept, salary, hire_date) | Ravi, 1, 150000, 2020-03-01, count 2 |
| Q8 | Monthly sales and month-over-month change | 2026-01: 3200, NULL · 2026-02: 1500, −1700 |
| Q9 | ROW_NUMBER vs RANK vs DENSE_RANK in Engineering | Asha 1/1/1 · Karan 2/2/2 · the three 150000 rows: rn 3,4,5 / rank 3 / dense 3 |

<details><summary>Answers</summary>

```sql
-- Q1
SELECT MAX(salary) AS second_highest FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
-- Generalised Nth highest:
SELECT DISTINCT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees) t
WHERE rnk = 2;

-- Q2
SELECT dept_name, name, salary FROM (
  SELECT d.dept_name, e.name, e.salary,
         DENSE_RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rnk
  FROM employees e JOIN departments d ON d.dept_id = e.dept_id) t
WHERE rnk <= 2
ORDER BY dept_name, salary DESC, name;

-- Q3 (self join)
SELECT e.name AS employee, m.name AS manager
FROM employees e JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;

-- Q4
SELECT d.dept_name, ROUND(AVG(e.salary)) AS avg_salary, COUNT(*) AS headcount
FROM employees e JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_name
HAVING AVG(e.salary) > 100000;

-- Q5 (anti-join; NOT EXISTS is equivalent and often clearer)
SELECT d.dept_name FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
WHERE e.emp_id IS NULL;

-- Q6
SELECT emp_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY emp_id ORDER BY order_date
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders ORDER BY emp_id, order_date;

-- Q7
SELECT name, dept_id, salary, hire_date, COUNT(*) AS cnt
FROM employees
GROUP BY name, dept_id, salary, hire_date
HAVING COUNT(*) > 1;

-- Q8 (PostgreSQL: use to_char(order_date, 'YYYY-MM') or date_trunc('month', ...))
SELECT month, total, total - LAG(total) OVER (ORDER BY month) AS mom_change FROM (
  SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
  FROM orders GROUP BY month) t;

-- Q9
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
       RANK()       OVER (ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS drnk
FROM employees WHERE dept_id = 1;
```

**Gotchas:** Q2 — using ROW_NUMBER silently drops tied salaries; Q3 — INNER self-join excludes the CEO (NULL manager), which is what you want here; Q9 — ROW_NUMBER order among ties is arbitrary unless you add a tiebreaker (`ORDER BY salary DESC, emp_id`), and hidden tests may expect a deterministic order.
</details>

---

## 2.7 pandas practice set

🔵 Same data as §2.6 loaded into DataFrames `emp`, `dept`. Useful if the AI track swaps SQL for a data-manipulation task, and the same mental model applies to PySpark (`groupBy`, `join`, `Window.partitionBy`).

| # | Task | Expected |
|---|---|---|
| P1 | Avg salary and headcount per department name | Eng 162000/5 · HR 70000/1 · Sales 92500/2 |
| P2 | Top 2 earners per department (dense rank) | Same as SQL Q2 |
| P3 | Drop duplicate employee rows | 8 → 7 rows |

<details><summary>Answers</summary>

```python
df = emp.merge(dept, on="dept_id", how="left")

# P1 - named aggregation (current idiom)
summary = df.groupby("dept_name", as_index=False).agg(
    avg_salary=("salary", "mean"),
    headcount=("emp_id", "count"),
)

# P2
df["rnk"] = df.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
top2 = (
    df.loc[df["rnk"] <= 2, ["dept_name", "name", "salary"]]
      .sort_values(["dept_name", "salary", "name"], ascending=[True, False, True])
)

# P3
deduped = emp.drop_duplicates(subset=["name", "dept_id", "salary", "hire_date"])
```

PySpark equivalent of P2, for reference:
```python
from pyspark.sql import Window, functions as F
w = Window.partitionBy("dept_id").orderBy(F.col("salary").desc())
top2 = df.withColumn("rnk", F.dense_rank().over(w)).filter("rnk <= 2")
```
</details>

---

## 2.8 Hands-on "build" task: FastAPI CRUD

🔵 Python counterpart of the reported "Spring Boot CRUD operations" task, and FastAPI basics were asked in an Accenture AI/ML Pune interview (Sep 2026). Full tested solution: `crud_app.py`.

**Task (try in ≤ 40 min):** Build a `/documents` API with in-memory storage.
- `POST /documents` → 201, body `{title (1–200 chars), content (non-empty), tags: list[str] = []}`, returns object with auto-increment `id`.
- `GET /documents?tag=ai` → list, optional tag filter.
- `GET /documents/{id}` → 404 if missing.
- `PUT /documents/{id}` → full replace (omitted `tags` resets to `[]`).
- `PATCH /documents/{id}` → partial update (only fields sent change).
- `DELETE /documents/{id}` → 204; 404 if missing.
- Invalid body → 422.

<details><summary>Key parts of the solution</summary>

```python
class DocumentPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = None


Repo = Annotated[DocumentRepository, Depends(get_repo)]   # DI -> swap in a DB repo / test fake


@app.patch("/documents/{doc_id}", response_model=DocumentOut)
def patch_document(doc_id: int, body: DocumentPatch, repo: Repo) -> DocumentOut:
    current = _require(repo, doc_id)                        # 404 helper
    merged = current.model_copy(update=body.model_dump(exclude_unset=True))
    return repo.replace(doc_id, DocumentIn(**merged.model_dump(exclude={"id"})))
```

**Design points worth saying out loud (interview gold):**
- `exclude_unset=True` is what makes PATCH partial; PUT validates a full `DocumentIn`.
- Repository behind `Depends` keeps routes storage-agnostic and testable (override with `app.dependency_overrides`).
- Pydantic v2 APIs: `model_dump`, `model_copy` (v1's `.dict()`/`.copy()` are deprecated).
- Production gaps you'd mention: thread-safety of the in-memory dict, persistence, pagination, auth, idempotency keys for POST.
</details>

---

## 2.9 Two timed mock tests

Do these in a plain editor with **no autocomplete AI**, timer on, then run the test file.

**Mock 1 — 60 minutes (closest to the reported format)**
| Block | Items | Time |
|---|---|---|
| MCQ | Q1, Q4, Q7, Q10, Q15, Q16, Q20, Q23, Q28, Q29, Q31, Q33 | 12 min |
| Coding 1 | A1 Minimum CPU Cores | 20 min |
| Coding 2 | A2 Password Sanitizer + B6 Top-k words | 20 min |
| SQL | §2.6 Q2 + Q3 | 8 min |

**Mock 2 — 75 minutes (AI-track variant)**
| Block | Items | Time |
|---|---|---|
| MCQ | Q2, Q5, Q8, Q12, Q14, Q19, Q21, Q24, Q26, Q30, Q32, Q36 | 12 min |
| Coding 1 | B4 Longest unique substring | 15 min |
| Coding 2 | B18 Chunker + B19 Top-k cosine | 25 min |
| Build | §2.8 CRUD (POST/GET/PATCH only) | 23 min |

**Scoring yourself:** HackerRank grades per hidden test case, so after each mock, run the asserts in the `.py` file and count passes — a solution that's "basically right" but fails inclusive-bound or empty-input cases loses real marks.

---

*Integrity note:* Accenture's FAQ explicitly bans external AI tools during the assessment. Everything above is for preparation before you start the test.
