# Pinecone needs the exact vector length UPFRONT at index-creation time —
# it pre-allocates storage shaped for that dimension. Get this number
# wrong (or stale) and every upsert fails with a dimension mismatch.
#
# Keyed by model name so the dimension is always DERIVED from
# settings.EMBEDDING_MODEL, never typed as a loose magic number.
# If EMBEDDING_MODEL ever changes in .env, the correct dimension is
# picked up automatically wherever this dict is looked up — instead of
# some other piece of code still silently pointing at the old number.

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from rag.config import settings

EMBEDDING_DIMENSIONS: dict[str, int] = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
}


def get_or_create_index(pc: Pinecone) -> None:
    if pc.has_index(settings.PINECONE_INDEX_NAME):
        return

    pc.create_index(
        name=settings.PINECONE_INDEX_NAME,
        # Derived from 5.1's lookup table, keyed by whatever model
        # settings.py currently points at — never a hardcoded number.
        dimension=EMBEDDING_DIMENSIONS[settings.EMBEDDING_MODEL],
        # cosine — same reasoning as Lesson 4: the safe default for text
        # embeddings, whether or not a given model guarantees its
        # vectors are unit-normalized.
        metric="cosine",
        # Serverless = Pinecone auto-scales capacity for you; you just
        # pick where it's hosted (cloud + region). This is the modern
        # default over pod-based indexes, which make YOU pre-size and
        # pay for fixed capacity whether you're using it or not — closer
        # to provisioning your own EC2 box than using a managed service.
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


def index_chunks(chunks: list[Document]) -> PineconeVectorStore:
    # Same model settings.py already points at. This is the ONE place
    # index-time embedding happens — whatever model is named here gets
    # baked into every vector this call writes. It must always match
    # what you embed QUERIES with later, or you hit Lesson 4's silent
    # same-dimension-different-model failure.
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)

    return PineconeVectorStore.from_documents(
        documents=chunks,  # page_content gets embedded; the full
        # metadata dict rides along as the
        # vector's Pinecone metadata
        embedding=embeddings,
        index_name=settings.PINECONE_INDEX_NAME,
        # THIS line is what makes re-ingestion safe. Under the hood,
        # if you don't pass ids=, LangChain generates a fresh random
        # uuid4 per chunk on every call — so re-running ingestion on an
        # unchanged file would silently create brand-new vector IDs
        # and pile up duplicates next to the old ones, forever.
        # Passing the deterministic chunk_id from Lesson 3
        # (f"{source}::{index}") means the SAME chunk always maps to
        # the SAME Pinecone vector ID — so upsert overwrites in place
        # instead of duplicating. This is the direct payoff of a
        # decision you made two lessons ago.
        ids=[c.metadata["chunk_id"] for c in chunks],
    )
