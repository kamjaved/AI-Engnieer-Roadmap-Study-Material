# Assignment 1.2: Embedding Playground

> **Week 1** | [Back to Week 1 Plan](../week-1.md)
> **Tooling updated:** `pip` → `uv` · `setup.py` → `pyproject.toml` · `flake8/black` → `ruff`

## Title
**Embedding Playground** — Making Machines Understand Meaning

## Objective
Build a Python script that generates text embeddings, computes semantic similarity between sentences, performs vector arithmetic (the classic king − man + woman = queen experiment), and visualizes high-dimensional embeddings in 2D. You will develop an intuition for how LLMs represent meaning as numbers.

## Difficulty
Beginner-Intermediate

## Estimated Time
3–4 hours

## Prerequisites
- Python 3.12+ installed
- UV package manager installed (see `python-env-setup.md`)
- VSCode with Pylance, Ruff, and Jupyter extensions installed
- Basic understanding of vectors (direction + magnitude)
- Familiarity with numpy arrays
- **Optional**: OpenAI API key (for comparing OpenAI embeddings vs local models)

## Why This Matters
Embeddings are the backbone of modern AI applications:
- **Semantic search**: Finding relevant documents by meaning, not keywords
- **RAG (Retrieval-Augmented Generation)**: The retrieval step relies entirely on embeddings
- **Recommendation systems**: "Users who liked X also liked Y"
- **Clustering and classification**: Grouping similar content automatically

Every GenAI engineer needs to understand embeddings deeply. This is not optional knowledge.

---

## Detailed Instructions

### Step 1: Project Setup (10 min)

> **Change from original:** Replaced `pip install` with `uv add` and `requirements.txt` project pattern with `uv init` + `pyproject.toml`. The original required manually creating all folders and files. UV's init scaffolds the base structure for you.

Create and enter your project:

```bash
uv init embedding-playground
cd embedding-playground
```

Add production dependencies:

```bash
uv add sentence-transformers numpy scikit-learn matplotlib seaborn
```

Add development dependencies:

```bash
uv add --dev ruff mypy pytest ipykernel
```

> **Jupyter kernel setup:** The visualizations in this assignment work very well in a notebook. Register the project kernel so VSCode's Jupyter extension can find it:
> ```bash
> uv run python -m ipykernel install --user --name="embedding-playground"
> ```
> Then open a new `.ipynb` file in VSCode and select the `embedding-playground` kernel from the top-right.

Create the package structure:

```bash
mkdir embedding_playground
touch embedding_playground/__init__.py
touch embedding_playground/embedder.py
touch embedding_playground/similarity.py
touch embedding_playground/arithmetic.py
touch embedding_playground/visualizer.py
touch embedding_playground/cli.py
mkdir data
touch data/sentences.json
```

Your final layout:

```
embedding-playground/
  embedding_playground/
    __init__.py
    embedder.py
    similarity.py
    arithmetic.py
    visualizer.py
    cli.py
  data/
    sentences.json
  explore.ipynb        ← create this for interactive exploration
  pyproject.toml
  uv.lock
  README.md
  .gitignore
```

Update `pyproject.toml` to add tooling config:

```toml
[project]
name = "embedding-playground"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "sentence-transformers>=3.0.0",
    "numpy>=1.26.0",
    "scikit-learn>=1.5.0",
    "matplotlib>=3.9.0",
    "seaborn>=0.13.0",
]

[dependency-groups]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pytest>=8.2.0",
    "ipykernel>=6.29.0",
]

# Only needed if you have an OpenAI API key
# uv add openai pydantic-settings
# then add to [project] dependencies above

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.12"
ignore_missing_imports = true  # sentence-transformers has incomplete stubs
```

Create `data/sentences.json`:

```json
{
  "similar_pairs": [
    ["The cat sat on the mat", "A feline rested on the rug"],
    ["Python is a programming language", "Python is used for coding software"],
    ["The stock market crashed today", "Financial markets saw a major downturn"]
  ],
  "dissimilar_pairs": [
    ["The cat sat on the mat", "The stock market crashed today"],
    ["I love eating pizza", "Quantum mechanics is complex"]
  ],
  "semantic_groups": {
    "animals": [
      "The dog chased the ball",
      "Cats are independent creatures",
      "The parrot repeated every word"
    ],
    "technology": [
      "The server went down at midnight",
      "We deployed the new API",
      "The database needs indexing"
    ],
    "food": [
      "The pasta was perfectly al dente",
      "She baked a chocolate cake",
      "Fresh sushi is unbeatable"
    ],
    "sports": [
      "The goalkeeper made an incredible save",
      "She scored a three-pointer at the buzzer",
      "The marathon runner hit the wall at mile 20"
    ]
  }
}
```

---

### Step 2: Build the Embedding Engine (30 min)

