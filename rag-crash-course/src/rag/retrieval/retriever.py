from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from rag.config import settings


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
) -> list[tuple[Document, float]]:
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
        query,
        k=k,
        # filter_dict or None: an empty {} dict is falsy in Python, so
        # if nothing was provided this evaluates to None — Pinecone
        # treats filter=None as "no filter," not "match nothing."
        # Passing filter={} explicitly would behave differently in some
        # vector DBs, so this line matters, not just style.
        filter=filter_dict or None,
    )
