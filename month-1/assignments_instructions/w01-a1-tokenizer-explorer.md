# Assignment 1.1: Tokenizer Explorer

> **Week 1 · Lesson 1.3 & 1.4** | Focus: BPE tokenization, multilingual token cost, cosine similarity

## Objective

Build a Python script that uses real tokenizers to see how LLMs break text into tokens — across models, across languages, and across semantic concepts. By the end you will have concrete intuition for why tokenization affects cost, context windows, and multilingual performance.

## Difficulty
Beginner-Intermediate

## Estimated Time
2–3 hours

## Prerequisites
- Python 3.12+ and UV installed
- Basic Python (functions, dataclasses, loops, dicts)
- Week 1 lessons 1.3 and 1.4 read

## Why This Matters
Every time you call an LLM API, text is tokenized first. The number of tokens directly determines cost and context window usage. Different languages tokenize very differently — a Japanese sentence that means the same thing as an English one can cost 2–3× more tokens. Understanding this at the code level removes it from being an abstract concept.

---

## Part 1: Project Setup (10 min)

Create the project with UV:

```bash
uv init tokenizer-explorer
cd tokenizer-explorer
```

Add dependencies:

```bash
uv add tiktoken numpy
uv add --dev ruff mypy
```

Create your working file:

```bash
touch explorer.py
```

Final `pyproject.toml` dependencies section:

```toml
[project]
name = "tokenizer-explorer"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "tiktoken>=0.7.0",
    "numpy>=1.26.0",
    "openai>=1.30.0",
    "python-dotenv>=1.0.0",
]

[dependency-groups]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
```

---

## Part 2: Tokenizer Wrapper (30 min)

In `explorer.py`, build a simple, consistent tokenizer interface using `tiktoken`.

```python
from dataclasses import dataclass
import tiktoken


@dataclass
class TokenResult:
    model_name: str
    text: str
    token_ids: list[int]
    token_strings: list[str]

    @property
    def count(self) -> int:
        return len(self.token_ids)


def tokenize(text: str, model: str = "gpt-4o") -> TokenResult:
    """Tokenize text using the specified OpenAI model's tokenizer."""
    enc = tiktoken.encoding_for_model(model)
    token_ids = enc.encode(text)
    token_strings = [enc.decode([tid]) for tid in token_ids]
    return TokenResult(
        model_name=model,
        text=text,
        token_ids=token_ids,
        token_strings=token_strings,
    )
```

**Verify it works** — run this at the bottom of the file:

```python
if __name__ == "__main__":
    result = tokenize("Hello, how are you?")
    print(f"Model:   {result.model_name}")
    print(f"Tokens:  {result.count}")
    print(f"IDs:     {result.token_ids}")
    print(f"Strings: {result.token_strings}")
```

Expected output (approximate — exact IDs depend on model version):

```
Model:   gpt-4o
Tokens:  6
IDs:     [9906, 11, 1268, 527, 499, 30]
Strings: ['Hello', ',', ' how', ' are', ' you', '?']
```

**What to notice:**
- A single space before a word is part of the token (` how`, not `how`)
- Punctuation usually gets its own token
- Capitalization affects the token ID

---

## Part 3: Multilingual Token Exploration (45 min)

This part directly demonstrates the BPE concept from Lesson 1.3: tokenizers trained on English-heavy data are inefficient for other languages.

### 3.1 — Define the sample dictionary

Add this to `explorer.py`:

```python
type MultiLangDict = dict[str, dict[str, str]]

MULTILINGUAL_SAMPLES: MultiLangDict = {
    "greeting": {
        "en": "Hello, how are you?",
        "ja": "こんにちは、お元気ですか？",
        "ar": "مرحبا، كيف حالك؟",
        "ko": "안녕하세요, 어떻게 지내세요?",
        "zh": "你好，你怎么样？",
        "de": "Hallo, wie geht es Ihnen?",
        "hi": "नमस्ते, आप कैसे हैं?",
        "ru": "Здравствуйте, как дела?",
    },
    "code": {
        "python": "def hello():\n    return 'world'",
        "javascript": "const hello = () => 'world';",
        "sql": "SELECT name FROM users WHERE active = true;",
    },
}
```

### 3.2 — Iterate and print token counts

Write a function that iterates the dictionary and prints the token count and IDs for each entry:

```python
def explore_multilingual(samples: MultiLangDict, model: str = "gpt-4o") -> None:
    """
    For each concept in the sample dictionary, tokenize every language/variant
    and print the token count, ratio vs English baseline, and raw token IDs.
    """
    for concept, variants in samples.items():
        print(f"\n{'='*60}")
        print(f"CONCEPT: {concept.upper()}")
        print(f"{'='*60}")

        # Get English (or first key) as baseline
        baseline_key = "en" if "en" in variants else next(iter(variants))
        baseline = tokenize(variants[baseline_key], model)
        print(f"[baseline: {baseline_key}]  {baseline.count} tokens\n")

        for lang, text in variants.items():
            result = tokenize(text, model)
            ratio = result.count / baseline.count
            print(f"  {lang:>12}  |  tokens: {result.count:>3}  |  ratio: {ratio:.2f}x  |  {text[:40]}")
            print(f"              |  IDs: {result.token_ids[:8]}{'...' if len(result.token_ids) > 8 else ''}")
```

