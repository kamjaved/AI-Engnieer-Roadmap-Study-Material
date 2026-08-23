from __future__ import annotations

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from rag.config import settings
from rag.retrieval.fusion import reciprocal_rank_fusion
from rag.retrieval.sparse_retriever import sparse_retrieve

_hyde_llm = ChatOpenAI(model=settings.CHAT_MODEL, temperature=0.3)


def get_vector_store() -> PineconeVectorStore:
    # Same embedding model settings.py already points at — this MUST
    # match whatever model Lesson 5 used to write the vectors in the
    # first place. This is Lesson 4's silent-failure trap again: if
    # this model doesn't match index-time, nothing crashes, the
    # numbers just come back meaningless.
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)

    # from_existing_index, NOT from_documents. from_documents (Lesson 5)
    # embeds + upserts — a write. from_existing_index just opens a
    # connection to an index that's already populated — a read-side
    # handle. It does not touch what's already stored.
    return PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
    )


def retrieve(
    vector_store: PineconeVectorStore,
    query: str,
    k: int = 5,
    team: str | None = None,
    doc_type: str | None = None,
    query_transform: str = "none",  # new — "none" | "hyde"
) -> list[tuple[Document, float]]:

    # If query_transform="hyde", swap what gets embedded/searched — the
    # raw question is discarded, hyde_query()'s output takes its place.
    # If "none" (the default), search_text is just the original query,
    search_text = hyde_query(query) if query_transform == "hyde" else query
    # Build the filter dict ONLY from whatever was actually passed in.
    # If both team and doc_type are None, filter_dict stays {} — an
    # unfiltered search across the whole index.
    filter_dict: dict = {}

    # Pinecone's filter syntax is Mongo-style operators, not a bare
    # value. "$eq" = exact match. There are others ($in, $gte, etc)
    # but $eq is all we need for team/doc_type equality checks.
    if team:
        filter_dict["team"] = {"$eq": team}
    if doc_type:
        filter_dict["doc_type"] = {"$eq": doc_type}

    return vector_store.similarity_search_with_score(
        search_text,  # <- was `query` before; now it's search_text
        k=k,
        # filter_dict or None: an empty {} dict is falsy in Python, so
        # if nothing was provided this evaluates to None — Pinecone
        # treats filter=None as "no filter," not "match nothing."
        # Passing filter={} explicitly would behave differently in some
        # vector DBs, so this line matters, not just style.
        filter=filter_dict or None,
    )


def hyde_query(question: str) -> str:
    """
    Turns a user's question into a hypothetical answer paragraph,
    written in the style of an internal Turab Industries policy doc.

    The output is NOT meant to be factually correct — only stylistically
    close to what a real chunk in the index would look like, so its
    embedding lands nearer the real answer than the raw question would.
    """
    prompt = (
        "You are writing an internal policy document for Turab Industries, "
        "a company with HR, procurement, sales, and leadership teams.\n\n"
        "Write a short paragraph (3-5 sentences) that would plausibly answer "
        "the following question, in the tone and style of an internal company "
        "policy or guide document. It is OK — expected, even — for the specific "
        "details to be invented. Only the style and vocabulary need to be realistic.\n\n"
        f"Question: {question}\n\n"
        "Hypothetical policy paragraph:"
    )

    # .invoke() on a ChatOpenAI instance sends one request, returns an AIMessage
    response = _hyde_llm.invoke(prompt)
    return response.content  # the actual generated text (a plain string)


def hybrid_retrieve(
    vector_store,
    bm25_index,
    chunks: list[Document],
    query: str,
    k: int = 5,
) -> list[Document]:
    """
    Runs dense (Pinecone) and sparse (BM25) retrieval independently,
    fuses their ranked lists with RRF, returns the top-k fused result.
    """
    # Fetch WIDER than the final k from each individual retriever before
    # fusing — the exact same "wide retrieval, then narrow" principle
    # from Lesson 6.5's concept check, just applied to fusion instead of
    # reranking. If both retrievers only returned k=5, a chunk sitting
    # at dense rank #7 but sparse rank #1 would already be excluded from
    # the dense list before RRF ever got a chance to reward it for
    # showing up strongly in the OTHER list. Fetching 10 from each gives
    # RRF real candidates to actually fuse, not just re-sort the same 5.
    FETCH_K = 10

    # retrieve() returns list[tuple[Document, float]] — strip the score
    # here. RRF only ever needs rank POSITION (established back in
    # 6.6.3/6.6.4), never the raw score value, so the score is dead
    # weight past this point.
    dense_results = retrieve(vector_store, query, k=FETCH_K)
    dense_docs = [doc for doc, _score in dense_results]

    # sparse_retrieve() already returns list[Document], no scores —
    # that design choice in 6.6.3 is exactly what makes this call site
    # symmetrical with the dense one above, once the score is stripped.
    sparse_docs = sparse_retrieve(bm25_index, chunks, query, k=FETCH_K)

    fused = reciprocal_rank_fusion([dense_docs, sparse_docs])

    return fused[:k]
