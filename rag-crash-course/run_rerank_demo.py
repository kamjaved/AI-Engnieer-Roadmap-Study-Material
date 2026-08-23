"""
Lesson 10.5 — demo: reranking on vs off, same query, side by side.
"""

from pinecone import Pinecone

from rag.config import settings
from rag.generation.chain import answer_question
from rag.retrieval.retriever import get_vector_store


def print_result(label: str, result: dict) -> None:
    print(f"--- {label} ---")
    # raw_chunks is still list[tuple[Document, float]] in EITHER mode —
    # that's the whole point of rerank() matching retrieve()'s shape —
    # so this same printing loop works for both calls below unchanged.
    for i, (doc, score) in enumerate(result["raw_chunks"], start=1):
        print(f"  [{i}] {doc.metadata['source']}  (score: {score:.4f})")
    print(f"  Cited sources: {result['sources']}")
    print()


if __name__ == "__main__":
    vector_store = get_vector_store()
    # Same client-construction pattern as run_ingest.py's pc — built once
    # here, passed in explicitly to answer_question(), not hidden inside it.
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    # Deliberately a broader/vaguer question than the earlier demos —
    # something with MORE than 5 plausible candidate chunks in the
    # corpus. A query with only 1-2 relevant chunks total wouldn't give
    # reranking any real room to reorder anything.
    query = "what benefits and leave am I entitled to as a new employee?"

    baseline = answer_question(vector_store, query, k=5)
    reranked = answer_question(
        vector_store, query, k=5, use_reranking=True, pc=pc, rerank_fetch_k=20
    )

    print_result("WITHOUT reranking (k=5 direct)", baseline)
    print_result("WITH reranking (retrieve k=20, rerank top_n=5)", reranked)