Call it in `__main__`:

```python
explore_multilingual(MULTILINGUAL_SAMPLES)
```

### 3.3 — What to observe

Run it and answer these questions in a comment block at the top of the file:

```python
"""
OBSERVATIONS (fill in after running):

1. Which language used the most tokens for the greeting? How many times more than English?
2. German is also Latin-script — how does it compare to English token count?
3. Look at the token IDs for Japanese vs English. What do you notice about the ID ranges?
4. The code variants have similar syntax — which language uses the fewest tokens and why?
5. What does this tell you about the cost difference when building a multilingual chatbot?
"""
```

**Engineering implication:** If your app serves Japanese users and you prompt in Japanese, your context window fills up 2–3x faster and your API bill is 2–3x higher for the same semantic content. This is a real production concern, not an academic one.

---

## Part 4: Cosine Similarity — Seeing Meaning in Vector Space (30 min)

Lesson 1.4 explained that embeddings are vectors where direction encodes meaning, and cosine similarity measures how aligned two vectors are. This exercise makes that concrete: you will call the OpenAI Embeddings API to embed a few hand-picked sentences, then manually compare pairs to see that the scores match semantic intuition.

No complex iteration here — just embed, compare, observe.

### 4.0 — Setup: packages and API key

**Step 1 — Add the required packages**

You need two new packages. Run these in your terminal from inside the `tokenizer-explorer` directory:

```bash
uv add openai python-dotenv
```

- `openai` — the official Python client for all OpenAI APIs, including embeddings
- `python-dotenv` — loads environment variables from a `.env` file so your API key never gets hardcoded in source code

After running, you should see both appear in `pyproject.toml` under `dependencies`.

**Step 2 — Create a `.env` file**

In the root of your project (same folder as `pyproject.toml`), create a file named `.env`:

```
OPENAI_API_KEY=sk-...your-key-here...
```

> **CRITICAL — never commit this file.** Check that `.gitignore` already has `.env` listed. If not, add it manually. Leaked API keys get abused within minutes and you will be billed.

**Step 3 — Add `.env` to `.gitignore`**

Open `.gitignore` (UV creates one automatically) and confirm this line is present:

```
.env
```

If it is missing, add it now before writing any code.

**Step 4 — Verify the key loads correctly**

Before building the full function, test the setup with a quick one-liner in your terminal:

```bash
uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(bool(os.getenv('OPENAI_API_KEY')))"
```

This should print `True`. If it prints `False`, the `.env` file is missing or in the wrong location.

---

### 4.1 — Understand the theory before writing code

Before you type anything, make sure you can answer these from Lesson 1.4:

- What does it mean for two vectors to be "close" in embedding space?
- Why does dot product equal cosine similarity when vectors are unit-normalized?
- What is `text-embedding-3-small`? Why is it cheaper than `text-embedding-3-large`?

Keep these in mind as you read the scores your code produces.

### 4.2 — Add the embedding helpers

At the top of `explorer.py`, add these imports alongside your existing ones:

```python
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
```

Then, before any function definitions, load the environment and initialize the client:

```python
load_dotenv()                 # reads .env file into os.environ
client = OpenAI()             # automatically reads OPENAI_API_KEY from environment
```

Now add the two helper functions:

```python
def get_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> np.ndarray:
    """
    Calls the OpenAI Embeddings API and returns a 2D numpy array.
    text-embedding-3-small outputs 1536-dimensional vectors.
    OpenAI embeddings are already unit-normalized, so
    dot product between any two rows = their cosine similarity.
    """
    response = client.embeddings.create(input=texts, model=model)
    vectors = [item.embedding for item in response.data]
    return np.array(vectors, dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Cosine similarity between two pre-normalized vectors.
    Because OpenAI embeddings are unit vectors, this is just the dot product.
    Score range: 0.0 (unrelated) → 1.0 (identical meaning).
    """
    return float(np.dot(a, b))
```

> **Why one batch call instead of one call per sentence?** `client.embeddings.create(input=texts, ...)` accepts a list and returns all embeddings in a single API round-trip. This is faster and cheaper than calling it 4 times in a loop.

> **Why are OpenAI embeddings already normalized?** OpenAI's embedding models return unit vectors by default — you do not need to normalize them yourself. This means `np.dot(a, b)` directly gives cosine similarity with no extra math.

### 4.3 — Define sentences with known similarity relationships

Add these four sentences to `explorer.py`. They are designed so you already have an intuition about which pairs should be close and which should not be:

```python
SIMILARITY_SAMPLES: list[tuple[str, str]] = [
    # label, text
    ("dog_1",   "The dog ran across the park"),
    ("dog_2",   "A puppy sprinted through the field"),
    ("weather", "It is raining heavily outside today"),
    ("code",    "def add(a, b): return a + b"),
]
```

Before running, write down your prediction: which two sentences do you think will have the highest cosine similarity? Which will be the lowest?

### 4.4 — Embed and compare pairs

