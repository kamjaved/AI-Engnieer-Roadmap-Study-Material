# Python Interview & HackerRank Question Bank for ~3 Years' Experience (TCS, Infosys, Accenture, Wipro, Deloitte, EY, Capgemini, HCLTech & Others)

For a 3-year Python candidate at Indian service and Big-4 firms, the questions that come up again and again are basic: list vs tuple, decorators, generators and comprehensions, OOP (`__init__`, `self`, inheritance), shallow vs deep copy, and easy coding tasks (Fibonacci, character frequency, reversing strings or words, sorting, flattening a nested list). The HackerRank online assessment (OA) adds 1–2 easy-to-medium problems plus Python and DBMS MCQs. Master those and you cover most of what candidates actually report.

> **My own attempts:** see [My Experience: Real Assessments I Attempted](#my-experience-real-assessments-i-attempted) at the end of this file (latest: Accenture AI Engineer, 10 Oct 2026).

## TL;DR
- **Most reported across companies:** list vs tuple (TCS, Wipro, Capgemini, Infosys); decorators (Accenture, Wipro, Infosys, Capgemini); Fibonacci (TCS, Capgemini, Wipro); and string or frequency programs (Accenture, Deloitte, Infosys, Capgemini). Generators, comprehensions, OOP/inheritance, shallow vs deep copy and `*args/**kwargs` come next.
- **The HackerRank OA format is small and predictable:** usually 2 coding problems in 45–110 minutes. Some firms add an MCQ block: Infosys reported 10 Python MCQs, 10 DBMS MCQs and 2 coding problems; Wipro reported a 40-question, 40-minute technical MCQ section. HackerRank's official Python (Basic) certification page specifies "a 1 hr 30 mins assessment" with "2 questions". HackerRank's blog says the test covers "strings, collections and iteration, modularity, objects, and types and classes". Candidates report tasks such as Shopping Cart, Multiset, Shape Classes and Dominant Cells.
- **How to prepare:** get the 45 items below to "write it cold in 10 minutes". Rehearse the output-prediction traps (mutable defaults, aliasing, `[[0]*3]*3`, late-binding closures, `finally` overriding `return`). Expect SQL and framework questions (Django/pandas/AWS) on top of Python at the 3-year level.

---

## Key Findings

**1. At 3 years, service-company interviews test fundamentals, not hard algorithms.**
- An Infosys hire with 3 years' experience (Technology Analyst) reported being asked to "write a program to sort the array", plus lambda, map/reduce/filter, interpreted vs compiled, class/objects, multiple inheritance and constructors. The certification round was 10 Python MCQs, 10 DBMS MCQs and 2 easy-medium coding problems. https://www.geeksforgeeks.org/infosys-interview-experience-2023-2/ \[1\]
- A TCS guide for 2–5 years' experience lists: zip two lists; list vs tuple and set vs dict; prime numbers in a range; Fibonacci; a multiplication table from user input. https://medium.com/@rana.akansha321/tcs-python-developer-interview-question-for-2023-87aab3426791 \[2\]
- Capgemini (Pune, 2025): "Fibonacci series or converting a nested list to a plain list", then list vs tuple, comprehensions, decorators, generators, Git merging and SQL. https://www.jointaro.com/interviews/companies/capgemini/experiences/python-developer-pune-march-3-2025-no-offer-positive-6ca61b4c/ \[3\]
- A Wipro automation candidate listed: sorting program, Fibonacci, break/continue/pass, `__init__`, `self`, multiple inheritance, range vs xrange, local vs global, file open/close. https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm \[4\]

**2. Decorators are the single most consistent "Python concept" question.**
- Accenture (Bengaluru, May 2026): "basic Python concepts such as decorators, along with SQL fundamentals". https://www.glassdoor.com/Interview/Accenture-Python-Developer-Interview-Questions-EI_IE4138.0,9_KO10,26.htm \[5\]
- Wipro: "Decorators, data structures and all basic things". https://www.glassdoor.com/Interview/Wipro-Python-Developer-Interview-Questions-EI_IE9936.0,5_KO6,22.htm \[6\]
- Infosys Senior Python: "shallow and deep copy decorators", plus "string related questions, decorators, libraries like pandas". https://www.glassdoor.com/Interview/Infosys-Senior-Python-Developer-Interview-Questions-EI_IE7927.0,7_KO8,31.htm \[7\]

**3. Coding asks are short and string- or list-heavy.**
- Accenture: "count the occurrence of characters in a string using HashMap". https://www.geeksforgeeks.org/interview-experiences/accenture-interview-experience-application-developer-full-time/ \[8\]
- Deloitte: "Merge two list based on some condition. Frequency count, easy sql joins". https://www.glassdoor.ca/Interview/Deloitte-Python-Developer-Interview-Questions-EI_IE2763.0,8_KO9,25.htm \[9\]
- Capgemini (Jan 2026): "two easy level python coding questions were asked on strings and loops". https://www.glassdoor.co.in/Interview/Capgemini-Python-Developer-Interview-Questions-EI_IE3803.0,9_KO10,26.htm \[10\]
- HCLTech is the outlier, reporting LeetCode-style "2sum and longest substring without repeating characters" plus a nested-list string-extraction task. https://www.glassdoor.com/Interview/HCLTech-Python-Developer-Interview-Questions-EI_IE553909.0,7_KO8,24.htm and https://www.glassdoor.com/Interview/python-developer-interview-questions-SRCH_KO0,16.htm \[11\]\[12\]

**4. HackerRank OA formats reported by candidates:**

| Company / test | Reported format | Source | Reliability |
|---|---|---|---|
| HackerRank Python (Basic) certification | "Solve 2 questions" in "a 1 hr 30 mins assessment" | https://www.hackerrank.com/skills-verification/python_basic | Official HackerRank page |
| HackerRank Problem Solving (Basic) certification | 2 problems, 90 min\[13\] | https://github.com/reebaseb/Hackerrank_ProblemSolvingBasic_Certificate_test-soltions | Candidate repo |
| Infosys (lateral, 3 yrs) | 10 Python MCQ + 10 DBMS MCQ + 2 coding (easy–medium) | https://www.geeksforgeeks.org/infosys-interview-experience-2023-2/ | Candidate\[1\] |
| Wipro | Technical MCQ: 40 questions / 40 min\[14\] | https://www.glassdoor.ca/Interview/Wipro-Python-Developer-Interview-Questions-EI_IE9936.0,5_KO6,22.htm | Candidate |
| Accenture (HackerRank, Feb 2026) | 2 coding problems, ~45 min, partial credit per test case\[15\] | https://interviewfox.ai/interview-questions/accenture-hackerrank/ | ⚠️ Marketing page for an AI "interview assist" tool; unverified |
| Deloitte | 2 coding + DSA MCQs, 50–60 min\[16\] | https://www.naukri.com/code360/interview-experiences/deloitte/deloitte-interview-experience-on-campus-mar-2025 | Candidate (campus) |
| EY GDS | 45 min coding + 15 min MCQ; or 2 problems in 110 min with a 24-hour window\[17\]\[18\] | https://www.naukri.com/code360/interview-experiences/ernst-young-ey/interview-experience-aug-2022-exp-0-2-years-2 ; https://www.naukri.com/code360/interview-experiences/ernst-young-ey/interview-experience-senior-software-developer-mar-2022-exp-0-2-years-2 | Candidate |
| IBM (product, HackerRank, 2026) | 2 coding problems, 60 min\[19\] | https://interviewfox.ai/interview-questions/ibm-hackerrank-test/ | ⚠️ Same marketing site |
| Cognizant (HackerRank) | 2–3 coding problems (e.g., sort and print alternate elements; GCD of an array) | https://www.geeksforgeeks.org/cognizant-interview-experience-set-2-campus/ | Candidate (campus, older)\[20\] |

**5. Self-reported difficulty is moderate, and the Glassdoor numbers conflict.**
- Glassdoor shows TCS Python Developer at 2.7/5, Capgemini at 3/5 and EY at 3.3/5.\[10\]\[21\]\[22\]
- For Accenture Python Developer, glassdoor.co.in shows 2.8/5 across 22 interviews while glassdoor.com shows 2.3/5 across 4.\[5\]\[23\] Treat these as rough signals, not measurements.
- Sources: https://www.glassdoor.com/Interview/TCS-Python-Developer-Interview-Questions-EI_IE3211746.0,3_KO4,20.htm ; https://www.glassdoor.co.in/Interview/Accenture-Python-Developer-Interview-Questions-EI_IE4138.0,9_KO10,26.htm

---

## How the Ranking Works

- **Rank** combines (a) the number of independent companies or candidate reports mentioning the topic and (b) how relevant it is to HackerRank OAs and 3-year technical rounds. Rank 1 is the highest priority.
- **Evidence labels:**
  - **[CR] Candidate-reported:** a named company, with a source URL.
  - **[PP] Popular practice:** HackerRank's certification tests, blog or practice tracks.
  - **[CT] Commonly asked theory:** standard trap or concept questions found across prep sources, not tied to one firm.
- **Difficulty:** Easy / Medium / Hard, judged for a 3-year candidate.

### Master Ranking Table

| Rank | Question | Category | Evidence | Companies / Source type | Difficulty |
|---|---|---|---|---|---|
| 1 | List vs tuple vs set vs dict | Theory | CR | TCS, Wipro, Capgemini, Infosys | Easy |
| 2 | Decorators (write one) | Theory + code | CR | Accenture, Wipro, Infosys, Capgemini | Medium |
| 3 | Fibonacci (series / nth / membership) | Coding | CR | TCS ×2, Capgemini, Wipro, Citadel | Easy |
| 4 | Character / element frequency | Coding | CR | Accenture, Deloitte | Easy |
| 5 | OOP: `__init__`, `self`, multiple inheritance, MRO | Theory + snippet | CR | Infosys, Wipro, EY | Medium |
| 6 | Generators, iterators, comprehensions | Theory + code | CR | Capgemini, Infosys, LTIMindtree | Medium |
| 7 | Reverse string / words / palindrome | Coding | CR + PP | LTIMindtree, HackerRank | Easy |
| 8 | Sort an array (without `sort`) | Coding | CR | Infosys, Wipro, Cognizant | Easy |
| 9 | Flatten nested list / extract strings | Coding | CR | Capgemini, HCLTech | Easy |
| 10 | Mutable default argument | Output prediction | CT + PP | HackerRank debugging challenge | Medium |
| 11 | Aliasing, shallow vs deep copy | Output prediction | CR | Infosys | Medium |
| 12 | `*args` / `**kwargs` (Average Function) | Theory + code | CR + PP | Accenture, HackerRank cert | Easy |
| 13 | lambda, map, filter, reduce | Theory + snippet | CR | Infosys | Easy |
| 14 | Prime numbers in a range | Coding | CR | TCS | Easy |
| 15 | Zip / merge two lists | Coding | CR | TCS, Deloitte | Easy |
| 16 | Scope: local/global, UnboundLocalError | Output prediction | CR | Wipro | Medium |
| 17 | Two Sum | Coding | CR | HCLTech | Easy |
| 18 | Longest substring without repeating chars | Coding | CR | HCLTech | Medium |
| 19 | Remove / find duplicates | Coding | CR | HackerRank (company OA), Deloitte | Easy |
| 20 | Anagram check / String Anagram | Coding | PP + CR | HackerRank PS cert, GfG | Easy |
| 21 | Memory management, GIL, multithreading | Theory | CR | TCS, Infosys, Deloitte | Medium |
| 22 | File handling: CSV / JSON | Theory + code | CR | EY ×2, Wipro | Easy |
| 23 | Quick-fire basics (pass/continue, range/xrange, interpreted) | Theory | CR | Wipro, Infosys, TCS | Easy |
| 24 | Maximum subarray (Kadane) | Coding | PP | HackerRank blog | Medium |
| 25 | Merge intervals / minimum CPU cores | Coding | PP + CR⚠️ | HackerRank blog, Accenture | Medium |
| 26 | Product of array except self | Coding | CR | EY | Medium |
| 27 | Password sanitizer | Coding | CR⚠️ | Accenture | Easy |
| 28 | Shape Classes + Shopping Cart | Coding (OOP) | PP | HackerRank Python (Basic) cert | Easy |
| 29 | Multiset implementation | Coding (OOP) | PP | HackerRank Python (Basic) cert | Easy |
| 30 | Dominant Cells | Coding (matrix) | PP | HackerRank Python (Basic) cert | Easy |
| 31 | Slicing outputs | Output prediction | CT | MCQ sections | Easy |
| 32 | `[[0]*3]*3` aliasing | Output prediction | CT | MCQ sections | Easy |
| 33 | `is` vs `==` | Output prediction | CT | Prep sources | Easy |
| 34 | Immutability: tuple, str, dict keys | Output prediction | CT | MCQ sections | Medium |
| 35 | Operator precedence and arithmetic MCQ | MCQ | CT | MCQ sections | Easy |
| 36 | Truthiness and implicit `None` | MCQ | CT | MCQ sections | Easy |
| 37 | try / except / else / finally | Output prediction | CT | Prep sources | Medium |
| 38 | Late-binding closures | Output prediction | CT | Prep sources | Medium |
| 39 | Comprehension / generator exhaustion | Output prediction | CT | Prep sources | Easy |
| 40 | Time complexity of built-ins | Complexity | CT | All rounds | Easy |
| 41 | Debug: HackerRank "Default Arguments" | Debugging | PP | HackerRank blog/practice | Medium |
| 42 | Balanced parentheses | Coding | CR | GfG candidate reports | Easy |
| 43 | GCD of array / decimal to binary | Coding | CR | Cognizant, LTIMindtree | Easy |
| 44 | Desired Array (k smallest non-divisible) | Coding | CR | Accenture OA | Medium |
| 45 | Count subsequences of equal elements | Coding | CR | Deloitte | Medium |

---

## Details — Section A: Coding Problems

### Rank 3 — Fibonacci (series, nth term, membership)
- **Category:** Coding / loops · **Difficulty:** Easy
- **Evidence [CR]:**
  - TCS "write a program for generate fibonacci series": https://medium.com/@rana.akansha321/tcs-python-developer-interview-question-for-2023-87aab3426791 \[2\]
  - TCS "determine whether N belongs to the Fibonacci sequence": https://www.naukri.com/code360/interview-experiences/tcs/interview-experience-system-engineer-jul-2022-exp-0-2-years \[24\]
  - Capgemini: https://www.jointaro.com/interviews/companies/capgemini/experiences/python-developer-pune-march-3-2025-no-offer-positive-6ca61b4c/
  - Wipro: https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm \[4\]
  - Citadel "return the nth fibonacci number… first two 1 and 1": https://www.glassdoor.com/Interview/python-developer-interview-questions-SRCH_KO0,16.htm \[12\]

```python
from math import isqrt

def fib_series(n: int) -> list[int]:
    """First n Fibonacci numbers starting 0, 1."""
    series: list[int] = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

def nth_fib(n: int) -> int:
    """1-indexed, fib(1) = fib(2) = 1 (Citadel wording)."""
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a

def is_fibonacci(n: int) -> bool:
    """n is Fibonacci iff 5n²+4 or 5n²−4 is a perfect square."""
    def is_square(x: int) -> bool:
        return x >= 0 and isqrt(x) ** 2 == x
    return n >= 0 and (is_square(5 * n * n + 4) or is_square(5 * n * n - 4))

print(fib_series(7))   # [0, 1, 1, 2, 3, 5, 8]
print(nth_fib(4))      # 3
print(is_fibonacci(21), is_fibonacci(22))  # True False
```
- **Explanation:** Tuple-swap iteration avoids the exponential cost of naive recursion. If asked for recursion, add `@functools.cache` and point out that it trades memory for speed.
- **Complexity:** series O(n) time, O(n) space · nth O(n) time, O(1) space · membership O(1) arithmetic (big-int aside).

### Rank 4 — Character / element frequency (and first non-repeating character)
- **Category:** Coding / dictionaries · **Difficulty:** Easy
- **Evidence [CR]:**
  - Accenture "count the occurrence of characters in a string using HashMap": https://www.geeksforgeeks.org/interview-experiences/accenture-interview-experience-application-developer-full-time/ \[8\]
  - Deloitte "Frequency count": https://www.glassdoor.ca/Interview/Deloitte-Python-Developer-Interview-Questions-EI_IE2763.0,8_KO9,25.htm \[9\]

```python
from collections import Counter

def char_frequency(s: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

def first_unique(s: str) -> str | None:
    counts = Counter(s)
    return next((ch for ch in s if counts[ch] == 1), None)

print(char_frequency("hello"))      # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
print(Counter("hello").most_common(1))  # [('l', 2)]
print(first_unique("swiss"))        # 'w'
```
- **Explanation:** Show the manual `dict.get` version first, since interviewers want to see the hash-map logic, then mention `Counter`. Dicts keep insertion order (guaranteed since 3.7), so the output order is predictable.
- **Complexity:** O(n) time, O(k) space (k = distinct characters).

### Rank 7 — Reverse a string / reverse words / swap case / palindrome
- **Category:** Coding / strings · **Difficulty:** Easy
- **Evidence:**
  - [CR] LTIMindtree "Program to Reverse the string": https://www.glassdoor.com/Interview/LTIMindtree-Software-Engineer-Interview-Questions-EI_IE8441464.0,11_KO12,29.htm \[25\]
  - [PP] HackerRank blog "Reverse Words in a Sentence": https://www.hackerrank.com/blog/python-interview-questions-developers-should-know/ \[26\]
  - [PP] HackerRank Python (Basic) cert "Reverse Word & Swap Case": https://github.com/anishLearnsToCode/hackerrank-python-basic-skill-test \[27\]

```python
def reverse_string(s: str) -> str:
    return s[::-1]

def reverse_string_manual(s: str) -> str:   # if slicing is "not allowed"
    chars = list(s)
    i, j = 0, len(chars) - 1
    while i < j:
        chars[i], chars[j] = chars[j], chars[i]
        i, j = i + 1, j - 1
    return "".join(chars)

def reverse_words(sentence: str) -> str:
    return " ".join(reversed(sentence.split()))

def reverse_words_swap_case(sentence: str) -> str:
    return reverse_words(sentence).swapcase()

def is_palindrome(s: str) -> bool:
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]

print(reverse_words("Python is awesome"))      # awesome is Python
print(reverse_words_swap_case("Hello World"))  # wORLD hELLO
print(is_palindrome("A man, a plan, a canal: Panama"))  # True
```
- **Explanation:** `split()` with no argument collapses repeated whitespace. Use `"".join` rather than `+=` in a loop, because strings are immutable and repeated concatenation copies.
- **Complexity:** O(n) time, O(n) space.

### Rank 8 — Sort an array (without `sort()`), and print alternate elements
- **Category:** Coding / algorithms · **Difficulty:** Easy
- **Evidence [CR]:**
  - Infosys (3 yrs) "write a program to sort the array": https://www.geeksforgeeks.org/infosys-interview-experience-2023-2/ \[1\]
  - Wipro "Write a program for sorting": https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm \[4\]
  - Cognizant HackerRank "Sorting and printing alternate numbers": https://www.geeksforgeeks.org/cognizant-interview-experience-set-2-campus/ \[20\]

```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def sorted_alternates(arr: list[int]) -> list[int]:
    return sorted(arr)[::2]

print(merge_sort([5, 2, 9, 1, 5, 6]))        # [1, 2, 5, 5, 6, 9]
print(sorted_alternates([5, 2, 9, 1, 5, 6])) # [1, 5, 6]
```
- **Explanation:** Give a hand-written O(n log n) sort, then say that in production you would use `sorted()` / `list.sort()` (Timsort: stable, O(n log n)). Know the difference: `sorted()` returns a new list, while `.sort()` sorts in place and returns `None`.
- **Complexity:** O(n log n) time, O(n) space.

### Rank 9 — Flatten a nested list / extract strings from nested lists
- **Category:** Coding / lists, recursion · **Difficulty:** Easy
- **Evidence [CR]:**
  - Capgemini "converting a nested list to a plain list": https://www.jointaro.com/interviews/companies/capgemini/experiences/python-developer-pune-march-3-2025-no-offer-positive-6ca61b4c/ \[3\]
  - HCLTech `my_list = [[35, 66, 31], ["python", 13, "is"], [15, "fun", 14]]`, print "python is fun": https://www.glassdoor.com/Interview/python-developer-interview-questions-SRCH_KO0,16.htm \[12\]

```python
from collections.abc import Iterable, Iterator
from typing import Any

def flatten(items: Iterable[Any]) -> Iterator[Any]:
    for x in items:
        if isinstance(x, (list, tuple)):
            yield from flatten(x)
        else:
            yield x

print(list(flatten([1, [2, [3, 4]], (5,), 6])))  # [1, 2, 3, 4, 5, 6]

my_list = [[35, 66, 31], ["python", 13, "is"], [15, "fun", 14]]
print(" ".join(x for sub in my_list for x in sub if isinstance(x, str)))  # python is fun
```
- **Explanation:** A recursive generator handles arbitrary depth. For one level only, a nested comprehension is enough. Don't treat `str` as iterable when recursing, or every character becomes an item.
- **Complexity:** O(N) time over all leaf elements; O(d) recursion depth.

### Rank 14 — Prime numbers in a range
- **Category:** Coding / loops, math · **Difficulty:** Easy
- **Evidence [CR]:** TCS "Write a program to print Prime Numbers for a given range": https://medium.com/@rana.akansha321/tcs-python-developer-interview-question-for-2023-87aab3426791 \[2\]

```python
from math import isqrt

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))

def primes_in_range(lo: int, hi: int) -> list[int]:
    """Sieve of Eratosthenes, inclusive bounds."""
    if hi < 2:
        return []
    sieve = bytearray([1]) * (hi + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(hi) + 1):
        if sieve[p]:
            sieve[p * p :: p] = bytes(len(range(p * p, hi + 1, p)))
    return [i for i in range(max(lo, 2), hi + 1) if sieve[i]]

print(primes_in_range(10, 30))  # [11, 13, 17, 19, 23, 29]
```
- **Explanation:** Trial division only needs to go up to √n. For a range, the sieve is the expected optimisation.
- **Complexity:** `is_prime` O(√n) · sieve O(n log log n) time, O(n) space.

### Rank 15 — Zip / merge two lists (and dict from two lists)
- **Category:** Coding / lists, dicts · **Difficulty:** Easy
- **Evidence [CR]:**
  - TCS "How we can zip two lists?": https://medium.com/@rana.akansha321/tcs-python-developer-interview-question-for-2023-87aab3426791 \[2\]
  - Deloitte "Merge two list based on some condition": https://www.glassdoor.ca/Interview/Deloitte-Python-Developer-Interview-Questions-EI_IE2763.0,8_KO9,25.htm \[9\]

```python
import heapq

names = ["asha", "ravi", "meena"]
scores = [91, 78, 85]

pairs = list(zip(names, scores, strict=True))   # strict= raises if lengths differ (3.10+)
lookup = dict(zip(names, scores))               # {'asha': 91, 'ravi': 78, 'meena': 85}
pass_list = [n for n, s in zip(names, scores) if s >= 80]   # merge-by-condition
merged_sorted = list(heapq.merge([1, 4, 9], [2, 3, 10]))    # [1, 2, 3, 4, 9, 10]
names_back, scores_back = zip(*pairs)            # "unzip"
```
- **Explanation:** By default `zip` silently truncates to the shortest input, which is a common bug; mention `strict=True` or `itertools.zip_longest`. Merging two sorted lists is a two-pointer O(n+m) job (`heapq.merge` does this lazily).
- **Complexity:** O(n) time; `zip` itself is lazy, O(1) extra.

### Rank 17 — Two Sum
- **Category:** Coding / hashing · **Difficulty:** Easy
- **Evidence [CR]:** HCLTech "Gave two coding questions from Leetcode, 2sum and longest substring without repeating characters": https://www.glassdoor.com/Interview/HCLTech-Python-Developer-Interview-Questions-EI_IE553909.0,7_KO8,24.htm \[11\]

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:
            return j, i
        seen[x] = i
    return None

print(two_sum([2, 7, 11, 15], 9))  # (0, 1)
```
- **Explanation:** One pass, storing value → index, and checking the complement before inserting so an element can't pair with itself. Mention the O(n²) brute force first, then optimise.
- **Complexity:** O(n) time, O(n) space.

### Rank 18 — Longest substring without repeating characters
- **Category:** Coding / sliding window · **Difficulty:** Medium
- **Evidence [CR]:** HCLTech (same report as above): https://www.glassdoor.com/Interview/HCLTech-Python-Developer-Interview-Questions-EI_IE553909.0,7_KO8,24.htm \[11\]

```python
def longest_unique_substring(s: str) -> int:
    last: dict[str, int] = {}
    start = best = 0
    for i, ch in enumerate(s):
        if last.get(ch, -1) >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best

print(longest_unique_substring("abcabcbb"))  # 3
print(longest_unique_substring("pwwkew"))    # 3
```
- **Explanation:** Keep a window `[start, i]` with no repeats. When a repeat appears inside the window, jump `start` past its last position.
- **Complexity:** O(n) time, O(min(n, alphabet)) space.

### Rank 19 — Remove / find duplicates
- **Category:** Coding / lists, sets · **Difficulty:** Easy
- **Evidence [CR]:**
  - HackerRank's own OA "Remove Duplicates from Sorted Array" (in place, O(1) extra memory): https://www.naukri.com/code360/interview-experiences/hackerrank/interview-experience-by-shivam-verma-off-campus-may-2022 \[28\]
  - "Find duplicate elements in an array": https://www.geeksforgeeks.org/interview-experiences/backend-developer-internship-interview-experience/ \[29\]

```python
from collections import Counter

def dedupe[T](xs: list[T]) -> list[T]:          # PEP 695 generic syntax (3.12+)
    return list(dict.fromkeys(xs))              # keeps first-seen order

def duplicates[T](xs: list[T]) -> list[T]:
    return [x for x, c in Counter(xs).items() if c > 1]

def remove_dups_sorted_inplace(arr: list[int]) -> int:
    if not arr:
        return 0
    k = 1
    for i in range(1, len(arr)):
        if arr[i] != arr[k - 1]:
            arr[k] = arr[i]
            k += 1
    return k   # first k elements are unique

nums = [1, 1, 2, 3, 3, 3]
print(dedupe([3, 1, 3, 2, 1]), duplicates(nums), remove_dups_sorted_inplace(nums), nums[:3])
# [3, 1, 2] [1, 3] 3 [1, 2, 3]
```
- **Explanation:** `set(xs)` loses order; `dict.fromkeys` keeps it. The in-place version is the two-pointer pattern HackerRank asked for.
- **Complexity:** O(n) time; O(n) space (hash versions) or O(1) (in-place sorted).

### Rank 20 — Anagram check / HackerRank "String Anagram"
- **Category:** Coding / strings, hashing · **Difficulty:** Easy
- **Evidence:**
  - [PP] HackerRank Problem Solving (Basic) cert includes "String Anagram": https://github.com/reebaseb/Hackerrank_ProblemSolvingBasic_Certificate_test-soltions \[13\]
  - [CR] GeeksforGeeks interview, anagram variant: https://www.geeksforgeeks.org/interview-experiences/geeksforgeeks-interview-experience-for-software-developer/ \[30\]

```python
from collections import Counter

def is_anagram(a: str, b: str) -> bool:
    return Counter(a) == Counter(b)

def string_anagram(dictionary: list[str], query: list[str]) -> list[int]:
    """For each query word, count dictionary words that are its anagrams."""
    signatures = Counter("".join(sorted(w)) for w in dictionary)
    return [signatures["".join(sorted(q))] for q in query]

print(is_anagram("listen", "silent"))  # True
print(string_anagram(["hack", "a", "rank", "khac", "ackh", "kran", "rankhacker", "a", "ab", "ba", "stairs", "raits"],
                     ["a", "nark", "bs", "hack", "stair"]))   # [2, 2, 0, 3, 1]
```
- **Explanation:** A sorted string (or a 26-count tuple) is a canonical "signature". Precomputing signature counts turns each query into an O(1) lookup.
- **Complexity:** O((D + Q) · L log L) time, O(D) space.

### Rank 24 — Maximum subarray sum (Kadane)
- **Category:** Coding / arrays, DP · **Difficulty:** Medium
- **Evidence [PP]:** HackerRank blog #2 "Maximum Subarray Sum", sample `[1, 2, 3, -2, 5]` → `9`: https://www.hackerrank.com/blog/python-interview-questions-developers-should-know/ \[26\]

```python
def max_subarray_sum(arr: list[int]) -> int:
    best = cur = arr[0]
    for x in arr[1:]:
        cur = max(x, cur + x)      # extend or restart
        best = max(best, cur)
    return best

print(max_subarray_sum([1, 2, 3, -2, 5]))   # 9
print(max_subarray_sum([-3, -1, -2]))       # -1 (all-negative edge case)
```
- **Explanation:** At each step, either extend the running subarray or start fresh at `x`. Initialising with `arr[0]` rather than 0 handles all-negative input correctly.
- **Complexity:** O(n) time, O(1) space.

### Rank 25 — Merge intervals / Minimum CPU cores (Accenture)
- **Category:** Coding / sorting, sweep line · **Difficulty:** Medium
- **Evidence:**
  - [PP] HackerRank blog #3 "Merge Intervals": https://www.hackerrank.com/blog/python-interview-questions-developers-should-know/ \[26\]
  - [CR⚠️] Accenture HackerRank (Feb 2026) "Minimum CPU Cores: processes with start/end times (end inclusive), find the minimum cores so no two overlap": https://interviewfox.ai/interview-questions/accenture-hackerrank/ (unverified marketing source)\[15\]

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

def min_cores(start: list[int], end: list[int]) -> int:
    # (time, 0) = start sorts before (time, 1) = end, so inclusive ends overlap
    events = sorted([(s, 0) for s in start] + [(e, 1) for e in end])
    cur = best = 0
    for _, kind in events:
        if kind == 0:
            cur += 1
            best = max(best, cur)
        else:
            cur -= 1
    return best

print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1, 6], [8, 10], [15, 18]]
print(min_cores([1, 2, 5], [3, 4, 6]))                        # 2
```
- **Explanation:** Both are "sort by start, then scan". The tie-break order on equal timestamps encodes whether ends are inclusive, which is the detail interviewers check.
- **Complexity:** O(n log n) time, O(n) space.

### Rank 26 — Product of array except self (EY)
- **Category:** Coding / prefix-suffix · **Difficulty:** Medium
- **Evidence [CR]:** EY Python Developer "Diamond inheritance, 2 leet code problems using python ex list product self": https://www.glassdoor.com/Interview/EY-Python-Developer-Interview-Questions-EI_IE2784.0,2_KO3,19.htm \[22\]

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    out = [1] * n
    prefix = 1
    for i in range(n):
        out[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix
        suffix *= nums[i]
    return out

print(product_except_self([1, 2, 3, 4]))  # [24, 12, 8, 6]
```
- **Explanation:** No division, so it is safe with zeros. Each output is (product of everything to the left) × (product of everything to the right).
- **Complexity:** O(n) time, O(1) extra space (excluding output).

### Rank 27 — Password sanitizer (Accenture)
- **Category:** Coding / strings · **Difficulty:** Easy
- **Evidence [CR⚠️]:** Accenture HackerRank (Feb 2026): "given a line of space-separated passwords, return valid ones in order; valid = length ≥5, not letters-only and not digits-only": https://interviewfox.ai/interview-questions/accenture-hackerrank/ (unverified)\[15\]

```python
def sanitize_passwords(line: str) -> list[str]:
    return [
        p for p in line.split()
        if len(p) >= 5 and not p.isalpha() and not p.isdigit()
    ]

print(sanitize_passwords("abc12 hello 123456 pa$$w0rd x1"))  # ['abc12', 'pa$$w0rd']
```
- **Explanation:** Know the built-in predicates: `isalpha`, `isdigit`, `isalnum`, `isupper`. Note that `"pa$$"` is neither alpha nor digit, so symbols pass.
- **Complexity:** O(total characters) time, O(n) space.

### Rank 28 — HackerRank Python (Basic) cert: Shape Classes with Area + Shopping Cart
- **Category:** Coding / OOP · **Difficulty:** Easy
- **Evidence [PP]:**
  - Shape Classes and Dominant Cells reported as the two questions: https://www.azhark.com/2023/04/07/hackerrank-python-basic-certification-solutions/ \[31\]
  - Shopping Cart: https://gist.github.com/ZakriaJanjua/95844e774d54cfb56796defe016ff753 \[32\]
  - Shopping Cart and Dominant Cells: https://medium.com/@j622amilah/hackerrank-tests-python-3420011863a1 \[33\]

```python
import math
from dataclasses import dataclass

class Rectangle:
    def __init__(self, length: float, width: float) -> None:
        self.length, self.width = length, width
    def area(self) -> float:
        return self.length * self.width

class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius
    def area(self) -> float:
        return math.pi * self.radius ** 2

@dataclass(frozen=True, slots=True)
class Item:
    name: str
    price: int

class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[Item] = []
    def add(self, item: Item) -> None:
        self._items.append(item)
    def total(self) -> int:
        return sum(i.price for i in self._items)
    def __len__(self) -> int:
        return len(self._items)

print(f"{Rectangle(2, 3).area():.2f} {Circle(1).area():.2f}")  # 6.00 3.14
cart = ShoppingCart(); cart.add(Item("Bike", 1000)); cart.add(Item("Lock", 50))
print(len(cart), cart.total())  # 2 1050
```
- **Explanation:** These tasks test whether you can implement dunder methods (`__len__`) so locked template code works (`len(cart)`).\[34\] Watch output formatting (`%.2f`), which is where hidden test cases fail.\[35\]
- **Complexity:** `add` O(1), `total` O(n), `len` O(1).

### Rank 29 — HackerRank Python (Basic) cert: Multiset Implementation
- **Category:** Coding / OOP, dunder methods · **Difficulty:** Easy
- **Evidence [PP]:** https://github.com/MD-MAFUJUL-HASAN/HackerRank-Python-Basic-Skills-Certification-Test ; https://github.com/sanskritilakhmani/Hackerrank/blob/main/Certification_Test_Python/Basic/Multiset_Implementation \[36\]\[37\]

```python
from collections import Counter

class Multiset:
    def __init__(self) -> None:
        self._counts: Counter[int] = Counter()
        self._size = 0

    def add(self, val: int) -> None:
        self._counts[val] += 1
        self._size += 1

    def remove(self, val: int) -> None:          # removes one occurrence, if any
        if self._counts[val] > 0:
            self._counts[val] -= 1
            self._size -= 1

    def __contains__(self, val: int) -> bool:    # enables `val in m`
        return self._counts[val] > 0

    def __len__(self) -> int:
        return self._size

m = Multiset(); m.add(1); m.add(1); m.remove(1)
print(1 in m, len(m))   # True 1
```
- **Explanation:** Many posted solutions use a list with `list.remove`, which is O(n).\[37\] A `Counter` makes every operation O(1), a good point to raise at 3 years' experience. A missing key in a `Counter` returns 0 without inserting it.
- **Complexity:** All operations O(1) average; O(distinct values) space.

### Rank 30 — HackerRank Python (Basic) cert: Dominant Cells
- **Category:** Coding / 2-D arrays · **Difficulty:** Easy
- **Evidence [PP]:** "find the integers greater than any of its side and corner neighbors": https://medium.com/@j622amilah/hackerrank-tests-python-3420011863a1 ; https://github.com/adminazhar/HackerRank-Python-Basic-Skills-Certification-Test-Solution \[33\]\[38\]

```python
def num_cells(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def dominant(r: int, c: int) -> bool:
        v = grid[r][c]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] >= v:
                    return False
        return True

    return sum(dominant(r, c) for r in range(rows) for c in range(cols))

print(num_cells([[1, 2, 7], [4, 5, 6], [8, 8, 9]]))  # 2  (7 and 9)
```
- **Explanation:** Check all 8 neighbours with bounds checks. "Strictly greater" means ties disqualify a cell (both 8s fail).
- **Complexity:** O(R·C) time, O(1) extra space.

### Rank 42 — Balanced parentheses
- **Category:** Coding / stack · **Difficulty:** Easy
- **Evidence [CR]:** "Check if parentheses are balanced" in an online coding test: https://www.geeksforgeeks.org/interview-experiences/backend-developer-internship-interview-experience/ ; listed among Infosys easy coding questions (Valid Parentheses): https://www.geeksforgeeks.org/interview-prep/infosys-coding-interview-questions/ \[29\]\[39\]

```python
def is_balanced(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

print(is_balanced("{[()]}"), is_balanced("([)]"))  # True False
```
- **Explanation:** A list works as a stack (`append`/`pop` are O(1)). Remember the empty-stack and leftover-opener edge cases.
- **Complexity:** O(n) time, O(n) space.

### Rank 43 — GCD of an array / decimal to binary
- **Category:** Coding / math · **Difficulty:** Easy
- **Evidence [CR]:**
  - Cognizant HackerRank "GCD of all the numbers in a given array": https://www.geeksforgeeks.org/cognizant-interview-experience-set-2-campus/ \[20\]
  - LTIMindtree "convert decimal to binary program": https://www.glassdoor.co.in/Interview/LTIMindtree-Developer-Interview-Questions-EI_IE8441464.0,11_KO12,21.htm \[40\]

```python
import math
from functools import reduce

def gcd_array(arr: list[int]) -> int:
    return reduce(math.gcd, arr)        # or math.gcd(*arr) on 3.9+

def to_binary(n: int) -> str:
    if n == 0:
        return "0"
    bits: list[str] = []
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    return "".join(reversed(bits))

print(gcd_array([12, 18, 24]), to_binary(10), format(10, "b"))  # 6 1010 1010
```
- **Explanation:** Euclid's algorithm is inside `math.gcd`. For binary, show the manual divide-by-2 loop, then `bin(n)[2:]` / `format(n, "b")`.
- **Complexity:** GCD O(n log M) · binary O(log n).

### Rank 44 — Accenture "Desired Array" (sum of k smallest positives not divisible by any element)
- **Category:** Coding / math, loops · **Difficulty:** Medium
- **Evidence [CR]:** Accenture Cognitive & Technical Assessment 2023, example `k=4, arr=[2,3,4,5,6]` → 1+7+11+13 = 32: https://leetcode.com/discuss/interview-question/3694490/Accenture-OA-(Cognitive-and-Technical-Assessment-2023)-Questions-and-Answers/ (fresher drive; detail partly secondhand)\[15\]\[41\]

```python
def desired_sum(arr: list[int], k: int) -> int:
    divisors = sorted(set(arr))
    if 1 in divisors:
        return 0                     # every integer is divisible by 1
    total = found = n = 0
    while found < k:
        n += 1
        if all(n % d for d in divisors):
            total += n
            found += 1
    return total

print(desired_sum([2, 3, 4, 5, 6], 4))  # 32
```
- **Explanation:** Brute force over candidates is enough for OA constraints. To optimise, drop any divisor that is a multiple of a smaller one (4 and 6 are redundant once 2 is present). Handle the `1` edge case to avoid an infinite loop.
- **Complexity:** O(answer × |distinct divisors|) time, O(|arr|) space.

### Rank 45 — Deloitte "Count Subsequences" (all elements equal, mod 1e9+7)
- **Category:** Coding / combinatorics, hashing · **Difficulty:** Medium
- **Evidence [CR]:** Deloitte Analyst (Python experience required), June 2022: "return the total number of those subsequences of the array in which all the elements are equal… modulo 10^9 + 7": https://www.naukri.com/code360/interview-experiences/deloitte/interview-experience-analyst-jun-2022-exp-0-2-years \[42\]

```python
from collections import Counter

def count_equal_subsequences(arr: list[int]) -> int:
    MOD = 10**9 + 7
    return sum(pow(2, c, MOD) - 1 for c in Counter(arr).values()) % MOD

print(count_equal_subsequences([1, 2, 1]))  # 4  -> {1},{1},{1,1},{2}
```
- **Explanation:** A value occurring c times gives 2^c − 1 non-empty subsequences made only of that value. Three-argument `pow` keeps the numbers small.
- **Complexity:** O(n + k log c) time, O(k) space.

---

## Details — Section B: Output-Prediction & Code-Snippet Questions

### Rank 10 — Mutable default argument
- **Category:** Functions / mutability · **Evidence [CT + PP]:** described as "the most common Python trick question" (https://thekiranacademy.com/python-interview-questions); \[43\] HackerRank's "Default Arguments" debugging challenge is built on this trap (https://www.hackerrank.com/blog/python-interview-questions-developers-should-know/) \[26\] · **Difficulty:** Medium\[26\]

```python
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))   # ['a']
print(add_item("b"))   # ['a', 'b']   <- same list reused

def add_item_fixed(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```
- **Answer / explanation:** The Python Language Reference (§8, Function definitions) states that "Default parameter values are evaluated from left to right when the function definition is executed", so "the same 'pre-computed' value is used for each call". That value lives in `add_item.__defaults__`. Fix with a `None` sentinel. Linters such as ruff flag this pattern (B006). The dataclass equivalent is `field(default_factory=list)`.

### Rank 11 — Assignment aliasing vs shallow vs deep copy
- **Category:** References / mutability · **Evidence [CR]:** Infosys Senior Python "basic questions from python like shallow and deep copy": https://www.glassdoor.com/Interview/Infosys-Senior-Python-Developer-Interview-Questions-EI_IE7927.0,7_KO8,31.htm · **Difficulty:** Medium\[7\]

```python
import copy

a = [[1, 2], [3]]
b = a                 # alias, same object
c = a[:]              # shallow copy (= list(a), a.copy(), copy.copy(a))
d = copy.deepcopy(a)  # fully independent

a[0].append(99)
a.append([4])
print(b)  # [[1, 2, 99], [3], [4]]
print(c)  # [[1, 2, 99], [3]]      <- shares inner lists, not the outer list
print(d)  # [[1, 2], [3]]
```
- **Answer / explanation:** `=` never copies.\[44\] A shallow copy duplicates only the outer container. `deepcopy` recursively copies nested objects (and tracks cycles via a memo dict).

### Rank 16 — Scope: local vs global, `UnboundLocalError`, `nonlocal`
- **Category:** Scope (LEGB) · **Evidence [CR]:** Wipro "what is local and global variable": https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm \[4\] · **Difficulty:** Medium

```python
x = 10
def f():
    print(x)   # UnboundLocalError: x is local because it's assigned below
    x = 20

def make_counter():
    count = 0
    def inc() -> int:
        nonlocal count
        count += 1
        return count
    return inc

c = make_counter(); c(); print(c())   # 2
```
- **Answer / explanation:** Any assignment to a name anywhere in a function makes it local for the whole function, decided at compile time. Name lookup order is Local → Enclosing → Global → Built-in.\[43\] Use `global` or `nonlocal` to rebind outer names.

### Rank 31 — Slicing
- **Category:** Slicing / sequences · **Evidence [CT]** · **Difficulty:** Easy

```python
s = "interview"
print(s[::-1])   # weivretni
print(s[1:4])    # nte
print(s[-3:])    # iew
print(s[::2])    # itriw
print(s[100:])   # ''   (out-of-range slice: no error)
# s[100]         # IndexError (indexing does raise)
a = [1, 2, 3, 4, 5]
a[1:3] = [9]
print(a)         # [1, 9, 4, 5]
```
- **Answer / explanation:** Slices are half-open `[start, stop)`, clamp out-of-range bounds silently, and always return a new object. Slice assignment can change a list's length.

### Rank 32 — `[[0] * 3] * 3`
- **Category:** References / list multiplication · **Evidence [CT]** · **Difficulty:** Easy

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)   # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

grid_ok = [[0] * 3 for _ in range(3)]
grid_ok[0][0] = 1
print(grid_ok)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```
- **Answer / explanation:** `* 3` repeats the reference to one inner list. Use a comprehension to build distinct rows.

### Rank 33 — `is` vs `==`
- **Category:** Identity vs equality · **Evidence [CT]:** listed among Deloitte prep questions (https://whitescholars.com/top-python-interview-questions-asked-in-deloitte/) \[45\] · **Difficulty:** Easy

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b, a is b)   # True False
print(a is a[:])        # False
x = None
print(x is None)        # True  (the idiomatic None check)
```
- **Answer / explanation:** `==` calls `__eq__` (value); `is` compares object identity. Small-integer and string caching (e.g., `256 is 256`) is a CPython implementation detail, so never rely on `is` for numbers or strings.

### Rank 34 — Immutability traps: tuple with a list, string mutation, unhashable keys
- **Category:** Data types / exceptions · **Evidence [CT]** · **Difficulty:** Medium

```python
t = ([1, 2], 3)
try:
    t[0] += [3]
except TypeError:
    print("TypeError")
print(t)            # ([1, 2, 3], 3)  <- list mutated despite the error!

s = "abc"
# s[0] = "z"        # TypeError: 'str' object does not support item assignment
# {[1]: "a"}        # TypeError: unhashable type: 'list'
print({(1, 2): "ok"})   # tuples of immutables are hashable
```
- **Answer / explanation:** `+=` on the list runs in place (`__iadd__`) before the tuple item assignment fails, so you get both the mutation and the exception. Dict keys and set members must be hashable.\[43\]

### Rank 35 — Operator precedence and arithmetic MCQs
- **Category:** Operators · **Evidence [CT]:** examples from MCQ banks (https://www.igmguru.com/blog/python-mcqs ; https://www.gyansetu.in/blog/70-python-mcq-questions-and-answers-interview-ready/) · **Difficulty:** Easy\[46\]\[47\]

```python
print(2 ** 3 ** 2)     # 512  (** is right-associative: 2 ** 9)
print((2 ** 3) ** 2)   # 64
print(4 + 3 % 5)       # 7    (% binds tighter than +)
print(7 / 2, 7 // 2)   # 3.5 3
print(-7 // 2)         # -4   (floor division rounds toward −∞)
print(-7 % 3)          # 2    (result takes the divisor's sign)
print(round(2.5), round(3.5))  # 2 4  (banker's rounding)
print(0.1 + 0.2 == 0.3)        # False (binary floating point)
```
- **Answer / explanation:** These are the standard MCQ distractors. Know right-associativity of `**`, floor semantics for negatives, and round-half-to-even.

### Rank 36 — Truthiness and implicit `None`
- **Category:** Data types / functions · **Evidence [CT]:** "What is the output of bool([])? → False"; "default return value of a function → None" (https://www.gyansetu.in/blog/70-python-mcq-questions-and-answers-interview-ready/) · **Difficulty:** Easy\[46\]

```python
print(bool([]), bool("0"), bool(0.0), bool(" "))  # False True False True
def f(): pass
print(f())               # None
print(None == False)     # False
print([] or "default")   # default   (or returns an operand, not a bool)
```
- **Answer / explanation:** Empty containers, `0`, `0.0`, `""` and `None` are falsy; any non-empty string (even `"0"`) is truthy. `and`/`or` return one of their operands.

### Rank 37 — try / except / else / finally
- **Category:** Exceptions · **Evidence [CT]:** exception handling appears in Deloitte/EY prep lists (https://entri.app/blog/deloitte-python-interview-questions/) \[48\] · **Difficulty:** Medium

```python
def f() -> int:
    try:
        return 1
    finally:
        return 2          # overrides the try's return

print(f())                # 2

try:
    x = int("42")
except ValueError:
    print("bad")
else:
    print("ok", x)        # runs only if no exception
finally:
    print("done")         # always runs
# ok 42
# done
```
- **Answer / explanation:** `finally` always runs; a `return` inside it swallows the earlier return or exception. That is why Python 3.14 adopted "PEP 765: Disallow return/break/continue that exit a finally block": per the CPython docs, "The compiler emits a SyntaxWarning when a return, break or continue statements appears where it exits a finally block." `else` keeps the "success path" out of the guarded block. Catch specific exceptions, not bare `except:`.

### Rank 38 — Late-binding closures
- **Category:** Functions / closures / comprehensions · **Evidence [CT]** · **Difficulty:** Medium

```python
funcs = [lambda: i for i in range(3)]
print([fn() for fn in funcs])        # [2, 2, 2]

funcs_ok = [lambda i=i: i for i in range(3)]
print([fn() for fn in funcs_ok])     # [0, 1, 2]
```
- **Answer / explanation:** Closures look up `i` when called, not when created. Binding it as a default argument (or using `functools.partial`) captures the current value.

### Rank 39 — Comprehensions and generator exhaustion
- **Category:** Comprehensions / generators · **Evidence [CT]:** list comprehension asked at LTIMindtree (https://www.glassdoor.co.in/Interview/LTIMindtree-Internship-Interview-Questions-EI_IE8441464.0,11_KO12,22.htm) and Capgemini · **Difficulty:** Easy\[49\]

```python
nums = [1, 2, 3, 4]
print([n * n for n in nums if n % 2 == 0])   # [4, 16]
print({n % 2 for n in nums})                 # {0, 1}
print({n: n * n for n in nums})              # {1: 1, 2: 4, 3: 9, 4: 16}
g = (n for n in nums)
print(sum(g), sum(g))                        # 10 0   <- generator is single-use
```
- **Answer / explanation:** Brackets decide the type: `[]` list, `{}` set or dict, `()` lazy generator. A generator can be consumed only once. Comprehension variables don't leak into the enclosing scope in Python 3.

---

## Details — Section C: Theory, Concepts, Complexity & Debugging

### Rank 1 — List vs tuple (and set vs dict)
- **Evidence [CR]:**
  - TCS: https://medium.com/@rana.akansha321/tcs-python-developer-interview-question-for-2023-87aab3426791 \[2\]
  - Wipro "List and tuple differences": https://www.glassdoor.ca/Interview/Wipro-Python-Developer-Interview-Questions-EI_IE9936.0,5_KO6,22.htm \[14\]
  - Capgemini: https://www.jointaro.com/interviews/companies/capgemini/experiences/python-developer-pune-march-3-2025-no-offer-positive-6ca61b4c/
  - Infosys "Python Core Basics like tuple, list": https://www.glassdoor.com/Interview/Infosys-Interview-RVW94750868.htm \[50\]
- **Difficulty:** Easy

| | list | tuple | set | dict |
|---|---|---|---|---|
| Mutable | Yes | No | Yes | Yes |
| Ordered | Yes | Yes | No | Insertion-ordered (3.7+) |
| Duplicates | Yes | Yes | No | Keys unique |
| Hashable (usable as key) | No | Yes, if elements are | No (`frozenset` is) | No |
| Membership `in` | O(n) | O(n) | O(1) avg | O(1) avg (keys) |
| Typical use | Growing collection | Fixed record, dict key | Dedup, membership | Key → value lookup |

- **Answer:** Lead with mutability, since everything else follows from it. Tuples are slightly smaller and faster to create, and they signal "this record doesn't change".\[43\]\[51\]

### Rank 2 — Decorators (write one)
- **Evidence [CR]:** Accenture, Wipro, Infosys, Capgemini (see Key Findings 2) · **Difficulty:** Medium

```python
import functools
import time
from collections.abc import Callable

def timed[**P, R](func: Callable[P, R]) -> Callable[P, R]:   # PEP 695 (3.12+)
    @functools.wraps(func)                                   # keeps __name__/__doc__
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
    return wrapper

def retry(times: int) -> Callable:                            # decorator with arguments
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times:
                        raise
        return wrapper
    return decorator

@timed
def slow_add(a: int, b: int) -> int:
    time.sleep(0.1)
    return a + b
```
- **Answer:** A decorator is a callable that takes a function and returns a replacement; `@d` is shorthand for `f = d(f)`. Mention `functools.wraps`, decorators with arguments (three levels of nesting), and real uses: logging, timing, auth, caching (`functools.cache`), Django `@login_required`, Flask `@app.route`.

### Rank 5 — OOP: `__init__`, `self`, multiple inheritance, MRO (diamond)
- **Evidence [CR]:**
  - Infosys "Define multiple inheritances… Define constructor": https://www.geeksforgeeks.org/infosys-interview-experience-2023-2/ \[52\]
  - Wipro "what is __init__… what is self… multiple inheritance": https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm \[4\]
  - EY "Diamond inheritance": https://www.glassdoor.com/Interview/EY-Python-Developer-Interview-Questions-EI_IE2784.0,2_KO3,19.htm \[22\]
- **Difficulty:** Medium

```python
class A:
    def hello(self) -> str:
        return "A"

class B(A):
    def hello(self) -> str:
        return "B" + super().hello()

class C(A):
    def hello(self) -> str:
        return "C" + super().hello()

class D(B, C):
    pass

print(D().hello())                        # BCA
print([k.__name__ for k in D.__mro__])    # ['D', 'B', 'C', 'A', 'object']
```
- **Answer:**
  - `__init__` initialises an already-created instance; `__new__` creates it.
  - `self` is the instance, passed explicitly as the first parameter.
  - Python resolves diamonds with C3 linearisation (the MRO), so `super()` means "next in the MRO", not "my parent". That is why the output is `BCA` and A runs only once.
  - Python has no method overloading by signature; use default arguments or `functools.singledispatchmethod`.

### Rank 6 — Generators, iterators, and comprehensions
- **Evidence [CR]:**
  - Capgemini "comprehensions, decorators, and generators": https://www.jointaro.com/interviews/companies/capgemini/experiences/python-developer-pune-march-3-2025-no-offer-positive-6ca61b4c/ \[3\]
  - Infosys "Generators, List comprehension": https://www.glassdoor.com/Interview/Infosys-Interview-RVW94750868.htm \[50\]
- **Difficulty:** Medium

```python
from collections.abc import Iterator

def read_large_file(path: str) -> Iterator[str]:
    with open(path, encoding="utf-8") as f:
        for line in f:                 # file objects are lazy iterators
            yield line.rstrip("\n")

class Countdown:                        # iterator protocol by hand
    def __init__(self, start: int) -> None:
        self.current = start
    def __iter__(self) -> "Countdown":
        return self
    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print(list(Countdown(3)))   # [3, 2, 1]
```
- **Answer:**
  - An iterable has `__iter__`; an iterator also has `__next__` and raises `StopIteration` when done.
  - A generator function (`yield`) builds an iterator automatically and pauses its state between values, so it uses O(1) memory for streams. That makes it the standard answer to "process a file larger than RAM".\[53\]
  - `yield from` delegates to a sub-generator.

### Rank 12 — `*args` / `**kwargs` (HackerRank "Average Function")
- **Evidence:**
  - [CR] Accenture "basic python questions like OOP, lists, kwargs and args": https://www.glassdoor.com/Interview/Accenture-Python-Developer-Interview-Questions-EI_IE4138.0,9_KO10,26.htm \[5\]
  - [PP] HackerRank cert "Average Function": https://github.com/MD-MAFUJUL-HASAN/HackerRank-Python-Basic-Skills-Certification-Test/blob/main/Average%20Function.py \[35\]
- **Difficulty:** Easy

```python
def avg(*nums: float) -> float:
    return sum(nums) / len(nums)

def describe(*args: object, **kwargs: object) -> None:
    print(args, kwargs)

print(f"{avg(1, 2, 3, 4):.2f}")   # 2.50
describe(1, 2, x=3)               # (1, 2) {'x': 3}
nums = [5, 10]
print(avg(*nums))                 # 7.5   (unpacking at call site)
```
- **Answer:** `*args` collects extra positional arguments into a tuple and `**kwargs` collects keyword arguments into a dict. The same symbols unpack at call sites. Parameter order is: positional, `*args`, keyword-only, `**kwargs`.

### Rank 13 — lambda, map, filter, reduce
- **Evidence [CR]:** Infosys (3 yrs) "What is a lambda function… Define a map, reduce, and filter": https://www.geeksforgeeks.org/infosys-interview-experience-2023-2/ · **Difficulty:** Easy\[1\]

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]
print(list(map(lambda x: x * 2, nums)))       # [2, 4, 6, 8, 10]
print(list(filter(lambda x: x % 2, nums)))    # [1, 3, 5]
print(reduce(lambda a, b: a * b, nums))       # 120
print(sorted(["bb", "a", "ccc"], key=len))    # ['a', 'bb', 'ccc']
```
- **Answer:** A lambda is a single-expression anonymous function. In Python 3, `map` and `filter` return lazy iterators, and `reduce` lives in `functools`. Comprehensions are usually more readable; the classic legitimate use of lambda is `key=` for sorting.

### Rank 21 — Memory management, GIL, multithreading vs multiprocessing
- **Evidence [CR]:**
  - TCS "How python will store memory… what we have in python [vs Java GC]?": https://www.naukri.com/code360/interview-experiences/tata-consultancy-services-tcs/interview-experience-by-on-campus-oct-2020-2-782 \[54\]
  - Infosys "Memory Management in Python": https://www.naukri.com/code360/interview-experiences/infosys-private-limited/infosys-interview-experience-off-campus-feb-2022-2-6910 \[55\]
  - Deloitte "Python multithreading": https://www.naukri.com/code360/interview-experiences/deloitte/deloitte-interview-experience-on-campus-mar-2025 \[16\]
- **Difficulty:** Medium
- **Answer:**
  - CPython frees objects through reference counting, and a cyclic garbage collector (`gc` module, generational) cleans up reference cycles. Objects live on a private heap managed by the interpreter.
  - The GIL lets only one thread execute Python bytecode at a time, so threads help I/O-bound work (network, disk) but not CPU-bound work. For CPU-bound work use `multiprocessing` / `ProcessPoolExecutor`; for high-concurrency I/O, `asyncio` is another option.
  - Bonus at 3 years, from the Python docs:
    - What's New in 3.13: "CPython 3.13 has experimental support for running with the global interpreter lock disabled" (PEP 703).
    - What's New in 3.14 (PEP 779): "The free-threaded build of Python is now supported and no longer experimental", i.e. "officially supported but still optional".

### Rank 22 — File handling: CSV / JSON, `with`
- **Evidence [CR]:**
  - EY "how we could read a CSV file with the datasets in python and split it into two parts": https://www.naukri.com/code360/interview-experiences/ernst-young-ey/interview-experience-by-vikram-kumar-gour-off-campus-jul-2022 \[56\]
  - EY "JSON file handling and error correction": https://www.glassdoor.com/Interview/EY-Python-Developer-Interview-Questions-EI_IE2784.0,2_KO3,19.htm \[22\]
  - Wipro "File open and close": https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm \[4\]
- **Difficulty:** Easy

```python
import csv
import json
from pathlib import Path

def split_csv(path: Path, ratio: float = 0.8) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:   # auto-closes, even on error
        rows = list(csv.DictReader(f))
    cut = int(len(rows) * ratio)
    return rows[:cut], rows[cut:]

def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Bad JSON at line {e.lineno}: {e.msg}") from e

# pandas variant (often expected at service companies):
# df = pd.read_csv(path); train = df.sample(frac=0.8, random_state=42); test = df.drop(train.index)
```
- **Answer:** Always use `with` (a context manager calls `__exit__` to close the file). Read large files line by line. Use `newline=""` for the csv module. Wipro and Infosys also report pandas basics such as "Create dataframe using a dictionary" (https://www.glassdoor.ca/Interview/Wipro-Python-Developer-Interview-Questions-EI_IE9936.0,5_KO6,22.htm): \[14\] `pd.DataFrame({"a": [1, 2], "b": [3, 4]})`.

### Rank 23 — Quick-fire basics
- **Evidence [CR]:**
  - Wipro "break, continue, pass… range and xrange": https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm \[4\]
  - Infosys "interpreted or compiled": https://www.geeksforgeeks.org/infosys-interview-experience-2023-2/ \[1\]
  - TCS "Who invented python and which year": https://www.glassdoor.com/Interview/TCS-Python-Developer-Interview-Questions-EI_IE3211746.0,3_KO4,20.htm \[57\]
- **Difficulty:** Easy
- **Answers:**
  - **`break`** exits the loop; **`continue`** skips to the next iteration; **`pass`** is a no-op placeholder. A loop's `else` block runs only if the loop wasn't `break`-ed.
  - **`range` vs `xrange`:** `xrange` existed only in Python 2. Python 3's `range` is already lazy (O(1) memory), supports O(1) `in` for ints, and supports slicing.
  - **Interpreted or compiled?** Both. Source is compiled to bytecode (cached as `.pyc` in `__pycache__`), and the CPython virtual machine then interprets that bytecode.\[53\]
  - **Creator:** Guido van Rossum; first released in 1991 (as stated in HackerRank's own Python blog, https://www.hackerrank.com/blog/python-interview-questions-developers-should-know/). \[26\]

### Rank 40 — Time complexity of built-ins (state the Big-O of every solution)
- **Evidence [CT]:** interviewers in candidate reports probe "time complexity of hash maps" (https://www.geeksforgeeks.org/interview-experiences/backend-developer-internship-interview-experience/) \[29\] and binary search analysis at Deloitte (https://www.geeksforgeeks.org/interview-experiences/deloitte-software-developer-interview-experience/) \[58\] · **Difficulty:** Easy

| Operation | Complexity | Interview note |
|---|---|---|
| `x in list` | O(n) | Convert to `set` if checked repeatedly |
| `x in set` / `key in dict` | O(1) average | Requires hashable elements |
| `list.append` / `list.pop()` | O(1) amortized | |
| `list.insert(0, x)` / `list.pop(0)` | O(n) | Use `collections.deque` |
| `sorted()` / `list.sort()` | O(n log n) | Timsort, stable |
| `s += ch` in a loop | O(n²) worst | Use `"".join(parts)` |
| Slicing `a[i:j]` | O(j − i) | Creates a copy |
| Binary search (`bisect`) | O(log n) | Input must be sorted |

### Rank 41 — Debugging: HackerRank "Default Arguments" (`print_from_stream`)
- **Evidence [PP]:** HackerRank blog #8: "the task is to debug the existing code… Debug the given function print_from_stream using the default value of one of its arguments": https://www.hackerrank.com/blog/python-interview-questions-developers-should-know/ \[26\] · **Difficulty:** Medium\[26\]

```python
class EvenStream:
    def __init__(self) -> None:
        self.current = 0
    def get_next(self) -> int:
        to_return = self.current
        self.current += 2
        return to_return

class OddStream:
    def __init__(self) -> None:
        self.current = 1
    def get_next(self) -> int:
        to_return = self.current
        self.current += 2
        return to_return

# Buggy: def print_from_stream(n, stream=EvenStream()):  <- one shared instance keeps its state
def print_from_stream(n: int, stream: EvenStream | OddStream | None = None) -> None:
    if stream is None:
        stream = EvenStream()          # fresh stream per call
    for _ in range(n):
        print(stream.get_next())
```
- **Answer / explanation:** This is the mutable-default bug (Rank 10) in a debugging wrapper. The default `EvenStream()` is created once, so a second call continues from where the first stopped instead of restarting at 0. HackerRank's debugging tasks typically lock the template, so fix only the signature and the first lines of the body.

---

## Recommendations

1. **Week 1: coding core (Ranks 3–9, 14–20).** Write each solution from scratch in under 10 minutes, saying its Big-O aloud. These match what TCS, Infosys, Capgemini, Accenture and Deloitte candidates report.
2. **Week 1, in parallel: concept trio (Ranks 1, 2, 6).** Be able to *write* a decorator with `functools.wraps` and a generator, not just define them. This is the most consistent signal across Accenture, Wipro, Infosys and Capgemini reports.
3. **Week 2: HackerRank mechanics (Ranks 28–30, 41).** Take HackerRank's free Python (Basic) certification as a dry run: same IDE, locked templates, hidden test cases, 2 problems in 90 minutes.\[31\]\[59\] Most failures come from output formatting (`%.2f`, trailing spaces) and edge cases, not the algorithm.
4. **Week 2: MCQ sprint (Ranks 10–11, 31–39).** Infosys and Wipro put Python MCQs in front of the interview, so drill output prediction on paper without running code.
5. **Budget 30–40% of prep for non-Python topics.** At 3 years, nearly every report pairs Python with SQL (joins, second-highest salary, window functions) and the framework on your CV (Django request/response cycle, pandas, AWS Lambda/EC2 at Infosys).\[7\]\[60\]
6. **If the role is product-based or client-facing (HCLTech client rounds, IBM),** add LeetCode-medium patterns: sliding window, prefix sums, intervals, heaps. Those OAs are harder than service-company ones.

## Caveats

- **Source coverage:**
  - I couldn't retrieve Reddit threads or AmbitionBox pages during this research; the targeted searches surfaced Glassdoor, GeeksforGeeks, Naukri Code360, Taro and Medium instead.
  - Glassdoor entries are short, anonymous snippets, often without dates or experience levels.
  - Several Code360 and GfG reports are from campus or 0–2-year hires; I used them for format and topic signal, not as 3-year-specific evidence.
- **Unverified sources (flagged ⚠️):** interviewfox.ai is a marketing site for an AI interview-assist tool. Its Accenture and IBM question reports are plausible and consistent with other sources, but unverifiable.
- **Not used as evidence:** aggregator "TCS/Infosys/Deloitte Python questions" pages (Entri, Credo Systemz, Internshala, PrepBytes, PrepInsta) are prep content, not candidate reports. They appear only as [CT] support.
- **Exact repeats are unlikely:** HackerRank Support's "Create a Question" article says "HackerRank for Work allows you to create questions based on your hiring requirements", and these are "saved in the My Company Library". So expect the same *patterns* (strings, frequency, intervals, small OOP classes) rather than identical problems.
- **Frequency ranks are evidence-weighted judgments,** not statistical counts. The public sample is small (tens of reports, not thousands), and Glassdoor difficulty ratings for the same company conflict between its .com and .co.in sites.

## Sources

1. [Infosys Interview Experience 2023](https://www.geeksforgeeks.org/infosys-interview-experience-2023-2/)
2. [Tcs Python Developer Interview Question for 2023](https://medium.com/@rana.akansha321/tcs-python-developer-interview-question-for-2023-87aab3426791)
3. [Capgemini Python Developer Interview Experience - Pune, Maharashtra](https://www.jointaro.com/interviews/companies/capgemini/experiences/python-developer-pune-march-3-2025-no-offer-positive-6ca61b4c/)
4. [Wipro Automation Engineer Interview Questions](https://www.glassdoor.com/Interview/Wipro-Automation-Engineer-Interview-Questions-EI_IE9936.0,5_KO6,25.htm)
5. [Accenture Python Developer Interview Experience & Questions](https://www.glassdoor.com/Interview/Accenture-Python-Developer-Interview-Questions-EI_IE4138.0,9_KO10,26.htm)
6. [Wipro Python Developer Interview Experience & Questions](https://www.glassdoor.com/Interview/Wipro-Python-Developer-Interview-Questions-EI_IE9936.0,5_KO6,22.htm)
7. [Infosys Senior Python Developer Interview Experience & Questions](https://www.glassdoor.com/Interview/Infosys-Senior-Python-Developer-Interview-Questions-EI_IE7927.0,7_KO8,31.htm)
8. [Accenture Interview Experience](https://www.geeksforgeeks.org/interview-experiences/accenture-interview-experience-application-developer-full-time/)
9. [Deloitte Python Developer Interview Questions](https://www.glassdoor.ca/Interview/Deloitte-Python-Developer-Interview-Questions-EI_IE2763.0,8_KO9,25.htm)
10. [Capgemini Python Developer Interview Questions](https://www.glassdoor.co.in/Interview/Capgemini-Python-Developer-Interview-Questions-EI_IE3803.0,9_KO10,26.htm)
11. [HCLTech Python Developer Interview Experience & Questions](https://www.glassdoor.com/Interview/HCLTech-Python-Developer-Interview-Questions-EI_IE553909.0,7_KO8,24.htm)
12. [Python Developer Interview Questions](https://www.glassdoor.com/Interview/python-developer-interview-questions-SRCH_KO0,16.htm)
13. [GitHub - reebaseb/Hackerrank\_ProblemSolvingBasic\_Certificate\_test-soltions: Solutions to Certification of Problem Solving Basic on Hackerrank · GitHub](https://github.com/reebaseb/Hackerrank_ProblemSolvingBasic_Certificate_test-soltions)
14. [Wipro Python Developer Interview Questions](https://www.glassdoor.ca/Interview/Wipro-Python-Developer-Interview-Questions-EI_IE9936.0,5_KO6,22.htm)
15. [I Passed Accenture HackerRank Questions in 2026: Real Questions](https://interviewfox.ai/interview-questions/accenture-hackerrank/)
16. [Deloitte interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/deloitte/deloitte-interview-experience-on-campus-mar-2025)
17. [Ernst & Young (EY) interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/ernst-young-ey/interview-experience-aug-2022-exp-0-2-years-2)
18. [Ernst & Young (EY) interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/ernst-young-ey/interview-experience-senior-software-developer-mar-2022-exp-0-2-years-2)
19. [My IBM HackerRank Assessment in 2026: What Actually Happened](https://interviewfox.ai/interview-questions/ibm-hackerrank-test/)
20. [Cognizant Interview Experience](https://www.geeksforgeeks.org/cognizant-interview-experience-set-2-campus/)
21. [TCS Python Developer Interview Questions](https://www.glassdoor.co.in/Interview/TCS-Python-Developer-Interview-Questions-EI_IE3211746.0,3_KO4,20.htm)
22. [EY Python Developer Interview Questions](https://www.glassdoor.com/Interview/EY-Python-Developer-Interview-Questions-EI_IE2784.0,2_KO3,19.htm)
23. [Accenture Python Developer Interview Questions](https://www.glassdoor.co.in/Interview/Accenture-Python-Developer-Interview-Questions-EI_IE4138.0,9_KO10,26.htm)
24. [TCS interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/tcs/interview-experience-system-engineer-jul-2022-exp-0-2-years)
25. [LTIMindtree Software Engineer Interview Questions](https://www.glassdoor.com/Interview/LTIMindtree-Software-Engineer-Interview-Questions-EI_IE8441464.0,11_KO12,29.htm)
26. [8 Python Interview Questions Developers Should Know - HackerRank Blog](https://www.hackerrank.com/blog/python-interview-questions-developers-should-know/)
27. [GitHub - anishLearnsToCode/hackerrank-python-basic-skill-test: Contains solved programs for the HackerRank Python (Basics) Skill Test Certification 🎓.](https://github.com/anishLearnsToCode/hackerrank-python-basic-skill-test)
28. [HackerRank interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/hackerrank/interview-experience-by-shivam-verma-off-campus-may-2022)
29. [Backend Developer Internship Interview Experience - GeeksforGeeks](https://www.geeksforgeeks.org/interview-experiences/backend-developer-internship-interview-experience/)
30. [GeeksforGeeks Interview Experience for Software Developer - GeeksforGeeks](https://www.geeksforgeeks.org/interview-experiences/geeksforgeeks-interview-experience-for-software-developer/)
31. [HackerRank Python Basic Certification Solutions - FREE SQL Certification](https://www.azhark.com/2023/04/07/hackerrank-python-basic-certification-solutions/)
32. [Hackerrank Python(Basic) certification question. Needed to create a shopping cart · GitHub](https://gist.github.com/ZakriaJanjua/95844e774d54cfb56796defe016ff753)
33. [Python Series. HackerRank.](https://medium.com/@j622amilah/hackerrank-tests-python-3420011863a1)
34. [HackerRank-python-basic-skill-test/shopping-cart.py at main · thekirankumarv/HackerRank-python-basic-skill-test](https://github.com/thekirankumarv/HackerRank-python-basic-skill-test/blob/main/shopping-cart.py)
35. [HackerRank-Python-Basic-Skills-Certification-Test/Average Function.py at main · MD-MAFUJUL-HASAN/HackerRank-Python-Basic-Skills-Certification-Test](https://github.com/MD-MAFUJUL-HASAN/HackerRank-Python-Basic-Skills-Certification-Test/blob/main/Average%20Function.py)
36. [GitHub - MD-MAFUJUL-HASAN/HackerRank-Python-Basic-Skills-Certification-Test: These Contain Basic Skills Certification Test Solution of Python programming language in HackerRank😏](https://github.com/MD-MAFUJUL-HASAN/HackerRank-Python-Basic-Skills-Certification-Test)
37. [Hackerrank/Certification\_Test\_Python/Basic/Multiset\_Implementation at main · sanskritilakhmani/Hackerrank](https://github.com/sanskritilakhmani/Hackerrank/blob/main/Certification_Test_Python/Basic/Multiset_Implementation)
38. [GitHub - adminazhar/HackerRank-Python-Basic-Skills-Certification-Test-Solution: Contains solved queries for the HackerRank Python (Basic) Skills Certification Test 🎓](https://github.com/adminazhar/HackerRank-Python-Basic-Skills-Certification-Test-Solution)
39. [Infosys Coding Interview Questions - GeeksforGeeks](https://www.geeksforgeeks.org/interview-prep/infosys-coding-interview-questions/)
40. [LTIMindtree Developer Interview Questions](https://www.glassdoor.co.in/Interview/LTIMindtree-Developer-Interview-Questions-EI_IE8441464.0,11_KO12,21.htm)
41. [Accenture OA (Cognitive and Technical Assessment 2023) - Questions and Answers - Discuss - LeetCode](<https://leetcode.com/discuss/interview-question/3694490/Accenture-OA-(Cognitive-and-Technical-Assessment-2023)-Questions-and-Answers/>)
42. [Deloitte interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/deloitte/interview-experience-analyst-jun-2022-exp-0-2-years)
43. [Python Interview Questions & Answers 2026 — For Freshers](https://thekiranacademy.com/python-interview-questions)
44. [120+ Top Python Interview Questions and Answers (2026) - InterviewBit](https://www.interviewbit.com/python-interview-questions/)
45. [Top Python Interview Questions Asked in Deloitte](https://whitescholars.com/top-python-interview-questions-asked-in-deloitte/)
46. [70+ Python MCQ Questions and Answers (Interview Ready)](https://www.gyansetu.in/blog/70-python-mcq-questions-and-answers-interview-ready/)
47. [Top 200 Python MCQs with Answers (2026)](https://www.igmguru.com/blog/python-mcqs)
48. [Deloitte Python interview Questions (Updated )](https://entri.app/blog/deloitte-python-interview-questions/)
49. [LTIMindtree Internship Interview Questions](https://www.glassdoor.co.in/Interview/LTIMindtree-Internship-Interview-Questions-EI_IE8441464.0,11_KO12,22.htm)
50. [Infosys Senior Software Developer Python Interview Questions](https://www.glassdoor.com/Interview/Infosys-Interview-RVW94750868.htm)
51. [Python interview questions: what each one actually predicts on the job (2026) - DEV Community](https://dev.to/fourleaf/python-interview-questions-what-each-one-actually-predicts-on-the-job-2026-27nc)
52. [Infosys Interview Question For Experienced (2023)](https://medium.com/@rana.akansha321/infosys-interview-process-question-for-experienced-2-5-years-e1f4ba6eb9b6)
53. [Python Interview Questions for Experienced (Senior) Developers: 58 Q&A](https://luminousmen.com/post/python-interview-questions-senior/)
54. [Tata Consultancy Services (TCS) interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/tata-consultancy-services-tcs/interview-experience-by-on-campus-oct-2020-2-782)
55. [Infosys private limited interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/infosys-private-limited/infosys-interview-experience-off-campus-feb-2022-2-6910)
56. [Ernst & Young (EY) interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/ernst-young-ey/interview-experience-by-vikram-kumar-gour-off-campus-jul-2022)
57. [TCS Python Developer Interview Experience & Questions](https://www.glassdoor.com/Interview/TCS-Python-Developer-Interview-Questions-EI_IE3211746.0,3_KO4,20.htm)
58. [Deloitte Software Developer Interview Experience - GeeksforGeeks](https://www.geeksforgeeks.org/interview-experiences/deloitte-software-developer-interview-experience/)
59. [Coding Assessment Test Guide 2026: HackerRank, Codility & LeetCode](https://www.careertestprep.com/knowledge/coding-assessment-test)
60. [Infosys Python Developer Interview Experience & Questions](https://www.glassdoor.com/Interview/Infosys-Python-Developer-Interview-Questions-EI_IE7927.0,7_KO8,24.htm)

---

## My Experience: Real Assessments I Attempted

> Personal log of questions I actually got in online assessments. Everything above is research on what *other* candidates reported; this section is first-hand. Add one `###` block per company, newest first, and one row to the log table.

| Date | Company | Role | # | Problem | Type | Full write-up |
|---|---|---|---|---|---|---|
| 10 Oct 2026 | Accenture | AI Engineer | Q1 | Lexicographical Binary Substring Replacement | Engineering / string simulation | [Below](#q1--lexicographical-binary-substring-replacement) |
| 10 Oct 2026 | Accenture | AI Engineer | Q2 | Consensus Orchestrator for Translation Quality Review | AI agent build (`consensus_workflow.py`) | [Short version below](#q2--consensus-orchestrator-for-translation-quality-review-short-version) · [Full doc](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md) |

### Accenture — AI Engineer (10 Oct 2026)

- **Format:** 2 questions: one pure engineering problem and one AI-agent build task.
- **My result:** _(fill in)_
- **Related prep:** [Accenture-AI-Engineer-HackerRank-Assessment.md](./Accenture-AI-Engineer-HackerRank-Assessment.md)
- **Pattern to remember:** neither question needed an ML library. Q1 tested careful reading of a simulation spec; Q2 tested deterministic control flow (validation, retries, voting, escalation, trace) around nondeterministic tools. Both reward reading the rules in order and testing the boundaries.

---

#### Q1 — Lexicographical Binary Substring Replacement

- **Category:** Strings / single-pass simulation · **Difficulty:** Easy–Medium (the difficulty is in following the rules exactly)

**Problem Description**

You are given a binary string `s` of length `n` consisting only of the characters `'0'` and `'1'`. The length of the string is not limited to 3 digits and can be arbitrarily long. Normalize the string by replacing specific 3-character substrings with their lexicographically smaller counterparts in a single pass.

Process the string from left to right using a zero-based index `i`, starting at `i = 0`. While `i <= n - 3`, examine the substring `s[i:i+3]`:

1. If it is `"110"`, replace it with `"101"` (lexicographically smaller). Then advance `i = i + 3`.
2. If it is `"111"`, leave it unchanged. Then advance `i = i + 3`.
3. Otherwise, leave the character `s[i]` unchanged and advance `i = i + 1`.

If `i > n - 3`, any remaining characters are appended as they are.

Return the fully transformed binary string after the loop terminates.

**Constraints**

- `1 <= n <= 10^5`
- `s` contains only `'0'` and `'1'`.

**Input Format:** a single line containing the binary string `s`.
**Output Format:** a single line containing the transformed string.

**Sample Input 0 / Output 0**

```
110
```
```
101
```
The whole string is `"110"`, which becomes `"101"`.

**Sample Input 1 / Output 1**

```
110111
```
```
101111
```
`"110"` becomes `"101"` (`i` jumps to 3), then `"111"` is kept as is.

**Sample Input 2 / Output 2 (longer string)**

```
011001111100
```
```
010101111010
```

| `i` | `s[i:i+3]` | Action | Next `i` |
|---|---|---|---|
| 0 | `011` | no match, keep `'0'` | 1 |
| 1 | `110` | emit `101` | 4 |
| 4 | `011` | no match, keep `'0'` | 5 |
| 5 | `111` | emit `111` | 8 |
| 8 | `110` | emit `101` | 11 |
| 11 | (`11 > 12-3`) | loop ends, append remaining `'0'` | — |

Output: `0` + `101` + `0` + `111` + `101` + `0` = `010101111010`.

**Solution**

```python
import sys


def normalize(s: str) -> str:
    n = len(s)
    out: list[str] = []          # list + join: O(n); `result += ...` in a loop is O(n²)
    i = 0
    while i <= n - 3:
        chunk = s[i : i + 3]
        if chunk == "110":
            out.append("101")
            i += 3
        elif chunk == "111":
            out.append("111")
            i += 3
        else:
            out.append(s[i])
            i += 1
    out.append(s[i:])            # tail shorter than 3 characters (may be empty)
    return "".join(out)


if __name__ == "__main__":
    print(normalize(sys.stdin.readline().strip()))
```

- **Complexity:** O(n) time, O(n) space. At `n = 10^5` this is instant.
- **Traps:**
  - **`s.replace("110", "101")` is wrong.** The spec skips 3 characters after a `"111"` block, so a `"110"` that starts *inside* a `"111"` block is never seen: `1110` stays `1110` (`replace` gives `1101`) and `11110` stays `11110` (`replace` gives `11101`). It is a left-to-right simulation, not a global substitution.
  - **Skip by 3 after a match, not by 1.** After `110 → 101`, the new characters must not be re-scanned.
  - **Don't forget the tail.** When `i > n - 3`, the last 0–2 characters must still be appended.
  - **`n < 3`:** the loop never runs, and the string comes back unchanged.
  - **Only `110 → 101` actually changes anything.** `111` is a no-op that exists purely to make `i` skip ahead.
- **Edge cases I'd test:** `1`, `10`, `11` (unchanged); `111`; `1110` → `1110`; `11110` → `11110`; `110110` → `101101`; `11011` → `10111`; all zeros; `10^5` characters of `110` repeated.

---

#### Q2 — Consensus Orchestrator for Translation Quality Review (short version)

- **Category:** AI agent build / orchestration · **Difficulty:** Medium · **File to write:** `consensus_workflow.py` · **Function:** `review()`
- **Full problem statement, 10 worked examples, 24 edge cases, boilerplate and design tradeoffs:** [Consensus Orchestrator for Translation Accenture Agent Problem.md](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md)
- **Fact vs reconstruction:** the rater list, the 7 business rules, the `QUORUM_APPROVE` reason code, the `"success"` trace status, the `approvals`/`rejections` summary, the rule that an invalid request has a null reason and an empty trace, and the failing `.status` smoke tests come from my screenshots and memory. Field names beyond those, the other reason codes and the rater interface are reconstructed assumptions. The full doc labels each one **[FACT]** or **[ASSUMPTION]**.

**Problem Description**

A localization platform machine-translates text **segments**. Before a segment ships, a panel of five automated raters reviews it, and each returns a **vote**. Implement `review()`, which runs the panel, combines the votes into one decision, and handles rater failures and missing responses clearly. The result must be deterministic and carry an accurate trace of every rater attempt.

**Provided Tools (the panel, called in this order)**

| Trace `step` | Rater | Checks |
|---|---|---|
| `accuracy` | `AccuracyRater` | translation preserves the source segment's meaning |
| `terminology` | `TerminologyRater` | domain and brand terminology is used correctly |
| `fluency` | `FluencyRater` | reads naturally in the target language |
| `localization_policy` | `LocalizationPolicyRater` | complies with locale-specific policy requirements |
| `formatting` | `FormattingRater` | placeholders, tags and layout are preserved |

Each rater exposes `rate(segment) -> RaterResponse | None`. A response has `vote` (`approve` / `reject` / `abstain`), `confidence` (0.0–1.0) and `hard_issue` (bool). A rater signals a transient outage by raising `RaterUnavailableError` or by returning `None`; both are retryable. Any other exception, or a malformed response, is **not** retried.

**Rules (evaluate in this order)**

1. **Invalid up front:** missing or blank `segment.id` or `segment.text` → status `invalid`, `reason: null`, `vote_summary: null`, `trace: []`. No rater is called.
2. **Retry:** an unavailable or missing rater is retried up to `max_retries` times (`1 + max_retries` attempts in total). **Every attempt adds one trace entry**, with `attempt` starting at 1 for each rater.
3. **Confidence filter:** only votes with `confidence >= min_confidence` count. Lower-confidence responses go into `invalid` in the summary.
4. **Hard issue:** if a counted vote has `hard_issue = true`, return `blocked` / `HARD_ISSUE` **immediately**. Raters that have not run yet are not called, so the trace holds only attempts that actually ran.
5. **Quorum:** once all raters are processed, `approvals >= approve_quorum` → `approved` / `QUORUM_APPROVE`. `rejections >= reject_quorum` → `rejected` / `QUORUM_REJECT`. If both quorums are met, escalate as a split.
6. **Escalate to a human** (`escalated`) when there is no quorum: `INSUFFICIENT_VOTERS` if too few raters responded (`responders < min_responders`), otherwise `SPLIT_NO_WINNER`.
7. **Never raise:** an unexpected internal failure or a bad config returns `errored` with an `error` message.

**Input Format** (JSON object passed to `review()`)

```json
{
  "segment": {"id": "seg-001", "text": "Speichern Sie {count} Artikel in Ihrem Warenkorb"},
  "config": {"min_confidence": 0.7, "approve_quorum": 3, "reject_quorum": 3, "max_retries": 1, "min_responders": 3}
}
```

**Output Format**

```json
{
  "segment_id": "seg-001",
  "status": "approved | rejected | blocked | escalated | errored | invalid",
  "reason": "QUORUM_APPROVE | QUORUM_REJECT | HARD_ISSUE | SPLIT_NO_WINNER | INSUFFICIENT_VOTERS | null",
  "vote_summary": {"approvals": 0, "rejections": 0, "abstentions": 0, "invalid": 0, "failed": 0, "responders": 0},
  "error": null,
  "trace": [{"step": "accuracy", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.94}]
}
```

A trace entry's `status` is `success`, `unavailable`, `missing` or `error`. A blocked, rejected, escalated or errored segment carries the matching status and reason (or `error`), plus a trace of only the attempts that ran. Tests read `result.status`, so `review()` should return a result object with attribute access and a `to_dict()` for JSON.

**Constraints**

- `0 <= max_retries <= 5`; `0.0 <= min_confidence <= 1.0`; quorums and `min_responders` between 1 and the panel size.
- Raters are called sequentially, in panel order. No global state, and the input must not be mutated.

**Sample 0: unanimous approval**

Rater behaviour: all five approve with confidence 0.94, 0.91, 0.88, 0.90, 0.97.

```json
{
  "segment_id": "seg-001", "status": "approved", "reason": "QUORUM_APPROVE",
  "vote_summary": {"approvals": 5, "rejections": 0, "abstentions": 0, "invalid": 0, "failed": 0, "responders": 5},
  "error": null,
  "trace": [
    {"step": "accuracy", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.94},
    {"step": "terminology", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.91},
    {"step": "fluency", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.88},
    {"step": "localization_policy", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.9},
    {"step": "formatting", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.97}
  ]
}
```
All five raters still run after quorum is reached, which is why `approvals` is 5.

**Sample 1: hard issue blocks immediately**

Rater behaviour: `accuracy` approves (0.93); `terminology` rejects (0.92) with `hard_issue = true`.

```json
{
  "segment_id": "seg-001", "status": "blocked", "reason": "HARD_ISSUE",
  "vote_summary": {"approvals": 1, "rejections": 1, "abstentions": 0, "invalid": 0, "failed": 0, "responders": 2},
  "error": null,
  "trace": [
    {"step": "accuracy", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.93},
    {"step": "terminology", "attempt": 1, "status": "success", "vote": "reject", "confidence": 0.92, "hard_issue": true}
  ]
}
```
`fluency`, `localization_policy` and `formatting` are never called, so their call count must be 0.

**Sample 2: retries exhausted, too few voters**

Rater behaviour: `terminology` and `localization_policy` are unavailable on every attempt; `fluency` returns `None` every time; `accuracy` and `formatting` approve.

```json
{
  "segment_id": "seg-001", "status": "escalated", "reason": "INSUFFICIENT_VOTERS",
  "vote_summary": {"approvals": 2, "rejections": 0, "abstentions": 0, "invalid": 0, "failed": 3, "responders": 2},
  "error": null,
  "trace": [
    {"step": "accuracy", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.94},
    {"step": "terminology", "attempt": 1, "status": "unavailable"},
    {"step": "terminology", "attempt": 2, "status": "unavailable"},
    {"step": "fluency", "attempt": 1, "status": "missing"},
    {"step": "fluency", "attempt": 2, "status": "missing"},
    {"step": "localization_policy", "attempt": 1, "status": "unavailable"},
    {"step": "localization_policy", "attempt": 2, "status": "unavailable"},
    {"step": "formatting", "attempt": 1, "status": "success", "vote": "approve", "confidence": 0.97}
  ]
}
```
There are only 2 approvals (< 3) and 2 responders (< `min_responders` 3).

**Sample 3: invalid request**

Input segment: `{"id": "seg-002", "text": "   "}`

```json
{"segment_id": "seg-002", "status": "invalid", "reason": null, "vote_summary": null,
 "error": "INVALID_REQUEST: segment.id and segment.text are required", "trace": []}
```

**Edge cases to check first** (24 in the full doc)

- `confidence == min_confidence` counts (`>=`).
- A hard issue on a **low-confidence** vote: ignored here because the confidence filter runs first. This is the biggest ambiguity, so re-read the spec and flip it if the tests disagree.
- A hard issue that arrives on a **retry** still blocks, and the earlier failed attempts stay in the trace.
- `max_retries = 0` means exactly one attempt per rater (`range(max_retries)` gives zero attempts).
- Both quorums met at once: escalate as a split, never "first check wins".
- Whitespace-only `id` or `text` is invalid. Booleans are not valid ints for config fields.
- Mutable default arguments (`trace=[]`) leak the trace between calls.
- Return a result object on **every** path. My failing smoke tests showed `'NoneType' object has no attribute 'status'`, which most likely means `review()` still returned `None`; start by returning a placeholder result everywhere, then fill in the rules in order.

**Skeleton** (full typed boilerplate, mock harness and pytest file are in the [full doc](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md#10-boilerplate))

```python
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def review(request: Mapping[str, Any], panel: Sequence["Rater"]) -> "ReviewResult":
    # 1 validate request -> invalid | 2 validate config -> errored
    # 3 per rater (in order): attempts with retries -> one trace entry per attempt
    # 4 confidence filter -> 5 hard issue short-circuit -> 6 quorum -> 7 escalation
    raise NotImplementedError
```

**Where to go deeper (in the full doc)**

- [Part 1: closest public analogues and the "no public copy found" check](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md#part-1-research-findings)
- [Rules in strict order of evaluation](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md#3-rules-precise-in-order-of-evaluation) and [output contract](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md#5-output-contract)
- [10 worked samples](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md#6-sample-cases) and [24 edge cases](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md#7-edge-cases-and-ambiguities-to-consider)
- [Part 3: design tradeoffs (sequential vs async, veto, retries, trace as an event log)](./Consensus%20Orchestrator%20for%20Translation%20Accenture%20Agent%20Problem.md#part-3-design-and-engineering-tradeoffs-for-a-reacttsnode-engineer-moving-into-genai-architecture)
