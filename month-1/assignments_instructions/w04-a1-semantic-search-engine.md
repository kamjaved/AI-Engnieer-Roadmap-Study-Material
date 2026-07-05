# Assignment 4.1: Capstone -- Semantic Search Engine

> **Week 4 (Capstone)** | [Back to Week 4 Plan](../week-4.md)

## Title
**Capstone Project, Part 1: Semantic Search Engine** -- Your First Full-Stack AI Application

## Objective
Build a complete semantic search engine from scratch: a Python FastAPI backend that ingests documents (PDF, text, markdown), chunks them using multiple strategies, generates embeddings, stores them in a vector database, and exposes a search API with metadata filtering. Add a simple React frontend and containerize everything with Docker. This project synthesizes everything from Month 1 into one deployable application.

## Difficulty
Intermediate-Advanced

## Estimated Time
10-12 hours across Week 4 (break it into phases)

## Prerequisites
- Completed all prior Month 1 assignments (especially 2.2 Pydantic, 2.3 FastAPI, 1.2 Embeddings)
- Python 3.10+, Node.js 18+, Docker installed
- An embedding model (sentence-transformers for free, or OpenAI API key)
- Install Python dependencies:
```bash
pip install fastapi uvicorn[standard] sentence-transformers chromadb pypdf2 python-multipart pydantic-settings python-dotenv rich structlog
```
- **Optional (for pgvector path):** PostgreSQL with pgvector extension, `pip install asyncpg sqlalchemy pgvector`

## Why This Matters
Semantic search is the foundation of RAG (Retrieval-Augmented Generation), which is the most commercially important pattern in GenAI today. Nearly every AI startup has some form of "search your documents with AI" product. By building one from scratch, you will:
- Understand the full RAG retrieval pipeline
- Learn document processing, chunking, and embedding -- the critical pre-LLM steps
- Experience the trade-offs between chunking strategies (this is where most RAG systems succeed or fail)
- Deploy a real application, not just a script

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│  [Upload] [Search Bar] [Results with highlights]     │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / SSE
┌──────────────────────▼──────────────────────────────┐
│                  FastAPI Backend                      │
│                                                      │
│  POST /api/documents/upload   (ingest)               │
│  GET  /api/documents          (list)                 │
│  POST /api/search             (semantic search)      │
│  GET  /api/health             (health check)         │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────┐   │
│  │ Chunking │ │Embedding │ │  Vector Store      │   │
│  │ Pipeline │→│ Engine   │→│  (ChromaDB/pgvec)  │   │
│  └──────────┘ └──────────┘ └───────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Detailed Instructions

### Phase 1: Project Structure and Backend Foundation (2 hours)

#### Step 1.1: Project Setup

```
semantic-search-engine/
  backend/
    app/
      __init__.py
      main.py
      config.py
      models/
        __init__.py
        documents.py
        search.py
      services/
        __init__.py
        document_processor.py
        chunker.py
        embedder.py
        vector_store.py
        search_service.py
      routes/
        __init__.py
        documents.py
        search.py
        health.py
    tests/
      __init__.py
      test_chunker.py
      test_search.py
    requirements.txt
    Dockerfile
  frontend/
    src/
      components/
        SearchBar.tsx
        DocumentUpload.tsx
        SearchResults.tsx
      App.tsx
      api.ts
    package.json
    Dockerfile
  docker-compose.yml
  DECISIONS.md
  README.md
```

#### Step 1.2: Configuration

`backend/app/config.py`:
```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "Semantic Search Engine"
    app_version: str = "0.1.0"
    debug: bool = False

    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"  # Local model (free)
    embedding_dimension: int = 384  # Matches all-MiniLM-L6-v2
    # Set to "openai" to use OpenAI embeddings instead
    embedding_provider: str = "local"
    openai_api_key: str | None = None

    # Vector Store
    vector_store: str = "chromadb"  # "chromadb" or "pgvector"
    chroma_persist_dir: str = "./data/chroma"
    postgres_url: str | None = None

    # Chunking
    default_chunk_size: int = 512
    default_chunk_overlap: int = 50

    # Upload
    max_file_size_mb: int = 50
    allowed_extensions: list[str] = [".pdf", ".txt", ".md"]
    upload_dir: str = "./data/uploads"

    # CORS
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

#### Step 1.3: Data Models

`backend/app/models/documents.py`:
```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ChunkingStrategy(str, Enum):
    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"