In `embedder.py`, create a class that supports multiple embedding models:

```python
from typing import Protocol

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel(Protocol):
    """Protocol defining the interface all embedding models must implement."""

    def embed(self, texts: list[str]) -> np.ndarray:
        """Return embeddings as numpy array of shape (n_texts, dim)."""
        ...

    @property
    def dimension(self) -> int:
        ...

    @property
    def name(self) -> str:
        ...


class LocalEmbedder:
    """Uses sentence-transformers (free, runs locally, no API key needed)."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model = SentenceTransformer(model_name)
        self._name = model_name

    def embed(self, texts: list[str]) -> np.ndarray:
        # normalize_embeddings=True gives unit-length vectors
        # This means cosine similarity == dot product (faster)
        return self.model.encode(texts, normalize_embeddings=True)

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    @property
    def name(self) -> str:
        return self._name
```

> **Model note:** `all-MiniLM-L6-v2` (384 dimensions) is the go-to local model for quick experiments — small and fast. For higher quality, use `BAAI/bge-large-en-v1.5` (1024d). Check the **MTEB Leaderboard** at `huggingface.co/spaces/mteb/leaderboard` for the current best models — it changes frequently.

If you have an OpenAI API key, also implement:

```python
class OpenAIEmbedder:
    """Uses OpenAI's embedding API (requires OPENAI_API_KEY env var)."""

    def __init__(self, model: str = "text-embedding-3-small") -> None:
        from openai import OpenAI

        self.client = OpenAI()  # reads OPENAI_API_KEY from environment automatically
        self._model = model
        # text-embedding-3-small supports Matryoshka — can truncate to any dim
        self._dimension = 1536

    def embed(self, texts: list[str]) -> np.ndarray:
        response = self.client.embeddings.create(input=texts, model=self._model)
        return np.array([item.embedding for item in response.data])

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def name(self) -> str:
        return self._model
```

> **API key setup:** If you are using the OpenAI embedder, put your API key in a `.env` file at the project root. Add `.env` to `.gitignore`. Load it with `pydantic-settings` (see `python-env-setup.md`) or simply set the `OPENAI_API_KEY` environment variable in your shell. The OpenAI SDK reads it automatically.
>
> Install the optional dependencies:
> ```bash
> uv add openai pydantic-settings
> ```

---

### Step 3: Implement Similarity Computation (30 min)

In `similarity.py`:

```python
import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two 1D vectors. Returns value in [-1, 1]."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Compute Euclidean distance between two vectors."""
    return float(np.linalg.norm(a - b))


def similarity_matrix(embeddings: np.ndarray, labels: list[str]) -> dict[str, object]:
    """Compute all pairwise cosine similarities. Returns matrix and labels."""
    n = len(embeddings)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = cosine_similarity(embeddings[i], embeddings[j])
    return {"matrix": matrix, "labels": labels}
```

> **Performance note:** For large embedding sets, computing similarity with a Python loop is slow. The vectorized form is `embeddings @ embeddings.T` (a single matrix multiplication) — give this a try as an optimization once the basic version works.

Build a function that produces a clear similarity report for the test pairs from your JSON:

```
Similarity Report
=================

Similar Pairs (expected high similarity):
  "The cat sat on the mat" <-> "A feline rested on the rug"
  Cosine Similarity: 0.83  ✓ High

  "Python is a programming language" <-> "Python is used for coding software"
  Cosine Similarity: 0.91  ✓ High

Dissimilar Pairs (expected low similarity):
  "The cat sat on the mat" <-> "The stock market crashed today"
  Cosine Similarity: 0.12  ✓ Low
```

---

### Step 4: Vector Arithmetic (45 min)

In `arithmetic.py`, implement the famous word/sentence analogy experiments.

The concept: if embeddings truly capture meaning, then:
- `embed("king") − embed("man") + embed("woman")` should be close to `embed("queen")`
- `embed("Paris") − embed("France") + embed("Germany")` should be close to `embed("Berlin")`

```python
from embedding_playground.embedder import EmbeddingModel
from embedding_playground.similarity import cosine_similarity

import numpy as np


def analogy(
    embedder: EmbeddingModel,
    a: str,
    b: str,
    c: str,
    candidates: list[str],
) -> list[tuple[str, float]]:
    """
    Solve: "a is to b as c is to ???"
    Returns candidates ranked by similarity to the computed target vector.

    Example: analogy("king", "man", "woman", ["queen", "princess", "girl"])
    """
    vecs = embedder.embed([a, b, c] + candidates)
    va, vb, vc = vecs[0], vecs[1], vecs[2]

    # The magic: subtract b, add c — shifts the direction of meaning
    target = va - vb + vc

    results = []
    for i, candidate in enumerate(candidates):
        sim = cosine_similarity(target, vecs[3 + i])
        results.append((candidate, sim))

    return sorted(results, key=lambda x: x[1], reverse=True)
```

