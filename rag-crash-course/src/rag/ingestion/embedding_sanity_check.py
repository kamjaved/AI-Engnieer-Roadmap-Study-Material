import numpy as np
from langchain_openai import OpenAIEmbeddings

from rag.config import settings

# We reuse settings.EMBEDDING_MODEL (defined back in Lesson 1's config.py)
# instead of hardcoding a model name string here. Same reasoning as always:
# one source of truth. If you ever change embedding models, you change it
# in ONE place (.env / config.py), not hunt through every script that
# creates an OpenAIEmbeddings instance.
embeddings = OpenAIEmbeddings(
    model=settings.EMBEDDING_MODEL,
    api_key=settings.OPENAI_API_KEY,  # explicit, not relying on OpenAIEmbeddings' own env lookup
)


# cosine_similarity(a, b) = (a · b) / (||a|| * ||b||)


def cosine_sim(a: list[float], b: list[float]) -> float:
    """
    Cosine similarity between two vectors — measures the angle between them,
    not their length. Returns a value from -1.0 (opposite) to 1.0 (identical
    direction). For text embeddings, scores are almost always positive,
    usually somewhere in the 0.7-0.99 range for genuinely related text.
    """
    vec_a = np.array(a)
    vec_b = np.array(b)

    dot_product = np.dot(vec_a, vec_b)  # a · b — direction + magnitude combined
    norm_a = np.linalg.norm(vec_a)  # ||a|| — length of vector a
    norm_b = np.linalg.norm(vec_b)  # ||b|| — length of vector b

    return dot_product / (norm_a * norm_b)  # dividing out magnitude leaves pure direction


sentence_1 = "Employees at the staff level and below are required to serve a 30-day notice period, while managers and higher-level employees are required to serve a 60-day notice period upon resignation."
sentence_2 = "All new employees are subject to a 90-day probationary period, which may be extended once by up to 30 days at the manager's discretion if performance requires additional evaluation rather than being deemed unsatisfactory."
sentence_3 = "Staff-level employees and below are expected to provide 1 month notice before leaving the organization, while managers and above are expected to provide 2 month notice."

# One batched API call instead of three separate ones — fewer round trips,
# and it's the natural fit since we're comparing documents, not a query
# against documents.
vec_1, vec_2, vec_3 = embeddings.embed_documents([sentence_1, sentence_2, sentence_3])

# The pair that should score HIGH — same fact, different wording (1 & 3)
sim_similar_pair = cosine_sim(vec_1, vec_3)

# The two pairs that should score LOWER — same domain, different topic
sim_1_vs_unrelated = cosine_sim(vec_1, vec_2)
sim_3_vs_unrelated = cosine_sim(vec_3, vec_2)

print(f"Similar pair   (sentence 1 vs sentence 3): {sim_similar_pair:.4f}")
print(f"Unrelated pair (sentence 1 vs sentence 2): {sim_1_vs_unrelated:.4f}")
print(f"Unrelated pair (sentence 3 vs sentence 2): {sim_3_vs_unrelated:.4f}")


# ----OUTPUT-----
# $ uv run python -m rag.ingestion.embedding_sanity_check
# Similar pair   (sentence 1 vs sentence 3): 0.7934
# Unrelated pair (sentence 1 vs sentence 2): 0.5645
# Unrelated pair (sentence 3 vs sentence 2): 0.4183


# src/rag/ingestion/embedding_sanity_check.py  (continued)

assert sim_similar_pair > sim_1_vs_unrelated and sim_similar_pair > sim_3_vs_unrelated, (
    "Sanity check FAILED: the similar-sentence pair did not score higher than "
    "the unrelated pairs. Something's off with the embedding model or the "
    "sentences themselves."
)

print("Sanity check PASSED: similar sentences scored higher than unrelated ones.")
