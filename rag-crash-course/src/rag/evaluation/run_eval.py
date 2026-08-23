# src/rag/evaluation/run_eval.py

import numpy as np
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from ragas import EvaluationDataset, evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import ContextPrecision, ContextRecall, Faithfulness, ResponseRelevancy

from rag.config import settings
from rag.generation.chain import answer_question

# Keyed on Ragas's OWN internal metric name (metric.name), not the class
# name — e.g. the ResponseRelevancy class still reports itself internally
# as "answer_relevancy" (the older name), confirmed by inspecting the
# installed package directly rather than guessing.
METRIC_INTERPRETATIONS = {
    "context_precision": "retrieval is pulling noise alongside the right chunks (tune k down, or add filtering)",
    "context_recall": "retrieval is missing the answer entirely — no prompt fix helps this; look at chunk size, k, or embedding model",
    "faithfulness": "the model is hallucinating claims the retrieved context doesn't support — a generation/prompt problem, not retrieval",
    "answer_relevancy": "the answer doesn't actually address what was asked, even if it's grounded — check for off-topic or over-hedged answers",
}


def build_eval_dataset(
    vector_store: PineconeVectorStore,
    qa_pairs: list[dict],
    #  NEW PARAMS DECLRATION TO SUPPORT RE RANKING
    use_reranking: bool = False,
    pc: Pinecone | None = None,
    rerank_fetch_k: int = 20,
) -> EvaluationDataset:
    """
    Runs every hand-written QA pair through the REAL pipeline
    (Lesson 7's answer_question — the same function the live
    /query endpoint calls) and reshapes each result into the
    four fields Ragas's EvaluationDataset requires.

    This is deliberately NOT a reimplemented/mocked retrieval or
    generation path — if it were, a passing eval score wouldn't
    prove anything about the system you actually ship.
    """
    rows = []

    for pair in qa_pairs:
        # Same call your API makes. Default k=5, no team/doc_type
        # filter — matches how a real, unscoped user query behaves.
        result = answer_question(
            vector_store,
            pair["question"],
            use_reranking=use_reranking,
            pc=pc,
            rerank_fetch_k=rerank_fetch_k,
        )

        rows.append(
            {
                "user_input": pair["question"],
                "response": result["answer"],
                # raw_chunks is list[tuple[Document, float]] — Ragas
                # only wants the bare page_content text, not the
                # Document object, metadata, or cosine score.
                "retrieved_contexts": [doc.page_content for doc, _score in result["raw_chunks"]],
                # Ragas's field is called "reference" — your QA_PAIRS
                # dict can keep the name "ground_truth", you just map
                # it here when assembling the row.
                "reference": pair["ground_truth"],
            }
        )

    return EvaluationDataset.from_list(rows)


def evaluate_pipeline(dataset) -> None:

    # Built explicitly from `settings`, not left to Ragas's default
    # (which falls back to a bare openai.OpenAI() client reading
    # os.environ directly — a key this project never populates there).
    evaluator_llm = LangchainLLMWrapper(
        ChatOpenAI(
            model=settings.CHAT_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0,  # deterministic judge, not a creative one
        )
    )

    evaluator_embeddings = LangchainEmbeddingsWrapper(
        OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)
    )

    results = evaluate(
        dataset=dataset,
        metrics=[ContextPrecision(), ContextRecall(), Faithfulness(), ResponseRelevancy()],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )
    print("\n--- Ragas Evaluation Summary ---")
    for metric_name, interpretation in METRIC_INTERPRETATIONS.items():
        # results[metric_name] returns the list of per-question scores;
        # nanmean skips any row Ragas couldn't score instead of letting
        # one bad row silently corrupt the whole average.
        score = np.nanmean(results[metric_name])
        print(f"{metric_name:>18}: {score:.3f}   (low = {interpretation})")


if __name__ == "__main__":
    import asyncio

    from rag.evaluation.eval_dataset import QA_PAIRS
    from rag.evaluation.run_eval_modern import evaluate_pipeline_modern
    from rag.retrieval.retriever import get_vector_store

    vector_store = get_vector_store()

    print(f"Running {len(QA_PAIRS)} questions through the real pipeline...")
    dataset = build_eval_dataset(vector_store, QA_PAIRS)

    evaluate_pipeline(dataset)

    asyncio.run(evaluate_pipeline_modern(dataset))
