"""Accenture AI Engineer HackerRank practice - reference solutions + self-tests.

Run:  uv run python accenture_practice_solutions.py   (or: python accenture_practice_solutions.py)
Every assert below is a test case. Try each problem yourself first, then compare.
"""

from __future__ import annotations

import heapq
import math
import re
from abc import ABC, abstractmethod
from collections import Counter, OrderedDict, defaultdict
from collections.abc import Iterable, Sequence

# =====================================================================
# PART A - Problems REPORTED by candidates (InterviewFox, Java track, low confidence)
# =====================================================================


# A1. Minimum CPU Cores (inclusive end times)
def min_cpu_cores(processes: Sequence[tuple[int, int]]) -> int:
    """Max number of processes running at the same instant. End time is inclusive."""
    events: list[tuple[int, int]] = []
    for start, end in processes:
        events.append((start, +1))
        events.append((end + 1, -1))  # inclusive end -> process frees the core at end + 1
    events.sort()  # at equal time, -1 sorts before +1 -> free before allocate
    running = peak = 0
    for _, delta in events:
        running += delta
        peak = max(peak, running)
    return peak


def min_cpu_cores_heap(processes: Sequence[tuple[int, int]]) -> int:
    """Alternative: sort by start, min-heap of end times."""
    ends: list[int] = []
    for start, end in sorted(processes):
        if ends and ends[0] < start:  # strictly less: inclusive end still overlaps
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)


# A2. Password Sanitizer
def sanitize_passwords(line: str) -> str:
    """Keep passwords with len >= 5 that are not all letters and not all digits."""
    MIN_LEN = 5
    valid = [
        p for p in line.split()
        if len(p) >= MIN_LEN and not p.isalpha() and not p.isdigit()
    ]
    return " ".join(valid)


# A3. Desired Array: sum of the k smallest positive integers not divisible by any element
def desired_array_sum(k: int, arr: Sequence[int]) -> int:
    divisors = sorted(set(arr))
    if 1 in divisors:
        raise ValueError("1 divides everything - no valid number exists")
    # Drop divisors that are multiples of a smaller divisor (they add nothing)
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


# A4. Majority Element (Boyer-Moore voting)
def majority_element(nums: Sequence[int]) -> int:
    candidate, count = 0, 0
    for n in nums:
        if count == 0:
            candidate = n
        count += 1 if n == candidate else -1
    return candidate  # problem guarantees a majority exists; verify with nums.count if not


# =====================================================================
# PART B - Practice problems modelled on REPORTED topics (not actual Accenture questions)
# =====================================================================


# B1. Strings/dict - first non-repeating character index (-1 if none)
def first_unique_char(s: str) -> int:
    counts = Counter(s)
    return next((i for i, ch in enumerate(s) if counts[ch] == 1), -1)


