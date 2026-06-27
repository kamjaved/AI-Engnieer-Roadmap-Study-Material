import os

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


# reads .env file into os.environ
load_dotenv()

# automatically reads OPENAI_API_KEY from environment
client = OpenAI()


SIMILARITY_SAMPLES: list[tuple[str, str]] = [
    # label, text
    ("dog_1", "The dog ran across the park"),
    ("dog_2", "A puppy sprinted through the field"),
    ("weather", "It is raining heavily outside today"),
    ("code", "def add(a, b): return a + b"),
]


def get_embeddings(texts: list[str], model: str = "text-embedding-3-small") -> np.ndarray:
    response = client.embeddings.create(input=texts, model=model)
    vectors = [item.embedding for item in response.data]
    return np.array(vectors, dtype=np.float32)


texts = [text for _, text in SIMILARITY_SAMPLES]
result = get_embeddings(texts)

# print(result)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Cosine similarity between two pre-normalized vectors.
    Because OpenAI embeddings are unit vectors and comes normalized, this is just the dot product.
    Score range: 0.0 (unrelated) → 1.0 (identical meaning).
    """
    return float(np.dot(a, b))


def explore_similarity(samples: list[tuple[str, str]]) -> None:

    labels = [label for label, _ in samples]
    texts = [text for _, text in samples]
    print(f"LABELS: {labels}")

    # Step 1: Embed all texts at once
    embeddings = get_embeddings(texts)
    print(f"\nEmbedding shape: {embeddings.shape}")
    print(
        f"  → {embeddings.shape[0]} sentences, each a {embeddings.shape[1]}-dimensional vector\n"
    )

    # Step 2: Build a simple index so we can look up by label
    idx = {label: i for i, label in enumerate(labels)}
    print(f"IDX: {idx}")

    # Step 3: Compare specific pairs
    pairs_to_compare = [
        ("dog_1", "dog_2"),  # Should be HIGH — same concept, different words
        ("dog_1", "weather"),  # Should be LOW — unrelated topics
        ("dog_1", "code"),  # Should be VERY LOW — completely different domains
        ("dog_2", "weather"),  # Middle ground
    ]

    print("Pairwise cosine similarity:")
    print(f"  {'Pair':<30}  Score")
    print(f"  {'-' * 30}  -----")

    for label_a, label_b in pairs_to_compare:
        similarity = cosine_similarity(embeddings[idx[label_a]], embeddings[idx[label_b]])
        print(f" {label_a} <--> {label_b:<18}  {similarity:.4f}")


result2 = explore_similarity(SIMILARITY_SAMPLES)

print(result2)
