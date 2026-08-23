from __future__ import annotations

from langchain_core.documents import Document
from pinecone import Pinecone


def rerank(
    pc: Pinecone,
    query: str,
    scored_docs: list[tuple[Document, float]],
    top_n: int = 5,
) -> list[tuple[Document, float]]:
    """
    Re-scores an already-retrieved candidate set using a cross-encoder,
    and returns the top_n re-ordered.

    Input/output shape is DELIBERATELY the same as retrieve()'s own
    return type — list[tuple[Document, float]] — so this drops straight
    into the pipeline between retrieve() and format_docs() with zero
    reshaping. Same trick you already used for hybrid_retrieve() in
    Lesson 6.6: match the existing shape, don't invent a new one.
    """

    # Pinecone's rerank API wants raw text, not LangChain Document
    # objects — it has no idea what a Document is. Strip down to just
    # page_content, same "unwrap before calling the SDK, re-wrap after"
    # pattern you used back in Lesson 5's index_chunks().
    docs_only = [doc.page_content for doc, _score in scored_docs]

    result = pc.inference.rerank(
        model="bge-reranker-v2-m3",
        query=query,
        documents=docs_only,
        top_n=top_n,
        # return_documents=False: don't ask Pinecone to send the chunk
        # text back to us — we already have it locally in scored_docs.
        # Sending it back would just be redundant bytes over the wire.
        # All we actually need from the response is WHICH ones ranked
        # highest, and in what order — that's what r.index gives us.
        return_documents=False,
    )

    # result.data is a list of rerank results, already sorted best-first
    # by the cross-encoder's own relevance score. r.index is the
    # POSITION of that chunk in the ORIGINAL docs_only list we sent —
    # so scored_docs[r.index] maps each result straight back to its
    # original (Document, cosine_score) tuple, in the new reranked order.
    return [scored_docs[r.index] for r in result.data]