# B2. Dict - group anagrams (preserve first-seen group order)
def group_anagrams(words: Iterable[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())


# B3. Intervals - merge overlapping (closed intervals; touching ones merge)
def merge_intervals(intervals: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(s, e) for s, e in merged]


# B4. Sliding window - longest substring without repeating characters
def longest_unique_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, ch in enumerate(s):
        if last_seen.get(ch, -1) >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


# B5. Sliding window - max sum of any subarray of size k
def max_window_sum(nums: Sequence[int], k: int) -> int:
    if not 0 < k <= len(nums):
        raise ValueError("k must be in 1..len(nums)")
    window = best = sum(nums[:k])
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


# B6. Sorting with custom key - top k frequent words (freq desc, then alphabetical)
def top_k_frequent_words(words: Sequence[str], k: int) -> list[str]:
    counts = Counter(words)
    return sorted(counts, key=lambda w: (-counts[w], w))[:k]


# B7. Comparator sort (Java "comparator sort" equivalent)
#     dept asc, salary desc, name asc
def sort_employees(rows: Sequence[tuple[str, str, int]]) -> list[tuple[str, str, int]]:
    return sorted(rows, key=lambda r: (r[1], -r[2], r[0]))


# B8. Dict - count pairs summing to target (i < j)
def count_pairs_with_sum(nums: Sequence[int], target: int) -> int:
    seen: Counter[int] = Counter()
    pairs = 0
    for n in nums:
        pairs += seen[target - n]
        seen[n] += 1
    return pairs


# B9. Stack - balanced brackets
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


# B10. String - run-length compression, return original if not shorter
def compress(s: str) -> str:
    if not s:
        return s
    parts: list[str] = []
    run_char, run_len = s[0], 1
    for ch in s[1:]:
        if ch == run_char:
            run_len += 1
        else:
            parts.append(f"{run_char}{run_len}")
            run_char, run_len = ch, 1
    parts.append(f"{run_char}{run_len}")
    out = "".join(parts)
    return out if len(out) < len(s) else s


# B11. Arrays - product of array except self (no division)
def product_except_self(nums: Sequence[int]) -> list[int]:
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


# B12. Arrays - second largest DISTINCT value (None if absent)
def second_largest(nums: Iterable[int]) -> int | None:
    first = second = None
    for n in nums:
        if first is None or n > first:
            first, second = n, first
        elif n != first and (second is None or n > second):
            second = n
    return second


# B13. Arrays - move zeros to end, keep order, in place
def move_zeros(nums: list[int]) -> list[int]:
    write = 0
    for x in nums:
        if x != 0:
            nums[write] = x
            write += 1
    nums[write:] = [0] * (len(nums) - write)
    return nums


# B14. Dict/parsing - error count per service from log lines, sorted by count desc then name
LOG_PATTERN = re.compile(r"^\S+ \S+ (?P<level>[A-Z]+) \[(?P<service>[\w-]+)\]")


def errors_per_service(lines: Iterable[str]) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for line in lines:
        m = LOG_PATTERN.match(line)
        if m and m["level"] == "ERROR":
            counts[m["service"]] += 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


# B15. OOP - LRU cache
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
            self._data.popitem(last=False)


# B16. OOP - abstract base class + inheritance + polymorphism + dunder
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    def __lt__(self, other: Shape) -> bool:
        return self.area() < other.area()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(area={self.area():.2f})"


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width, self.height = width, height

    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side: float) -> None:
        super().__init__(side, side)


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius**2


# B17. OOP - bank account with validation and custom exception
class InsufficientFundsError(Exception):
    pass


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
            raise InsufficientFundsError(f"balance {self._balance} < {amount}")
        self._balance -= amount


# B18. AI-flavoured - word chunker with overlap (RAG chunking)
def chunk_words(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("need chunk_size > 0 and 0 <= overlap < chunk_size")
    words = text.split()
    step = chunk_size - overlap
    chunks: list[str] = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_size]))
        if start + chunk_size >= len(words):
            break
    return chunks


# B19. AI-flavoured - top-k retrieval by cosine similarity (pure Python)
def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return 0.0 if norm == 0 else dot / norm


def top_k_similar(query: Sequence[float], docs: dict[str, Sequence[float]], k: int) -> list[str]:
    scored = ((cosine(query, vec), doc_id) for doc_id, vec in docs.items())
    return [doc_id for _, doc_id in heapq.nlargest(k, scored)]


# B20. Dict - rate limiter: allow at most `limit` requests per user in any `window` seconds
def rate_limit(requests: Sequence[tuple[int, str]], limit: int, window: int) -> list[bool]:
    from collections import deque

    history: dict[str, deque[int]] = defaultdict(deque)
    decisions: list[bool] = []
    for ts, user in requests:
        q = history[user]
        while q and q[0] <= ts - window:
            q.popleft()
        if len(q) < limit:
            q.append(ts)
            decisions.append(True)
        else:
            decisions.append(False)
    return decisions


# =====================================================================
# Tests
# =====================================================================


