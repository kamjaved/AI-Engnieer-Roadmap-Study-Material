"""
Lesson 10.6 (optional extension) — does reranking actually move
context_precision on this corpus, or not? Runs Lesson 9's eval suite
twice on the SAME 11-question set: once through the untouched Lesson 9
baseline path, once with reranking wired in.
"""

from pinecone import Pinecone

from rag.config import settings
from rag.evaluation.eval_dataset import QA_PAIRS
from rag.evaluation.run_eval import build_eval_dataset, evaluate_pipeline
from rag.retrieval.retriever import get_vector_store

if __name__ == "__main__":
    vector_store = get_vector_store()
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    print(f"Running {len(QA_PAIRS)} questions WITHOUT reranking (Lesson 9 baseline)...")
    baseline_dataset = build_eval_dataset(vector_store, QA_PAIRS)

    print(f"Running {len(QA_PAIRS)} questions WITH reranking (retrieve k=20, rerank top_n=5)...")
    reranked_dataset = build_eval_dataset(
        vector_store, QA_PAIRS, use_reranking=True, pc=pc, rerank_fetch_k=20
    )

    print("\n=== WITHOUT reranking ===")
    evaluate_pipeline(baseline_dataset)

    print("\n=== WITH reranking ===")
    evaluate_pipeline(reranked_dataset)
