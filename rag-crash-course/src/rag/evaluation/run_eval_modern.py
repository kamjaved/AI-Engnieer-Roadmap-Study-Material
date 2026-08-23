# src/rag/evaluation/run_eval_modern.py

# Kept in its own file specifically so ragas.metrics.collections'
# ContextPrecision/ContextRecall/Faithfulness never share a namespace
# with run_eval.py's legacy ragas.metrics versions of the same names.
# Importing both into one file silently shadows one set with the
# other — no import error, just a confusing runtime failure later,
# since the old evaluate() can't work with the new metric classes.

import numpy as np
import openai
from ragas.embeddings import OpenAIEmbeddings as RagasOpenAIEmbeddings
from ragas.llms import llm_factory
from ragas.metrics.collections import (
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
    Faithfulness,
)

from rag.config import settings

# Small, deliberate duplication of run_eval.py's METRIC_INTERPRETATIONS
# rather than importing it across files. The dict is 4 lines and static —
# not worth risking a cross-module import tangle with a file that's
# also run directly via `python -m`, where the same module can end up
# loaded twice under two different names (as __main__ and by its real
# dotted path). A shared third file would be the fix if this ever grows
# past a couple of static lines.
METRIC_INTERPRETATIONS = {
    "context_precision": "retrieval is pulling noise alongside the right chunks (tune k down, or add filtering)",
    "context_recall": "retrieval is missing the answer entirely — no prompt fix helps this; look at chunk size, k, or embedding model",
    "faithfulness": "the model is hallucinating claims the retrieved context doesn't support — a generation/prompt problem, not retrieval",
    "answer_relevancy": "the answer doesn't actually address what was asked, even if it's grounded — check for off-topic or over-hedged answers",
}


async def evaluate_pipeline_modern(dataset) -> None:
    """
    Modern (non-deprecated) Ragas scoring path, using
    ragas.metrics.collections instead of ragas.metrics + evaluate().

    Real architectural difference from run_eval.py's evaluate_pipeline(),
    not just a renamed import: evaluate() only recognizes the OLD Metric
    base class internally, and these collections classes deliberately
    don't inherit from it — so there's no batch runner for them. This
    function replaces evaluate() with its own per-row async loop.
    """
    # ragas's own client here, not LangChain's ChatOpenAI — the modern
    # collections API talks to the OpenAI SDK directly via llm_factory,
    # dropping the LangchainLLMWrapper indirection entirely.
    client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    llm = llm_factory(settings.CHAT_MODEL, client=client)
    embeddings = RagasOpenAIEmbeddings(client=client, model=settings.EMBEDDING_MODEL)

    context_precision = ContextPrecision(llm=llm)
    context_recall = ContextRecall(llm=llm)
    faithfulness = Faithfulness(llm=llm)
    # Note the name: this is the legacy ResponseRelevancy() metric, but
    # ragas.metrics.collections exposes it as AnswerRelevancy — verified
    # directly against the installed package, since ragas's own
    # deprecation-warning text names a class that doesn't actually exist
    # at that import path (a real bug in their warning message).
    answer_relevancy = AnswerRelevancy(llm=llm, embeddings=embeddings)

    # Same EvaluationDataset object build_eval_dataset() already built —
    # .to_list() unpacks it back into plain row dicts, since there's no
    # batch scorer left to hand the whole dataset object to.
    rows = dataset.to_list()

    scores = {
        "context_precision": [],
        "context_recall": [],
        "faithfulness": [],
        "answer_relevancy": [],
    }

    for row in rows:
        # Each metric only takes the fields it actually needs — notice
        # answer_relevancy never even sees retrieved_contexts, since it
        # only ever compares the answer against the question.
        cp = await context_precision.ascore(
            user_input=row["user_input"],
            reference=row["reference"],
            retrieved_contexts=row["retrieved_contexts"],
        )
        cr = await context_recall.ascore(
            user_input=row["user_input"],
            retrieved_contexts=row["retrieved_contexts"],
            reference=row["reference"],
        )
        f = await faithfulness.ascore(
            user_input=row["user_input"],
            response=row["response"],
            retrieved_contexts=row["retrieved_contexts"],
        )
        ar = await answer_relevancy.ascore(
            user_input=row["user_input"],
            response=row["response"],
        )

        scores["context_precision"].append(cp.value)
        scores["context_recall"].append(cr.value)
        scores["faithfulness"].append(f.value)
        scores["answer_relevancy"].append(ar.value)

    print("\n--- Ragas Evaluation Summary (modern ragas.metrics.collections API) ---")
    for metric_name, interpretation in METRIC_INTERPRETATIONS.items():
        score = np.nanmean(scores[metric_name])
        print(f"{metric_name:>18}: {score:.3f}   (low = {interpretation})")