def _run_tests() -> None:
    # A1
    for fn in (min_cpu_cores, min_cpu_cores_heap):
        assert fn([(0, 3), (3, 5), (2, 6)]) == 3
        assert fn([(1, 2), (3, 4), (5, 6)]) == 1
        assert fn([(1, 2), (2, 3)]) == 2  # inclusive end overlaps
        assert fn([(1, 10), (2, 3), (4, 5), (6, 7)]) == 2
        assert fn([]) == 0
    # A2
    assert sanitize_passwords("abc123 abcd 123456 Passw0rd abcdef") == "abc123 Passw0rd"
    assert sanitize_passwords("a!b@c# 12345 hello") == "a!b@c#"
    assert sanitize_passwords("") == ""
    # A3
    assert desired_array_sum(4, [2, 3, 4, 5, 6]) == 32
    assert desired_array_sum(3, [2]) == 1 + 3 + 5
    assert desired_array_sum(2, [4, 6]) == 1 + 2
    # A4
    assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2
    assert majority_element([3, 3, 4]) == 3
    # B
    assert first_unique_char("leetcode") == 0
    assert first_unique_char("loveleetcode") == 2
    assert first_unique_char("aabb") == -1
    assert group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    assert merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]) == [(1, 6), (8, 10), (15, 18)]
    assert merge_intervals([(1, 4), (4, 5)]) == [(1, 5)]
    assert longest_unique_substring("abcabcbb") == 3
    assert longest_unique_substring("pwwkew") == 3
    assert longest_unique_substring("abba") == 2
    assert max_window_sum([2, 1, 5, 1, 3, 2], 3) == 9
    assert top_k_frequent_words(["i", "love", "ai", "i", "love", "code"], 2) == ["i", "love"]
    assert top_k_frequent_words(["b", "a", "c", "a", "b"], 2) == ["a", "b"]
    emps = [("Asha", "Eng", 90), ("Ravi", "Eng", 120), ("Bina", "Ops", 80), ("Arun", "Eng", 120)]
    assert sort_employees(emps) == [("Arun", "Eng", 120), ("Ravi", "Eng", 120), ("Asha", "Eng", 90), ("Bina", "Ops", 80)]
    assert count_pairs_with_sum([1, 5, 7, -1, 5], 6) == 3
    assert count_pairs_with_sum([1, 1, 1, 1], 2) == 6
    assert is_balanced("{[()]}") and not is_balanced("([)]") and not is_balanced("((")
    assert compress("aabcccccaaa") == "a2b1c5a3"
    assert compress("abc") == "abc"
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([0, 1, 2]) == [2, 0, 0]
    assert second_largest([10, 5, 10, 8]) == 8
    assert second_largest([7, 7]) is None
    assert move_zeros([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]
    logs = [
        "2026-10-07 10:00:01 ERROR [auth] token expired",
        "2026-10-07 10:00:02 INFO [auth] login ok",
        "2026-10-07 10:00:03 ERROR [billing] timeout",
        "2026-10-07 10:00:04 ERROR [auth] bad signature",
        "malformed line",
    ]
    assert errors_per_service(logs) == [("auth", 2), ("billing", 1)]
    cache = LRUCache(2)
    cache.put(1, 1); cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts 2
    assert cache.get(2) == -1 and cache.get(3) == 3
    shapes = [Circle(1), Square(2), Rectangle(1, 2)]
    assert [type(s).__name__ for s in sorted(shapes)] == ["Rectangle", "Circle", "Square"]
    acct = BankAccount("Kamran", 100)
    acct.deposit(50); acct.withdraw(30)
    assert acct.balance == 120
    try:
        acct.withdraw(500)
        raise AssertionError("expected InsufficientFundsError")
    except InsufficientFundsError:
        pass
    assert chunk_words("a b c d e f g", 3, 1) == ["a b c", "c d e", "e f g"]
    assert chunk_words("a b c d", 3, 0) == ["a b c", "d"]
    docs = {"d1": [1.0, 0.0], "d2": [0.7, 0.7], "d3": [0.0, 1.0]}
    assert top_k_similar([1.0, 0.1], docs, 2) == ["d1", "d2"]
    assert rate_limit([(1, "u"), (2, "u"), (3, "u"), (11, "u"), (3, "v")], 2, 10) == [True, True, False, True, True]
    print("All tests passed.")


if __name__ == "__main__":
    _run_tests()