class DocumentMetadata(BaseModel):
    """Metadata extracted from a document."""
    filename: str
    file_type: str
    file_size_bytes: int
    page_count: int | None = None
    word_count: int = 0
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str] = Field(default_factory=list)
    source: str | None = None


class DocumentChunk(BaseModel):
    """A single chunk of a document with its embedding."""
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: dict = Field(default_factory=dict)
    # Embedding stored separately in vector store


class Document(BaseModel):
    """A complete ingested document."""
    document_id: str
    metadata: DocumentMetadata
    chunk_count: int
    status: str = "processed"  # "processing", "processed", "error"
    error_message: str | None = None


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    processing_time_ms: float
    message: str
```

`backend/app/models/search.py`:
```python
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(5, ge=1, le=50)
    min_score: float = Field(0.0, ge=0.0, le=1.0)
    filter_file_type: str | None = None
    filter_tags: list[str] | None = None
    include_metadata: bool = True


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float  # Cosine similarity score
    metadata: dict = Field(default_factory=dict)
    highlights: list[str] = Field(
        default_factory=list,
        description="Relevant text snippets"
    )


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    total_results: int
    search_time_ms: float
    embedding_time_ms: float
```

### Phase 2: Document Ingestion Pipeline (2-3 hours)

#### Step 2.1: Document Processor

`backend/app/services/document_processor.py`:
```python
"""
Reads raw files and extracts text content.
Supports: PDF, plain text, Markdown
"""
import os
from pathlib import Path


