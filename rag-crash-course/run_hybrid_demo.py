# run_hybrid_demo.py (project root — same entry-point convention as
# run_retrieval_demo.py and run_hyde_demo.py)

from rag.ingestion.chunker import chunk_documents
from rag.ingestion.loader import load_documents
from rag.retrieval.retriever import get_vector_store, hybrid_retrieve, retrieve
from rag.retrieval.sparse_retriever import build_bm25_index, sparse_retrieve

# Query 1: an exact phrase pulled straight from corporate_gifts_price_list.pdf
# — the same term Lesson 3.4/3.5 already confirmed is real content in that
# PDF. Expected to favor BM25's exact lexical matching over dense.
EXACT_TOKEN_QUERY = "steel water bottle"

# Query 2: reused from Lesson 6.5's HyDE demo on purpose — same vague,
# paraphrased HR question, so this result is directly comparable to what
# you already saw dense (and HyDE) do with it. Expected to favor dense's
# meaning-based matching over BM25's literal word overlap.
PARAPHRASE_QUERY = "what do I do if I need to travel for a client meeting on short notice?"


def print_ranked_list(label: str, docs: list) -> None:
    print(f"  {label}:")
    for rank, doc in enumerate(docs, start=1):
        print(f"    #{rank}  {doc.metadata['source']}")


def run_query(vector_store, bm25_index, chunks, query: str) -> None:
    print(f"\nQuery: {query!r}")

    dense_results = retrieve(vector_store, query, k=5)
    dense_docs = [doc for doc, _score in dense_results]

    sparse_docs = sparse_retrieve(bm25_index, chunks, query, k=5)

    hybrid_docs = hybrid_retrieve(vector_store, bm25_index, chunks, query, k=5)

    print_ranked_list("Dense-only", dense_docs)
    print_ranked_list("Sparse-only (BM25)", sparse_docs)
    print_ranked_list("Hybrid (RRF)", hybrid_docs)


def main() -> None:
    # Same load -> chunk pipeline every ingestion/demo script has used
    # since Lesson 3 — the same 57 chunks already sitting in Pinecone
    # (Lesson 5), now ALSO fed into a fresh in-memory BM25 index.
    chunks = chunk_documents(load_documents())
    # build_bm25_index returns (index, chunks) as a bundle — per 6.6.2's
    # design decision, reassigning chunks here even though its contents
    # don't change is what keeps the index and its chunk list guaranteed
    # to stay in the same order downstream.
    bm25_index, chunks = build_bm25_index(chunks)

    vector_store = get_vector_store()

    run_query(vector_store, bm25_index, chunks, EXACT_TOKEN_QUERY)
    run_query(vector_store, bm25_index, chunks, PARAPHRASE_QUERY)


if __name__ == "__main__":
    main()
