# run_hyde_demo.py (project root)

from rag.retrieval.retriever import get_vector_store, retrieve

# Deliberately short and vague — this is the exact failure case HyDE
# targets. A real Turab travel policy doc will use formal phrasing
# ("travel authorization," "expedited approval") that this casual
# question doesn't share a single word with. If we picked a question
# that already used the doc's own vocabulary, we wouldn't be testing
# anything — dense search alone would already do fine on it.
QUESTION = "what do I do if I need to travel for a client meeting on short notice?"


def main() -> None:
    vector_store = get_vector_store()

    # Run 1: raw query, straight into embedding + search — Lesson 6 behavior,
    # unchanged. This is our baseline to compare against.
    baseline_results = retrieve(vector_store, QUESTION, k=5, query_transform="none")

    # Run 2: same question, same vector_store, same k — the ONLY variable
    # that changes is query_transform. That's what makes this a controlled
    # comparison instead of two unrelated results (same discipline as
    # Lesson 6.3's demo, which held the query fixed and varied only the filter).
    hyde_results = retrieve(vector_store, QUESTION, k=5, query_transform="hyde")

    # similarity_search_with_score returns list[tuple[Document, float]] —
    # unpack the top hit from each run to compare side by side.
    baseline_doc, baseline_score = baseline_results[0]
    hyde_doc, hyde_score = hyde_results[0]

    print(f"Question: {QUESTION}\n")
    print("--- query_transform='none' (raw question embedded) ---")
    print(f"Top chunk: {baseline_doc.metadata['source']} (score: {baseline_score:.4f})\n")

    print("--- query_transform='hyde' (hypothetical answer embedded) ---")
    print(f"Top chunk: {hyde_doc.metadata['source']} (score: {hyde_score:.4f})")


if __name__ == "__main__":
    main()