Write a function that:
1. Embeds all four sentences in one batch call (efficient — one model load)
2. Prints the embedding shape so you can see what a "vector" actually is
3. Computes cosine similarity for specific pairs that test your intuition

```python
def explore_similarity(samples: list[tuple[str, str]]) -> None:
    """
    Embed a small set of sentences and compare specific pairs.
    Goal: confirm that cosine similarity matches semantic intuition.
    """
    labels = [label for label, _ in samples]
    texts  = [text  for _, text  in samples]

    # Step 1: Embed all texts at once
    embeddings = get_embeddings(texts)
    print(f"\nEmbedding shape: {embeddings.shape}")
    print(f"  → {embeddings.shape[0]} sentences, each a {embeddings.shape[1]}-dimensional vector\n")

    # Step 2: Build a simple index so we can look up by label
    idx = {label: i for i, label in enumerate(labels)}

    # Step 3: Compare specific pairs
    pairs_to_compare = [
        ("dog_1",   "dog_2"),    # Should be HIGH — same concept, different words
        ("dog_1",   "weather"),  # Should be LOW — unrelated topics
        ("dog_1",   "code"),     # Should be VERY LOW — completely different domains
        ("dog_2",   "weather"),  # Middle ground
    ]

    print("Pairwise cosine similarity:")
    print(f"  {'Pair':<30}  Score")
    print(f"  {'-'*30}  -----")
    for label_a, label_b in pairs_to_compare:
        sim = cosine_similarity(embeddings[idx[label_a]], embeddings[idx[label_b]])
        print(f"  {label_a} ↔ {label_b:<18}  {sim:.4f}")
```

Call it in `__main__`:

```python
explore_similarity(SIMILARITY_SAMPLES)
```

### 4.5 — What to observe

After running, fill in this comment block:

```python
"""
SIMILARITY OBSERVATIONS (fill in after running):

1. What shape did the embedding array have (rows × columns)? What does the 1536 represent?
2. Was your prediction correct about which pair would be most similar?
3. dog_1 and dog_2 use completely different words — why is their score still high?
4. The code sentence has a very low score vs everything else. Why does code
   live in a different neighborhood of vector space than natural language?
5. The score is never exactly 0 or 1 (unless sentences are identical). Why not?
"""
```

**The key insight:** Cosine similarity measures direction, not word overlap. Two sentences can share zero tokens and still score 0.8+ because the embedding model has learned that "dog ran" and "puppy sprinted" point in the same direction in meaning-space. This is exactly why vector search works — you search by meaning, not keywords.

---

## Full `__main__` Block

```python
if __name__ == "__main__":
    print("\n--- PART 2: Tokenizer Wrapper Sanity Check ---")
    result = tokenize("Hello, how are you?")
    print(f"Model: {result.model_name} | Tokens: {result.count}")
    print(f"IDs:     {result.token_ids}")
    print(f"Strings: {result.token_strings}")

    print("\n--- PART 3: Multilingual Token Exploration ---")
    explore_multilingual(MULTILINGUAL_SAMPLES)

    print("\n--- PART 4: Cosine Similarity Exploration ---")
    explore_similarity(SIMILARITY_SAMPLES)
```

Run everything with:

```bash
uv run python explorer.py
```

---

## Expected Output (abbreviated)

```
--- PART 3: Multilingual Token Exploration ---

============================================================
CONCEPT: GREETING
============================================================
[baseline: en]  6 tokens

          en  |  tokens:   6  |  ratio: 1.00x  |  Hello, how are you?
              |  IDs: [9906, 11, 1268, 527, 499, 30]
          ja  |  tokens:  14  |  ratio: 2.33x  |  こんにちは、お元気ですか？
              |  IDs: [4955, 25775, 3393, 27091, ...]
          de  |  tokens:   7  |  ratio: 1.17x  |  Hallo, wie geht es Ihnen?
              |  IDs: [39, 38, ...]

--- PART 4: Cosine Similarity Exploration ---

Embedding shape: (4, 1536)
  → 4 sentences, each a 1536-dimensional vector

Pairwise cosine similarity:
  Pair                            Score
  ------------------------------  -----
  dog_1 ↔ dog_2                   0.8741
  dog_1 ↔ weather                 0.2103
  dog_1 ↔ code                    0.0892
  dog_2 ↔ weather                 0.1934
```

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **Part 2 working** | 25% | `tokenize()` returns correct token IDs and strings |
| **Part 3 output** | 30% | Correct iteration, ratio vs baseline, IDs printed per variant |
| **Part 4 output** | 30% | Embedding shape printed, all 4 pairs compared with correct scores |
| **Observations filled in** | 15% | Both comment blocks answered in your own words |

---

## Key Concepts This Assignment Reinforces

- **BPE tokenization**: Why non-Latin scripts use more tokens per semantic unit
- **Token IDs**: The actual integers the model processes, not the text
- **Cosine similarity**: Direction-based comparison of meaning vectors
- **Tokens ≠ meaning**: Same meaning, completely different tokens (en vs ja greeting)
- **Embeddings capture semantics**: High similarity despite zero token overlap