class DocumentProcessor:
    """Extract text content from various file formats."""

    def process(self, file_path: str) -> tuple[str, dict]:
        """
        Process a file and return (text_content, metadata).
        """
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext == ".pdf":
            return self._process_pdf(path)
        elif ext == ".txt":
            return self._process_text(path)
        elif ext == ".md":
            return self._process_markdown(path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _process_pdf(self, path: Path) -> tuple[str, dict]:
        """Extract text from PDF."""
        from PyPDF2 import PdfReader

        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        content = "\n\n".join(pages)
        metadata = {
            "page_count": len(reader.pages),
            "file_type": "pdf",
        }
        return content, metadata

    def _process_text(self, path: Path) -> tuple[str, dict]:
        """Read plain text file."""
        content = path.read_text(encoding="utf-8")
        return content, {"file_type": "txt"}

    def _process_markdown(self, path: Path) -> tuple[str, dict]:
        """Read markdown file (keep as-is for now)."""
        content = path.read_text(encoding="utf-8")
        return content, {"file_type": "md"}
```

#### Step 2.2: Chunking Pipeline (THE CRITICAL COMPONENT)

`backend/app/services/chunker.py`:

This is where most RAG systems succeed or fail. Implement two strategies and compare them.

```python
"""
Document chunking strategies.

Chunking quality directly determines search quality.
Bad chunks = irrelevant search results = bad RAG output.
"""
import re
import uuid
from app.models.documents import DocumentChunk, ChunkingStrategy


class Chunker:
    """Split documents into chunks for embedding."""

    def chunk(
        self,
        text: str,
        document_id: str,
        strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ) -> list[DocumentChunk]:
        if strategy == ChunkingStrategy.FIXED_SIZE:
            return self._fixed_size_chunks(
                text, document_id, chunk_size, chunk_overlap
            )
        elif strategy == ChunkingStrategy.SEMANTIC:
            return self._semantic_chunks(
                text, document_id, chunk_size
            )
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def _fixed_size_chunks(
        self,
        text: str,
        document_id: str,
        chunk_size: int,
        overlap: int,
    ) -> list[DocumentChunk]:
        """
        Strategy 1: Fixed-size chunks with overlap.

        Simple and reliable. Works well for uniform text.
        Risk: May split mid-sentence or mid-paragraph.
        Mitigation: Use overlap to maintain context at boundaries.
        """
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence end within the last 20% of the chunk
                search_start = end - int(chunk_size * 0.2)
                search_region = text[search_start:end]
                last_period = search_region.rfind(". ")
                if last_period != -1:
                    end = search_start + last_period + 1

            chunk_text = text[start:end].strip()

            if chunk_text:  # Skip empty chunks
                chunks.append(DocumentChunk(
                    chunk_id=f"{document_id}_chunk_{chunk_index}",
                    document_id=document_id,
                    content=chunk_text,
                    chunk_index=chunk_index,
                    start_char=start,
                    end_char=end,
                    metadata={
                        "strategy": "fixed_size",
                        "chunk_size": chunk_size,
                    },
                ))
                chunk_index += 1

            start = end - overlap
            if start >= len(text) - overlap:
                break

        return chunks

    def _semantic_chunks(
        self,
        text: str,
        document_id: str,
        target_size: int,
    ) -> list[DocumentChunk]:
        """
        Strategy 2: Semantic chunking.

        Splits on natural boundaries: paragraphs, sections, headers.
        Better for structured documents (markdown, reports).
        Risk: Chunk sizes vary widely. Some chunks may be too small
        (a one-line paragraph) or too large (a massive paragraph).
        """
        # Split into paragraphs first
        paragraphs = re.split(r"\n\s*\n", text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        chunks = []
        current_chunk = ""
        current_start = 0
        chunk_index = 0
        char_pos = 0

        for para in paragraphs:
            # If adding this paragraph would exceed target size,
            # and we already have content, finalize current chunk
            if (
                current_chunk
                and len(current_chunk) + len(para) > target_size
            ):
                chunks.append(DocumentChunk(
                    chunk_id=f"{document_id}_chunk_{chunk_index}",
                    document_id=document_id,
                    content=current_chunk.strip(),
                    chunk_index=chunk_index,
                    start_char=current_start,
                    end_char=current_start + len(current_chunk),
                    metadata={"strategy": "semantic"},
                ))
                chunk_index += 1
                current_start = char_pos
                current_chunk = ""

            # If a single paragraph exceeds target, chunk it by sentences
            if len(para) > target_size:
                if current_chunk:
                    chunks.append(DocumentChunk(
                        chunk_id=f"{document_id}_chunk_{chunk_index}",
                        document_id=document_id,
                        content=current_chunk.strip(),
                        chunk_index=chunk_index,
                        start_char=current_start,
                        end_char=current_start + len(current_chunk),
                        metadata={"strategy": "semantic"},
                    ))
                    chunk_index += 1
                    current_chunk = ""

                sentences = re.split(r"(?<=[.!?])\s+", para)
                sent_chunk = ""
                sent_start = char_pos
                for sent in sentences:
                    if len(sent_chunk) + len(sent) > target_size and sent_chunk:
                        chunks.append(DocumentChunk(
                            chunk_id=f"{document_id}_chunk_{chunk_index}",
                            document_id=document_id,
                            content=sent_chunk.strip(),
                            chunk_index=chunk_index,
                            start_char=sent_start,
                            end_char=sent_start + len(sent_chunk),
                            metadata={"strategy": "semantic_sentence_split"},
                        ))
                        chunk_index += 1
                        sent_start = sent_start + len(sent_chunk)
                        sent_chunk = ""
                    sent_chunk += sent + " "

                if sent_chunk.strip():
                    current_chunk = sent_chunk
                    current_start = sent_start
            else:
                current_chunk += para + "\n\n"

            char_pos += len(para) + 2  # +2 for paragraph separator

        # Flush remaining content
        if current_chunk.strip():
            chunks.append(DocumentChunk(
                chunk_id=f"{document_id}_chunk_{chunk_index}",
                document_id=document_id,
                content=current_chunk.strip(),
                chunk_index=chunk_index,
                start_char=current_start,
                end_char=current_start + len(current_chunk),
                metadata={"strategy": "semantic"},
            ))

        return chunks
```

**Write tests** in `tests/test_chunker.py`:
```python
from app.services.chunker import Chunker
from app.models.documents import ChunkingStrategy


def test_fixed_size_basic():
    chunker = Chunker()
    text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four."
    chunks = chunker.chunk(text, "doc1", ChunkingStrategy.FIXED_SIZE, chunk_size=50, chunk_overlap=10)
    assert len(chunks) > 1
    assert all(c.document_id == "doc1" for c in chunks)
    # Verify no content is lost
    # (overlap means some content appears in multiple chunks, but
    # concatenating unique portions should reconstruct the original)


def test_semantic_respects_paragraphs():
    chunker = Chunker()
    text = "Paragraph one about dogs.\n\nParagraph two about cats.\n\nParagraph three about birds."
    chunks = chunker.chunk(text, "doc2", ChunkingStrategy.SEMANTIC, chunk_size=100)
    # Each paragraph is short enough to be its own chunk
    # (or combined if under target size)
    assert len(chunks) >= 1
    full_text = " ".join(c.content for c in chunks)
    assert "dogs" in full_text
    assert "cats" in full_text
    assert "birds" in full_text


def test_empty_text():
    chunker = Chunker()
    chunks = chunker.chunk("", "doc3", ChunkingStrategy.FIXED_SIZE)
    assert len(chunks) == 0


def test_chunk_ids_are_unique():
    chunker = Chunker()
    text = "A " * 1000  # Long enough to produce multiple chunks
    chunks = chunker.chunk(text, "doc4", ChunkingStrategy.FIXED_SIZE, chunk_size=100)
    ids = [c.chunk_id for c in chunks]
    assert len(ids) == len(set(ids))
```

#### Step 2.3: Embedding Engine

`backend/app/services/embedder.py`:
```python
"""
Generate embeddings for text chunks.
Supports local (sentence-transformers) and API (OpenAI) models.
"""
import numpy as np
from app.config import get_settings


class Embedder:
    """Generate text embeddings."""

    def __init__(self):
        self.settings = get_settings()
        self._model = None

    @property
    def model(self):
        if self._model is None:
            if self.settings.embedding_provider == "local":
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(
                    self.settings.embedding_model
                )
            # OpenAI path handled separately
        return self._model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts. Returns list of embedding vectors."""
        if self.settings.embedding_provider == "openai":
            return self._embed_openai(texts)
        return self._embed_local(texts)

    def embed_query(self, query: str) -> list[float]:
        """Embed a single search query."""
        results = self.embed_texts([query])
        return results[0]

    def _embed_local(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False
        )
        return embeddings.tolist()

    def _embed_openai(self, texts: list[str]) -> list[list[float]]:
        from openai import OpenAI
        client = OpenAI(api_key=self.settings.openai_api_key)
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-small",
        )
        return [item.embedding for item in response.data]
```

#### Step 2.4: Vector Store

`backend/app/services/vector_store.py`:
```python
"""
Vector storage and retrieval using ChromaDB.
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import get_settings
from app.models.documents import DocumentChunk
from app.models.search import SearchResult


class VectorStore:
    """Store and search document embeddings."""

    def __init__(self):
        settings = get_settings()
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        """Add document chunks with their embeddings to the store."""
        self.collection.add(
            ids=[c.chunk_id for c in chunks],
            embeddings=embeddings,
            documents=[c.content for c in chunks],
            metadatas=[
                {
                    "document_id": c.document_id,
                    "chunk_index": c.chunk_index,
                    "start_char": c.start_char,
                    "end_char": c.end_char,
                    **c.metadata,
                }
                for c in chunks
            ],
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        filter_dict: dict | None = None,
    ) -> list[SearchResult]:
        """Search for similar chunks."""
        where = filter_dict if filter_dict else None

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        search_results = []
        if results["ids"] and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                # ChromaDB returns distances, convert to similarity
                distance = results["distances"][0][i]
                similarity = 1 - distance  # For cosine distance

                search_results.append(SearchResult(
                    chunk_id=results["ids"][0][i],
                    document_id=results["metadatas"][0][i].get(
                        "document_id", ""
                    ),
                    content=results["documents"][0][i],
                    score=round(similarity, 4),
                    metadata=results["metadatas"][0][i],
                ))

        return search_results

    def delete_document(self, document_id: str) -> None:
        """Delete all chunks for a document."""
        self.collection.delete(
            where={"document_id": document_id}
        )

    def get_stats(self) -> dict:
        """Get store statistics."""
        return {
            "total_chunks": self.collection.count(),
        }
```

### Phase 3: Search API (2 hours)

#### Step 3.1: Search Service

`backend/app/services/search_service.py`:
```python
import time
import uuid
import os
from app.services.document_processor import DocumentProcessor
from app.services.chunker import Chunker
from app.services.embedder import Embedder
from app.services.vector_store import VectorStore
from app.models.documents import (
    Document, DocumentMetadata, DocumentChunk,
    ChunkingStrategy, UploadResponse
)
from app.models.search import SearchRequest, SearchResponse
from app.config import get_settings


class SearchService:
    """Orchestrates document ingestion and search."""

    def __init__(self):
        self.processor = DocumentProcessor()
        self.chunker = Chunker()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.settings = get_settings()
        self._documents: dict[str, Document] = {}  # In-memory registry

    async def ingest_document(
        self,
        file_path: str,
        filename: str,
        tags: list[str] | None = None,
        chunking_strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE,
    ) -> UploadResponse:
        """Process, chunk, embed, and store a document."""
        start = time.time()
        document_id = uuid.uuid4().hex[:12]

        # 1. Extract text
        text, file_metadata = self.processor.process(file_path)

        # 2. Chunk
        chunks = self.chunker.chunk(
            text,
            document_id,
            strategy=chunking_strategy,
            chunk_size=self.settings.default_chunk_size,
            chunk_overlap=self.settings.default_chunk_overlap,
        )

        if not chunks:
            raise ValueError("Document produced no chunks. It may be empty.")

        # 3. Embed all chunks
        chunk_texts = [c.content for c in chunks]
        embeddings = self.embedder.embed_texts(chunk_texts)

        # 4. Store in vector database
        # Add file-level metadata to each chunk
        for chunk in chunks:
            chunk.metadata.update({
                "filename": filename,
                "file_type": file_metadata.get("file_type", "unknown"),
                **({"tags": ",".join(tags)} if tags else {}),
            })

        self.vector_store.add_chunks(chunks, embeddings)

        # 5. Register document
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        doc = Document(
            document_id=document_id,
            metadata=DocumentMetadata(
                filename=filename,
                file_type=file_metadata.get("file_type", "unknown"),
                file_size_bytes=file_size,
                page_count=file_metadata.get("page_count"),
                word_count=len(text.split()),
                tags=tags or [],
            ),
            chunk_count=len(chunks),
        )
        self._documents[document_id] = doc

        elapsed = (time.time() - start) * 1000
        return UploadResponse(
            document_id=document_id,
            filename=filename,
            chunk_count=len(chunks),
            processing_time_ms=round(elapsed, 2),
            message=f"Successfully ingested {filename}: {len(chunks)} chunks created.",
        )

    async def search(self, request: SearchRequest) -> SearchResponse:
        """Perform semantic search."""
        # 1. Embed the query
        embed_start = time.time()
        query_embedding = self.embedder.embed_query(request.query)
        embed_time = (time.time() - embed_start) * 1000

        # 2. Build filters
        filters = None
        if request.filter_file_type:
            filters = {"file_type": request.filter_file_type}

        # 3. Search vector store
        search_start = time.time()
        results = self.vector_store.search(
            query_embedding,
            top_k=request.top_k,
            filter_dict=filters,
        )
        search_time = (time.time() - search_start) * 1000

        # 4. Filter by min score
        if request.min_score > 0:
            results = [r for r in results if r.score >= request.min_score]

        # 5. Add highlights (simple keyword highlighting)
        query_words = set(request.query.lower().split())
        for result in results:
            sentences = result.content.split(". ")
            highlights = []
            for sent in sentences:
                if any(w in sent.lower() for w in query_words):
                    highlights.append(sent.strip())
            result.highlights = highlights[:3]  # Top 3 highlights

        return SearchResponse(
            query=request.query,
            results=results,
            total_results=len(results),
            search_time_ms=round(search_time, 2),
            embedding_time_ms=round(embed_time, 2),
        )

    def list_documents(self) -> list[Document]:
        return list(self._documents.values())

    async def delete_document(self, document_id: str) -> None:
        self.vector_store.delete_document(document_id)
        self._documents.pop(document_id, None)
```

#### Step 3.2: API Routes

`backend/app/routes/documents.py`:
```python
import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.documents import (
    Document, UploadResponse, ChunkingStrategy
)
from app.services.search_service import SearchService
from app.config import get_settings

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Singleton service (in production, use dependency injection)
_service: SearchService | None = None

def get_service() -> SearchService:
    global _service
    if _service is None:
        _service = SearchService()
    return _service


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    tags: str = Form(""),
    chunking_strategy: ChunkingStrategy = Form(ChunkingStrategy.FIXED_SIZE),
):
    """Upload and ingest a document."""
    settings = get_settings()

    # Validate file type
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {ext} not supported. Allowed: {settings.allowed_extensions}",
        )

    # Save uploaded file
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(
        settings.upload_dir, f"{uuid.uuid4().hex}_{file.filename}"
    )

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        result = await get_service().ingest_document(
            file_path, file.filename or "unknown", tag_list, chunking_strategy
        )
        return result
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[Document])
async def list_documents():
    """List all ingested documents."""
    return get_service().list_documents()


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its chunks."""
    await get_service().delete_document(document_id)
    return {"message": f"Document {document_id} deleted"}
```

`backend/app/routes/search.py`:
```python
from fastapi import APIRouter, HTTPException
from app.models.search import SearchRequest, SearchResponse
from app.routes.documents import get_service

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Perform semantic search across all documents."""
    try:
        return await get_service().search(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

`backend/app/routes/health.py`:
```python
import time
from fastapi import APIRouter
from app.config import get_settings
from app.routes.documents import get_service

router = APIRouter(tags=["health"])

_start = time.time()


@router.get("/health")
async def health():
    settings = get_settings()
    service = get_service()
    stats = service.vector_store.get_stats()
    return {
        "status": "ok",
        "version": settings.app_version,
        "embedding_model": settings.embedding_model,
        "vector_store": settings.vector_store,
        "total_chunks": stats["total_chunks"],
        "total_documents": len(service.list_documents()),
        "uptime_seconds": round(time.time() - _start, 2),
    }
```

#### Step 3.3: Main App

`backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routes import documents, search, health

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Semantic search engine with document ingestion, "
                "chunking, embedding, and vector search.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(search.router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Semantic Search Engine API", "docs": "/docs"}
```

Test it:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
# Open http://localhost:8000/docs
```

### Phase 4: React Frontend (2 hours)

You already know React, so this should be fast. Build a minimal but functional UI.

#### Step 4.1: Setup

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install axios
```

#### Step 4.2: API Client

`frontend/src/api.ts`:
```typescript
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export interface SearchResult {
  chunk_id: string;
  document_id: string;
  content: string;
  score: number;
  metadata: Record<string, any>;
  highlights: string[];
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total_results: number;
  search_time_ms: number;
  embedding_time_ms: number;
}

export interface Document {
  document_id: string;
  metadata: {
    filename: string;
    file_type: string;
    word_count: number;
    tags: string[];
  };
  chunk_count: number;
  status: string;
}

export const api = {
  search: async (query: string, topK = 5): Promise<SearchResponse> => {
    const { data } = await axios.post(`${API_BASE}/search/`, {
      query,
      top_k: topK,
    });
    return data;
  },

  uploadDocument: async (
    file: File,
    tags: string = '',
    strategy: string = 'fixed_size'
  ) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('tags', tags);
    formData.append('chunking_strategy', strategy);
    const { data } = await axios.post(
      `${API_BASE}/documents/upload`,
      formData
    );
    return data;
  },

  listDocuments: async (): Promise<Document[]> => {
    const { data } = await axios.get(`${API_BASE}/documents/`);
    return data;
  },

  health: async () => {
    const { data } = await axios.get('http://localhost:8000/health');
    return data;
  },
};
```

#### Step 4.3: Components

Build these three components:

1. **SearchBar**: Text input with search button. Shows search time after results.
2. **DocumentUpload**: Drag-and-drop file upload with tag input and strategy selector.
3. **SearchResults**: Displays results as cards with score badges, content preview, and highlighted snippets.

Keep it simple -- you know React. Focus on functionality over styling. Use plain CSS or any library you prefer.

#### Step 4.4: App Assembly

`frontend/src/App.tsx` should have:
- A header with the app name
- A tab or toggle between "Search" and "Upload" views
- The document list sidebar showing ingested documents
- The search results area

### Phase 5: Docker and Deployment (2 hours)

#### Step 5.1: Backend Dockerfile

`backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directories
RUN mkdir -p data/uploads data/chroma

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 5.2: Frontend Dockerfile

`frontend/Dockerfile`:
```dockerfile
FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

`frontend/nginx.conf`:
```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
    location /api/ {
        proxy_pass http://backend:8000/api/;
    }
    location /health {
        proxy_pass http://backend:8000/health;
    }
}
```

#### Step 5.3: Docker Compose

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - EMBEDDING_PROVIDER=local
      - EMBEDDING_MODEL=all-MiniLM-L6-v2
      - VECTOR_STORE=chromadb
      - CHROMA_PERSIST_DIR=/app/data/chroma
    volumes:
      - chroma_data:/app/data/chroma
      - upload_data:/app/data/uploads

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  chroma_data:
  upload_data:
```

Build and run:
```bash
docker-compose up --build
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

#### Step 5.4: Deploy to Free Tier (Optional)

For **Render.com** (free tier):
1. Push to GitHub
2. Create a new Web Service for the backend (point to `/backend`)
3. Create a new Static Site for the frontend (point to `/frontend`)
4. Set environment variables in the Render dashboard

For **Railway.app** (free tier with limits):
1. Connect your GitHub repo
2. Railway auto-detects the Dockerfiles
3. Set environment variables in the Railway dashboard

---

## DECISIONS.md Template

Create this file to document your architectural decisions:

```markdown
# Architecture Decisions

## Decision 1: Vector Store Choice
**Choice:** ChromaDB
**Alternatives considered:** pgvector, Pinecone, Weaviate
**Reasoning:** ChromaDB is embedded (no separate server), has a Python-native API, and persists to disk. Good for prototyping. pgvector would be better for production (SQL queries, joins, ACID).
**Trade-offs:** ChromaDB has limited filtering capabilities compared to pgvector. No SQL. Harder to inspect data.

## Decision 2: Chunking Strategy
**Choice:** Fixed-size with sentence-boundary snapping (default), semantic chunking (optional)
**Reasoning:** Fixed-size is predictable and works for most documents. Semantic chunking is better for structured docs but produces variable-size chunks.
**Trade-offs:** Fixed-size may split related content. Semantic may produce very small or very large chunks.

## Decision 3: Embedding Model
**Choice:** all-MiniLM-L6-v2 (local, free)
**Alternatives:** OpenAI text-embedding-3-small, Cohere embed-v3
**Reasoning:** Free, fast, runs locally, 384 dimensions (small = fast search). Quality is good enough for a prototype.
**Trade-offs:** Lower quality than OpenAI embeddings. English-focused. 384 dims vs 1536 dims means less nuance.

## Decision 4: [Add your own decisions here]
...
```

---

## README Template

```markdown
# Semantic Search Engine

A full-stack semantic search application built with FastAPI, ChromaDB, and React.

## Features
- Document ingestion (PDF, TXT, Markdown)
- Two chunking strategies (fixed-size, semantic)
- Semantic search with cosine similarity
- Metadata filtering
- Docker deployment

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OR: Python 3.10+ and Node.js 18+

### With Docker
\`\`\`bash
docker-compose up --build
# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
\`\`\`

### Without Docker
\`\`\`bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
\`\`\`

## API Endpoints
- `POST /api/documents/upload` - Upload and ingest a document
- `GET /api/documents/` - List all documents
- `POST /api/search/` - Semantic search
- `GET /health` - Health check

## Architecture
[Include the architecture diagram from above]

## Chunking Strategies
[Explain your two strategies and when to use each]

## Known Limitations
[Be honest about what does not work well]
```

---

## Expected Output

After completing all phases:

1. **Backend API** at `http://localhost:8000/docs` with interactive Swagger UI
2. **Upload a PDF** and see it chunked, embedded, and stored
3. **Search by meaning**: searching "how to handle errors" should find chunks about error handling even if they do not contain those exact words
4. **React frontend** showing search results with scores and highlights
5. **Docker deployment** with `docker-compose up`
6. **DECISIONS.md** documenting at least 4 architectural choices
7. All chunker tests passing

---

## Evaluation Criteria

| Criteria | Weight | Description |
|---|---|---|
| **Ingestion Pipeline** | 20% | Documents are correctly processed, chunked, and stored |
| **Search Quality** | 20% | Semantic search returns relevant results, not just keyword matches |
| **Chunking Implementation** | 15% | Both strategies work correctly, tests pass |
| **API Design** | 15% | Clean REST endpoints, proper error handling, Swagger docs |
| **Frontend** | 10% | Functional UI for upload and search (does not need to be beautiful) |
| **Docker** | 10% | `docker-compose up` works end to end |
| **DECISIONS.md** | 10% | Thoughtful documentation of trade-offs and choices |

---

## Bonus Challenges

1. **Hybrid Search**: Combine semantic search (embeddings) with keyword search (BM25). Use reciprocal rank fusion to merge results. This is how production search engines work.
2. **Re-ranking**: After initial retrieval, use a cross-encoder model (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) to re-rank results for higher precision.
3. **Chunk Context Enrichment**: Before embedding, prepend each chunk with its document title and section header. Compare search quality with and without enrichment.
4. **Evaluation Suite**: Create a set of 20 query-document relevance pairs. Calculate Mean Reciprocal Rank (MRR) and Recall@k for your search engine. Compare chunking strategies quantitatively.
5. **Real-time Ingestion Progress**: Use WebSockets to show real-time progress during document ingestion (parsing -> chunking -> embedding -> storing).
6. **pgvector Path**: Implement the pgvector alternative to ChromaDB. Compare query performance, filtering capabilities, and deployment complexity.
7. **Multi-modal**: Add image support -- extract text from images via OCR (pytesseract) and embed it alongside text documents.

---

## Key Concepts You Will Learn

- **Document processing pipeline**: The full journey from raw file to searchable content
- **Chunking strategies**: The most impactful design decision in any RAG system
- **Embedding generation**: Converting text to vectors for similarity search
- **Vector databases**: How ChromaDB (and pgvector) store and search embeddings
- **Cosine similarity search**: Finding semantically similar content
- **Full-stack AI app architecture**: How frontend, backend, and AI components connect
- **Docker containerization**: Packaging your AI app for deployment
- **Architectural decision documentation**: Professional engineering practice