> **Important note about sentence vs word models:** `all-MiniLM-L6-v2` is trained on *sentences*, not individual words. Word arithmetic (king − man + woman) was designed for word-level models like Word2Vec and GloVe, where each word has a single fixed vector. Sentence models encode contextual meaning — the vector for "king" in "The king ruled the land" is different from "king" alone.
>
> This means your arithmetic results may be less clean than the famous Word2Vec demos. **This is the expected result and is itself a key learning point.** In your analysis, discuss *why* sentence-level models produce different behavior than word-level models.

Test cases to implement:

1. `king − man + woman = ?` — candidates: queen, princess, girl, duchess
2. `Paris − France + Germany = ?` — candidates: Berlin, Munich, Hamburg, Frankfurt
3. `walked − walk + swim = ?` — candidates: swam, swimming, swims, swimmer
4. `good − bad + terrible = ?` — candidates: wonderful, great, excellent, amazing

---

### Step 5: 2D Visualization (45 min)

> **Tip:** This step is best done in `explore.ipynb` (the Jupyter notebook) rather than as a script. Matplotlib plots render inline and you can iterate on the visualization without re-running the whole pipeline. Once you are happy with the output, refactor the code into `visualizer.py`.

In `visualizer.py`:

```python
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def plot_embeddings_2d(
    embeddings: np.ndarray,
    labels: list[str],
    groups: list[str] | None = None,
    method: str = "tsne",
    title: str = "Embedding Visualization",
    output_path: str = "embeddings_2d.png",
) -> None:
    """
    Project embeddings to 2D and create a labeled scatter plot.

    Args:
        embeddings: Array of shape (n, dim) — one row per text.
        labels: Text label for each point (truncated if too long).
        groups: Optional group name for each point (controls color).
        method: "tsne" or "pca". t-SNE preserves local structure;
                PCA is deterministic and faster.
        output_path: Where to save the PNG.
    """
    if method == "tsne":
        reducer = TSNE(
            n_components=2,
            random_state=42,
            perplexity=min(5, len(embeddings) - 1),
        )
    else:
        reducer = PCA(n_components=2)

    coords = reducer.fit_transform(embeddings)

    plt.figure(figsize=(14, 10))

    if groups:
        unique_groups = list(set(groups))
        colors = plt.cm.Set2(np.linspace(0, 1, len(unique_groups)))  # type: ignore[attr-defined]
        for group, color in zip(unique_groups, colors, strict=False):
            mask = np.array([g == group for g in groups])
            plt.scatter(coords[mask, 0], coords[mask, 1], c=[color], label=group, s=100)
    else:
        plt.scatter(coords[:, 0], coords[:, 1], s=100)

    for i, label in enumerate(labels):
        short = label[:40] + "..." if len(label) > 40 else label
        plt.annotate(short, (coords[i, 0], coords[i, 1]), fontsize=8, ha="center", va="bottom")

    plt.title(title)
    if groups:
        plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved visualization to {output_path}")


def plot_similarity_heatmap(
    sim_matrix: np.ndarray,
    labels: list[str],
    output_path: str = "similarity_heatmap.png",
) -> None:
    """Create a color-coded heatmap of pairwise cosine similarities."""
    plt.figure(figsize=(12, 10))
    short_labels = [label[:30] + "..." if len(label) > 30 else label for label in labels]
    sns.heatmap(
        sim_matrix,
        xticklabels=short_labels,
        yticklabels=short_labels,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        vmin=-1,
        vmax=1,
    )
    plt.title("Pairwise Cosine Similarity")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
```

> **`zip(strict=False)` note:** Python 3.12's `zip()` gained a `strict` parameter. Using `strict=False` makes intent explicit and satisfies Ruff's `B905` rule. This is a minor but good habit.

Create these three visualizations:

1. **Semantic clusters (t-SNE):** Embed all sentences from `semantic_groups`. Color by group. You should see clusters — animals near animals, tech near tech. Save as `semantic_clusters_tsne.png`.
2. **Semantic clusters (PCA):** Same data, PCA instead of t-SNE. Note the differences. Save as `semantic_clusters_pca.png`.
3. **Similarity heatmap:** Pairwise cosine similarity across all sentences. Save as `similarity_heatmap.png`.

---

### Step 6: Build the CLI (20 min)

Tie everything together in `cli.py`:

```bash
# Run similarity analysis
uv run python -m embedding_playground similarity

# Run vector arithmetic experiments
uv run python -m embedding_playground arithmetic

# Generate all visualizations
uv run python -m embedding_playground visualize

# Compare two specific sentences
uv run python -m embedding_playground compare "I love dogs" "I adore puppies"

# Full report
uv run python -m embedding_playground report
```

