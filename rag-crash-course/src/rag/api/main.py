from fastapi import FastAPI
from pydantic import BaseModel

from rag.generation.chain import answer_question
from rag.indexing.embed_and_index import index_chunks
from rag.ingestion.chunker import chunk_documents
from rag.ingestion.loader import load_documents
from rag.retrieval.retriever import get_vector_store

app = FastAPI(title="Turab Industries RAG API")
vector_store = get_vector_store()


class QueryRequest(BaseModel):
    question: str
    k: int = 5
    team: str | None = None
    doc_type: str | None = None


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ingest")
def ingest():
    documents = load_documents()
    chunks = chunk_documents(documents)
    index_chunks(chunks)

    return {"chunks_indexed": len(chunks)}


@app.post("/query")
def query(request: QueryRequest):
    result = answer_question(
        vector_store,
        request.question,
        k=request.k,
        team=request.team,
        doc_type=request.doc_type,
    )

    print(result)
    # Deliberately NOT returning result["raw_chunks"] here
    # We omit raw_chunks in API responses because it's debug-only data  in outside world no need to
    # expose and leak internals + add payload weight.

    return {
        "answer": result["answer"],
        "sources": result["sources"],
    }
