# run_retrieval_demo.py  (project root)

from rag.retrieval.retriever import get_vector_store, retrieve

QUERY = "what is the notice period for resigning?"


def print_results(label: str, results: list[tuple]) -> None:
    print(f"\n--- {label} ---")
    if not results:
        # An empty list is itself a meaningful result here — it means
        # the filter eliminated every candidate before scoring even
        # happened, not that scoring ran and found nothing good.
        print("  (no results)")
        return
    for doc, score in results:
        # doc.metadata["source"] is the same field loader.py (Lesson
        # 2.5) attached at ingestion time — it's how you trace a
        # retrieved chunk back to which file it actually came from.
        print(f"  score={score:.4f}  source={doc.metadata.get('source')}")


def main() -> None:
    # One connection, reused for all three calls — no reason to
    # reconnect to Pinecone three times for one script run.
    vector_store = get_vector_store()

    # 1. No filter — the whole index is fair game.
    print_results("No filter", retrieve(vector_store, QUERY, k=5))

    # 2. Filtered to HR — this is where the real answer lives.
    print_results('team="hr"', retrieve(vector_store, QUERY, k=5, team="hr"))

    # 3. Filtered to sales — the answer does NOT live here. This is the
    # one that actually proves the filter narrows the search space,
    # rather than just re-sorting the same candidates.
    print_results('team="sales"', retrieve(vector_store, QUERY, k=5, team="sales"))


if __name__ == "__main__":
    main()