> **Change from original:** Every `python -m ...` command is now prefixed with `uv run`. This ensures the command always runs inside the project's virtual environment — regardless of what Python is active in your shell. You will never hit "module not found" because you forgot to activate the venv.

---

### Step 7: Experiments and Analysis (30 min)

Run these experiments and document your findings (print to terminal or save to `analysis.txt`):

1. **Negation problem**: Compare similarity of `"I love this movie"` vs `"I hate this movie"`. Are they similar or different? Why? (This reveals a known limitation of embeddings — they often encode topic similarity, not sentiment polarity.)
2. **Context sensitivity**: Compare `"bank"` in `"river bank"` vs `"bank account"`. Does the model distinguish them? (Hint: sentence-level models handle this better than word-level models.)
3. **Length sensitivity**: Does embedding `"Hello"` give different results than `"Hello, this is a very long sentence that keeps going and going"`?
4. **Embedding drift**: Embed the same sentence with `all-MiniLM-L6-v2` and `BAAI/bge-large-en-v1.5` if you have time. How different are the similarity scores? Which seems more accurate?

---

## Expected Output

Your final script should produce:

1. A terminal report showing similarity scores for all test pairs
2. Vector arithmetic results with accuracy assessment and a note on why sentence models behave differently from word models
3. Three saved PNG visualizations:
   - `semantic_clusters_tsne.png` — Clustered semantic groups (t-SNE)
   - `semantic_clusters_pca.png` — Same data with PCA
   - `similarity_heatmap.png` — Pairwise similarity matrix
4. A written analysis (printed or saved as `analysis.txt`) with findings from the experiments in Step 7

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **Embedding Implementation** | 25% | Correct embedding generation, Protocol interface, type hints throughout |
| **Similarity Analysis** | 20% | Accurate cosine similarity, clear reporting with expected vs actual |
| **Vector Arithmetic** | 20% | Correct implementation, thoughtful candidate selection, honest analysis of model limitations |
| **Visualizations** | 20% | Clear, labeled, informative plots saved as PNG; prefer notebook-first workflow |
| **Analysis & Insights** | 15% | Written observations about experiments, honest discussion of limitations |

---

## Bonus Challenges

1. **Embedding Cache**: Implement a local cache (SQLite or `diskcache`) so embeddings are not recomputed for the same text + model combination. Measure the speedup with `time.perf_counter()`.
2. **Interactive 3D Plot**: Use `plotly` to create an interactive 3D scatter plot that you can rotate and zoom. Export it as an HTML file (`uv add plotly`).
3. **Custom Benchmark**: Create a benchmark of 50+ sentence pairs with human-judged similarity scores (1–5). Evaluate how well different embedding models correlate with human judgment (use Spearman correlation).
4. **Embedding Search**: Build a mini search engine — embed a set of 50 documents, embed a query, find the top-k most similar. This is the exact foundation of RAG retrieval that you will build in Month 2.
5. **Cross-Lingual Embeddings**: Use `paraphrase-multilingual-MiniLM-L12-v2` (a multilingual model) and test if `"I love pizza"` in English is similar to `"J'adore la pizza"` in French. Genuinely surprising results.

---

## Key Concepts You Will Learn

- **Embeddings**: Dense vector representations of text that capture semantic meaning
- **Cosine similarity**: The standard metric for comparing embeddings (range: −1 to 1)
- **Dimensionality reduction**: t-SNE and PCA for visualizing high-dimensional data
- **Vector arithmetic**: How meaning can be manipulated mathematically (and its limits)
- **Embedding model trade-offs**: Local (free, private) vs API (better quality, costs money)
- **Limitations**: Negation blindness, length sensitivity, word vs sentence model differences

---

## What Changed and Why

| Original | Updated | Reason |
|---|---|---|
| `pip install sentence-transformers ...` | `uv add sentence-transformers ...` | UV is faster, creates lockfile automatically |
| No project file shown | `uv init` + `pyproject.toml` | Reproducible project setup; any collaborator can run `uv sync` |
| `python -m embedding_playground ...` | `uv run python -m embedding_playground ...` | No manual venv activation needed; always uses correct environment |
| `List[str]` from `typing` | `list[str]` built-in | Python 3.12 native syntax; old form deprecated since 3.9 |
| `list[str] \| None` missing | `list[str] \| None` (union syntax) | Python 3.10+ syntax for optional types; no `Optional[...]` import needed |
| No dev tooling | `ruff` + `mypy` in `pyproject.toml` | Linting and type checking configured from day one |
| No notebook mention | Notebook-first workflow for visualization | Iteration on plots is much faster in a Jupyter cell than re-running a script |
| `zip(a, b)` | `zip(a, b, strict=False)` | Explicit intent, satisfies Ruff B905 rule in Python 3.12 |
| Static BAAI model name | MTEB leaderboard reference added | Embedding model rankings change; engineers should know where to look |
