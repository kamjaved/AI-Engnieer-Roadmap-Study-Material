# Week 4 — Embeddings & Vector Search

> **Month 1 · Week 4 of 16** | Est. 12-15 hours | Prerequisites: Weeks 1-3 (LLM fundamentals, APIs, prompt engineering)
> Back to [Roadmap](../ROADMAP.md) | Next: Month 2, Week 5 (RAG Architecture)

---

## Why This Week Matters

Embeddings and vector search are the foundation of retrieval-augmented generation (RAG), which is the most commonly deployed LLM pattern in production. If you can only build one GenAI system well, it should be a retrieval system. This week you go from understanding embeddings as a concept (Week 1) to building a working semantic search pipeline. You will also scope and begin your first capstone project — a deployed system that demonstrates you can build, not just study.

---

## Lesson 4.1 — Embedding Models in Practice

### Sub-topics
- OpenAI text-embedding-3-small / text-embedding-3-large
- Sentence-transformers (open-source)
- Embedding dimensions vs quality tradeoff
- Batch embedding strategies
- Normalization

### Key Concepts

**OpenAI Embedding Models**

OpenAI offers two embedding models: `text-embedding-3-small` (1536 dimensions, cheaper) and `text-embedding-3-large` (3072 dimensions, higher quality). Both support a `dimensions` parameter that lets you reduce the output size via Matryoshka representation learning — you can request 256 or 512 dimensions from the large model and still get useful embeddings. This is a significant cost/performance lever.

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="How do vector databases work?",
    dimensions=512  # reduce from 1536 to 512 — less storage, faster search
)

embedding = response.data[0].embedding  # list of 512 floats
print(f"Dimensions: {len(embedding)}")
```

Key insight: `text-embedding-3-small` at 512 dimensions is often sufficient for most retrieval tasks and dramatically cheaper than the large model. Start small, benchmark, and only scale up if retrieval quality demands it.

**Sentence-Transformers (Open Source)**

For scenarios where you cannot send data to an external API (privacy, cost, latency), open-source embedding models are the answer. The `sentence-transformers` library provides access to hundreds of pre-trained models.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dimensions, fast
# Or: "BAAI/bge-large-en-v1.5" — 1024 dims, higher quality

texts = [
    "How do vector databases work?",
    "Vector DBs store embeddings for similarity search.",
    "The weather is nice today."
]

embeddings = model.encode(texts, normalize_embeddings=True)
# embeddings.shape = (3, 384)
```

Popular models to know:
- `all-MiniLM-L6-v2`: Fast, 384 dims, good baseline
- `BAAI/bge-large-en-v1.5`: High quality, 1024 dims, competitive with commercial models
- `nomic-embed-text-v1.5`: Strong performer with Matryoshka support
- `Cohere embed-v3`: Commercial but worth benchmarking against

**Embedding Dimensions vs Quality Tradeoff**

More dimensions capture more semantic nuance but cost more in storage and search time. The relationship is not linear — going from 256 to 512 dimensions gives a significant quality boost, but going from 1536 to 3072 gives diminishing returns for most tasks.

| Dimensions | Storage per 1M docs | Search speed | Quality |
|-----------|---------------------|-------------|---------|
| 256 | ~1 GB | Fastest | Good for broad similarity |
| 512 | ~2 GB | Fast | Good for most retrieval |
| 1024 | ~4 GB | Moderate | High — covers nuance |
| 1536 | ~6 GB | Slower | Diminishing returns begin |
| 3072 | ~12 GB | Slowest | Marginal gain over 1536 |

Production decision: Start with 512 dimensions. Benchmark retrieval quality (precision@k, recall@k) against your actual queries. Only increase if you see meaningful quality improvement on your data.

**Batch Embedding**

Embedding one document at a time is wasteful. Both OpenAI and sentence-transformers support batch processing, which is dramatically faster.

```python
# OpenAI — batch of up to 2048 inputs per request
texts = ["doc1...", "doc2...", "doc3...", ...]  # up to 2048
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)
embeddings = [item.embedding for item in response.data]

# sentence-transformers — automatically batches internally
embeddings = model.encode(texts, batch_size=64, show_progress_bar=True)
```

For large datasets (100K+ documents), implement a pipeline: read documents in chunks, embed each chunk, insert into vector DB, repeat. Use async calls for the OpenAI API to maximize throughput.

**Normalization**

Normalized embeddings have unit length (L2 norm = 1). When embeddings are normalized, cosine similarity is equivalent to dot product, which is faster to compute. Most embedding models output normalized vectors by default, but verify this for your model.

```python
import numpy as np

def normalize(embedding):
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding

# Verify normalization
emb = np.array(embedding)
print(f"L2 norm: {np.linalg.norm(emb):.4f}")  # should be ~1.0
```

If you are using cosine distance in your vector DB, normalization is handled automatically. If you are using inner product (dot product) distance, you must normalize beforehand for correct similarity ranking.

### Interview Questions

**Q1: When would you choose open-source embeddings over OpenAI's embedding API?**

A: Choose open-source when: (1) **Data privacy** — the data cannot leave your infrastructure (healthcare, finance, legal). (2) **Cost at scale** — embedding millions of documents with OpenAI adds up; a local model on a GPU is a one-time cost. (3) **Latency** — local inference eliminates network round-trips, critical for real-time search. (4) **Offline capability** — edge deployments or air-gapped environments. Choose OpenAI when: (1) You want maximum quality with minimal setup. (2) Your data volume is moderate (under 1M documents). (3) You do not have GPU infrastructure. (4) Rapid prototyping — no model management overhead. The best production systems often use both: OpenAI for the prototype, then benchmark against open-source models and switch if quality is comparable.

**Q2: Explain Matryoshka embeddings and why they matter for production systems.**

A: Matryoshka representation learning trains embeddings so that the first N dimensions are a valid, useful embedding on their own — like nested Russian dolls. OpenAI's text-embedding-3 models support this via the `dimensions` parameter. Why it matters: you can generate a 3072-dimension embedding once and store truncated versions for different use cases. A 256-dimension version works for coarse filtering, a 1024-dimension version for precise retrieval. This lets you trade storage and speed for quality at query time without re-embedding your entire corpus. It also enables multi-stage retrieval: fast search with small embeddings to get candidates, then re-rank with full-dimension embeddings.

**Q3: You have 5 million documents to embed. Design the embedding pipeline.**

A: Pipeline steps: (1) **Extract and clean text** — batch read documents, strip irrelevant content (headers, footers, boilerplate). (2) **Chunk** — split into semantic units (covered in Lesson 4.3). Store chunk-to-document mapping. (3) **Deduplicate** — hash chunks to avoid embedding duplicates. (4) **Embed in batches** — if using OpenAI, send 2048 texts per request with async calls (10-20 concurrent). If local, use GPU with batch_size=64-256. (5) **Insert into vector DB** — batch upsert (1000+ vectors per call). (6) **Validate** — spot-check random queries to verify retrieval quality. (7) **Monitor** — track embedding latency, API costs, and failure rate. For 5M docs with OpenAI text-embedding-3-small: roughly $0.02 per 1M tokens. If average doc is 500 tokens, that is 2.5B tokens total = ~$50. Time: 2-4 hours with concurrent requests. With local model on a decent GPU: 4-8 hours, zero API cost.

---

## Lesson 4.2 — Vector Databases

### Sub-topics
- ChromaDB (local development)
- pgvector (production — leverages your Postgres knowledge)
- Qdrant (awareness)
- FAISS (awareness)
- Indexing strategies (HNSW, IVF)
- Distance metrics (cosine, euclidean, dot product)

### Key Concepts

**ChromaDB — Local Development**

ChromaDB is the easiest vector database to start with. It runs in-process (no server needed), stores data in a local directory, and has a clean Python API. Perfect for prototyping and local development. Not ideal for production at scale.

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}  # distance metric
)

# Add documents (ChromaDB can auto-embed with a default model)
collection.add(
    documents=["Vector databases store embeddings", "LLMs generate text"],
    ids=["doc1", "doc2"],
    metadatas=[{"source": "textbook"}, {"source": "blog"}]
)

# Or add pre-computed embeddings
collection.add(
    embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    documents=["doc1 text", "doc2 text"],
    ids=["doc1", "doc2"],
    metadatas=[{"source": "textbook"}, {"source": "blog"}]
)

# Query
results = collection.query(
    query_texts=["How do embeddings work?"],
    n_results=5,
    where={"source": "textbook"}  # metadata filtering
)
```

ChromaDB strengths: zero config, built-in embedding support, metadata filtering. Limitations: single-process, no replication, limited scale (works well up to ~100K documents).

**pgvector — Production with PostgreSQL**

pgvector is a PostgreSQL extension that adds vector similarity search to your existing Postgres database. This is a strong production choice because: (1) you already know Postgres, (2) vectors live alongside your relational data (no separate system), (3) you get ACID transactions, backups, and tooling for free, (4) it scales well for most use cases (up to ~10M vectors).

```sql
-- Enable the extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table with a vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(512),  -- 512-dimension vectors
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create an HNSW index for fast similarity search
CREATE INDEX ON documents 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 200);

-- Insert a document
INSERT INTO documents (content, metadata, embedding)
VALUES (
    'Vector databases store embeddings for similarity search',
    '{"source": "textbook", "chapter": 4}',
    '[0.1, 0.2, 0.3, ...]'  -- 512-dim vector
);

-- Similarity search (cosine distance — lower is more similar)
SELECT id, content, 1 - (embedding <=> query_embedding) AS similarity
FROM documents
ORDER BY embedding <=> '[0.15, 0.25, ...]'  -- <=> is cosine distance
LIMIT 10;

-- Combined: vector search + metadata filter + full-text
SELECT id, content, 1 - (embedding <=> query_embedding) AS similarity
FROM documents
WHERE metadata->>'source' = 'textbook'
  AND content ILIKE '%vector%'
ORDER BY embedding <=> '[0.15, 0.25, ...]'
LIMIT 10;
```

Python integration with SQLAlchemy or asyncpg:

```python
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(512))

# Insert
doc = Document(content="...", embedding=embedding_list)
session.add(doc)
session.commit()

# Query — nearest neighbors
from pgvector.sqlalchemy import Vector
from sqlalchemy import text

results = session.query(Document).order_by(
    Document.embedding.cosine_distance(query_embedding)
).limit(10).all()
```

**Qdrant (Awareness)**

Qdrant is a purpose-built vector database (Rust-based) with strong filtering, payload indexing, and horizontal scaling. Use it when: you need to scale beyond what pgvector handles comfortably (10M+ vectors), or you need advanced features like quantization, multi-vector search, or complex filter conditions at scale. It runs as a standalone service or in Qdrant Cloud.

**FAISS (Awareness)**

Facebook AI Similarity Search (FAISS) is a library, not a database. It provides extremely fast in-memory vector similarity search but has no persistence, no metadata filtering, and no server mode out of the box. Use FAISS when: you need raw speed for batch operations, you are building a custom pipeline, or you want to benchmark index strategies. In production, FAISS is often embedded inside a larger system rather than used directly.

**Indexing Strategies: HNSW vs IVF**

Vector search at scale requires approximate nearest neighbor (ANN) indexes. Brute-force exact search is O(n) per query — too slow for millions of vectors.

**HNSW (Hierarchical Navigable Small World):** Builds a multi-layer graph where each node connects to its approximate nearest neighbors. Search traverses the graph from coarse to fine layers. Excellent accuracy-speed tradeoff. This is the default and recommended index for most use cases.

- `m` parameter: number of connections per node (higher = better recall, more memory, 16-64 typical)
- `ef_construction`: search width during index building (higher = better index quality, slower build, 100-400 typical)
- `ef_search`: search width at query time (higher = better recall, slower query, 50-200 typical)

Trade-offs: High memory usage (stores the graph in RAM). Slow to build initially. But query performance is excellent and predictable.

**IVF (Inverted File Index):** Clusters vectors into partitions using k-means, then searches only the nearest partitions. Lower memory than HNSW but typically lower recall at the same speed.

- `nlist`: number of partitions (sqrt(n) is a starting point)
- `nprobe`: number of partitions to search at query time (higher = better recall, slower)

Trade-offs: Lower memory than HNSW. Faster to build. But recall is more sensitive to parameter tuning.

**Production recommendation:** Start with HNSW. Use IVF only if memory is a hard constraint and you have tuned nprobe carefully.

**Distance Metrics**

| Metric | Formula | When to Use |
|--------|---------|-------------|
| Cosine | 1 - (A . B) / (\|A\| \|B\|) | Default for text embeddings. Measures direction, ignores magnitude. |
| Euclidean (L2) | sqrt(sum((a-b)^2)) | When magnitude matters. Less common for text. |
| Dot Product | A . B | Equivalent to cosine when vectors are normalized. Faster to compute. |

For normalized text embeddings, cosine and dot product give identical rankings. Dot product is faster, so if you control normalization, prefer it. If you are unsure whether embeddings are normalized, use cosine (it normalizes for you).

### Interview Questions

**Q1: Compare pgvector and a dedicated vector database like Qdrant. When would you choose each?**

A: Choose pgvector when: (1) Your dataset is under ~10M vectors — pgvector handles this well. (2) You already use PostgreSQL — no new infrastructure. (3) You need joins between vector results and relational data (user permissions, metadata). (4) ACID transactions matter for your write path. (5) Your team knows Postgres but not specialized vector DBs. Choose Qdrant when: (1) Scale exceeds 10M vectors. (2) You need advanced features: quantization, multi-vector search, complex payload filters at scale. (3) You need horizontal scaling across nodes. (4) Search latency at the p99 level is critical. The decision is often pragmatic: start with pgvector (simpler, one less system), migrate to a dedicated vector DB if and when you hit scaling limits. Do not prematurely add infrastructure complexity.

**Q2: Explain HNSW indexing. How do the parameters m and ef_construction affect performance?**

A: HNSW builds a multi-layered graph of nearest-neighbor connections. Each vector is a node; edges connect approximate neighbors. The top layers are sparse (few nodes, long-range connections for coarse navigation), the bottom layer is dense (all nodes, short-range connections for fine search). Query traversal starts at the top, greedily follows edges to the nearest neighbor, then descends to the next layer for finer search. `m` is the max connections per node. Higher m = better recall (more paths to find the true nearest neighbor) but more memory (each connection is stored). Typical range: 16-48. `ef_construction` is how many candidates the algorithm considers when building the index. Higher = better quality graph (more accurate connections) but slower build time. Typical: 100-400. At query time, `ef_search` controls search thoroughness — higher values find better results but slower. The key insight: HNSW gives you knobs to trade memory and build time for recall and query speed, making it tunable to your specific requirements.

**Q3: You are building a search system. The team debates between cosine similarity and Euclidean distance. What do you recommend and why?**

A: For text embeddings, recommend cosine similarity. Reasoning: (1) Text embedding models are designed to encode semantic meaning into the direction of the vector, not its magnitude. Two documents about the same topic will point in similar directions regardless of length. (2) Cosine similarity is invariant to vector magnitude, so it works correctly even if embeddings are not normalized. (3) Euclidean distance is affected by magnitude — two vectors pointing in the same direction but with different magnitudes will have a large Euclidean distance, which is misleading for semantic similarity. (4) However, if you normalize all embeddings to unit length, cosine and Euclidean distance produce equivalent rankings (mathematical fact), so the choice does not matter. In practice: normalize your embeddings, use dot product distance (fastest), and you get equivalent results to cosine with lower computational cost.

**Q4: How would you handle schema migrations when your embedding model changes (e.g., upgrading from text-embedding-ada-002 to text-embedding-3-small)?**

A: This is a significant operational challenge. The new model produces embeddings in a different vector space — you cannot mix old and new embeddings. Strategy: (1) **Add a new column** or new collection for the new embeddings. Do not overwrite the old ones yet. (2) **Re-embed the entire corpus** with the new model. For large datasets, run this as a background job over hours/days. (3) **Run both in parallel** — query both vector spaces and compare results to validate that the new model is equal or better. (4) **Switch over** — update the query path to use the new embeddings. Keep the old column temporarily. (5) **Clean up** — drop the old column after a confidence period. Also: store the model name/version as metadata with each embedding. Track which model version produced each vector. Include "re-embed" as a documented operational runbook in your system.

---

## Lesson 4.3 — Semantic Search Architecture

### Sub-topics
- Document ingestion pipeline
- Chunking strategies (fixed-size, overlap, recursive)
- Metadata filtering
- Hybrid search (vector + keyword/BM25)
- Search quality measurement

### Key Concepts

**Document Ingestion Pipeline**

A semantic search system has two pipelines: ingestion (offline, batch) and query (online, real-time).

Ingestion pipeline:
1. **Source** — Load documents from files, databases, APIs, web scraping
2. **Extract** — Convert to plain text (PDF extraction, HTML parsing, OCR)
3. **Clean** — Remove boilerplate, normalize whitespace, handle encoding
4. **Chunk** — Split into search-sized units (see below)
5. **Enrich** — Add metadata (source, date, author, document type, section headers)
6. **Embed** — Generate vector embeddings for each chunk
7. **Store** — Insert chunks + embeddings + metadata into the vector database
8. **Index** — Build or update the ANN index

```python
# Simplified ingestion pipeline
async def ingest_documents(documents: list[Document]):
    for doc in documents:
        text = extract_text(doc)           # Step 2
        cleaned = clean_text(text)          # Step 3
        chunks = chunk_text(cleaned)        # Step 4
        
        for i, chunk in enumerate(chunks):
            metadata = {
                "source": doc.source,
                "doc_id": doc.id,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            embedding = await embed(chunk)  # Step 6
            await vector_db.upsert(         # Step 7
                id=f"{doc.id}_chunk_{i}",
                embedding=embedding,
                content=chunk,
                metadata=metadata
            )
```

**Chunking Strategies**

Chunking is one of the most impactful decisions in a retrieval system. The goal: create chunks that are (a) self-contained enough to be meaningful, (b) small enough for precise retrieval, (c) large enough to contain useful context.

**Fixed-size chunking:** Split every N tokens/characters. Simple but crude — splits mid-sentence, mid-paragraph.

```python
def fixed_size_chunk(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
```

**Overlap chunking:** Same as fixed-size but chunks overlap by N tokens. This prevents information loss at boundaries. Typical overlap: 10-20% of chunk size.

**Recursive chunking:** Split on natural boundaries in priority order: double newlines (paragraphs) -> single newlines -> sentences -> words. If a paragraph is too large, split it on sentences. If a sentence is too large (rare), split on words. This preserves semantic coherence.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]  # priority order
)
chunks = splitter.split_text(document_text)
```

**Semantic chunking:** Use the embedding model itself to detect topic boundaries. Embed each sentence, compute similarity between adjacent sentences, and split where similarity drops below a threshold. Most sophisticated but also most compute-intensive.

**Practical recommendation:** Start with recursive chunking at 400-600 tokens with 10-15% overlap. This works well for most document types. Benchmark against your actual queries and adjust.

**Metadata Filtering**

Metadata filtering narrows the search space before vector similarity, dramatically improving relevance and speed.

```python
# ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10,
    where={
        "$and": [
            {"source": {"$eq": "product_docs"}},
            {"date": {"$gte": "2024-01-01"}}
        ]
    }
)

# pgvector (SQL)
SELECT content, 1 - (embedding <=> query_embedding) AS score
FROM documents
WHERE metadata->>'source' = 'product_docs'
  AND (metadata->>'date')::date >= '2024-01-01'
ORDER BY embedding <=> query_embedding
LIMIT 10;
```

Essential metadata fields: source/origin, document type, date/version, access control (who can see this), section/chapter, language. Design your metadata schema upfront — changing it later requires re-ingestion.

**Hybrid Search (Vector + Keyword/BM25)**

Pure vector search misses exact keyword matches (product names, error codes, acronyms). Pure keyword search misses semantic meaning. Hybrid search combines both and is the production standard.

BM25 (Best Matching 25) is the classic keyword search algorithm. It ranks documents by term frequency and inverse document frequency — essentially, "how often does this word appear here, weighted by how rare it is across all documents."

```python
# Hybrid search pattern (pseudocode)
def hybrid_search(query: str, top_k: int = 10, alpha: float = 0.7):
    # Vector search
    vector_results = vector_db.search(embed(query), top_k=top_k * 2)
    
    # Keyword search (BM25)
    keyword_results = bm25_index.search(query, top_k=top_k * 2)
    
    # Combine scores with Reciprocal Rank Fusion (RRF)
    combined = reciprocal_rank_fusion(
        vector_results, 
        keyword_results,
        alpha=alpha  # 0.7 = 70% weight on vector, 30% on keyword
    )
    
    return combined[:top_k]

def reciprocal_rank_fusion(results_a, results_b, alpha=0.7, k=60):
    """RRF is a simple, effective way to merge ranked lists."""
    scores = {}
    for rank, doc in enumerate(results_a):
        scores[doc.id] = scores.get(doc.id, 0) + alpha / (k + rank + 1)
    for rank, doc in enumerate(results_b):
        scores[doc.id] = scores.get(doc.id, 0) + (1 - alpha) / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

pgvector + PostgreSQL full-text search gives you hybrid search in a single database — no extra infrastructure.

```sql
-- Hybrid: vector similarity + full-text search
SELECT id, content,
    (1 - (embedding <=> query_embedding)) * 0.7 +
    ts_rank(to_tsvector('english', content), plainto_tsquery('english', 'search terms')) * 0.3
    AS combined_score
FROM documents
ORDER BY combined_score DESC
LIMIT 10;
```

**Search Quality Measurement**

You cannot improve what you do not measure. Essential retrieval metrics:

- **Precision@k**: Of the top k results, what fraction is relevant? High precision = no garbage in the results.
- **Recall@k**: Of all relevant documents, what fraction appears in the top k? High recall = you are not missing important results.
- **MRR (Mean Reciprocal Rank)**: Average of 1/rank of the first relevant result. High MRR = the best result appears near the top.
- **NDCG (Normalized Discounted Cumulative Gain)**: Measures ranking quality — are the most relevant results ranked highest?

```python
def precision_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    top_k = retrieved_ids[:k]
    relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return relevant_in_top_k / k

def recall_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    top_k = retrieved_ids[:k]
    relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant_ids)
    return relevant_in_top_k / len(relevant_ids) if relevant_ids else 0.0

def mrr(retrieved_ids: list, relevant_ids: set) -> float:
    for rank, doc_id in enumerate(retrieved_ids, 1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0
```

To measure, you need a golden dataset: a set of queries with labeled relevant documents. Build this manually for your domain (even 50-100 query-relevance pairs is enough to start). Run your search pipeline on these queries and compute metrics. This is your retrieval eval — it tells you whether changes to chunking, embedding model, or search strategy actually improve results.

### Interview Questions

**Q1: Compare fixed-size chunking, recursive chunking, and semantic chunking. When would you use each?**

A: Fixed-size is simplest — split every N tokens. Use it when document structure is uniform (e.g., all plain text, no sections). It is fast but splits mid-thought, losing context at boundaries. Recursive chunking splits on natural boundaries (paragraphs, sentences) with a size limit. Use it as the default for most document types — it preserves semantic coherence while controlling chunk size. Semantic chunking uses embedding similarity to detect topic changes and splits at topic boundaries. Use it when documents cover multiple distinct topics in flowing text (e.g., meeting transcripts, long articles). The tradeoff: semantic chunking requires embedding every sentence during ingestion (expensive) but produces the most coherent chunks. In practice, recursive chunking with 10-15% overlap is the right starting point for 90% of use cases. Only invest in semantic chunking if retrieval quality metrics show that chunk boundary issues are your bottleneck.

**Q2: Design a hybrid search system. How do you determine the weight between vector and keyword search?**

A: Architecture: run vector search and BM25 keyword search in parallel, merge results using Reciprocal Rank Fusion (RRF) or a weighted linear combination. For the weight (alpha): start with 0.7 vector / 0.3 keyword as a baseline. Then tune empirically using your golden eval set. Queries with specific identifiers (error codes, product SKUs) benefit from higher keyword weight. Queries expressing intent or meaning ("how do I fix the login issue") benefit from higher vector weight. Advanced: use a lightweight classifier to detect query type and dynamically adjust alpha per query. Some systems learn the optimal weights from user click data. The key insight: hybrid consistently outperforms either approach alone because the failure modes are complementary — vector search misses exact matches, keyword search misses semantics.

**Q3: How do you evaluate retrieval quality, and how does retrieval quality affect the overall RAG system?**

A: Evaluate with a golden dataset of query-relevance pairs. Compute precision@k (are results relevant?), recall@k (are we finding all relevant docs?), and MRR (is the best result ranked first?). Retrieval quality is the ceiling for RAG quality — if the right documents are not retrieved, the LLM cannot produce a good answer regardless of how good the prompt is. This is why "garbage in, garbage out" is the first law of RAG. A common mistake: teams focus on improving the generation prompt when the real problem is retrieval. Always measure retrieval separately from generation. If precision@5 is below 0.7, fix retrieval before touching the prompt. Retrieval improvements (better chunking, hybrid search, re-ranking) typically have 3-5x more impact on overall system quality than prompt improvements.

**Q4: Your semantic search returns relevant documents but they are ranked poorly (relevant result at position 8 instead of 1). How do you improve ranking?**

A: Several approaches, in order of implementation ease: (1) **Adjust embedding model** — a higher-quality model (e.g., text-embedding-3-large vs small) may produce better similarity scores. (2) **Add a re-ranker** — retrieve top-20 with vector search, then re-rank with a cross-encoder model (e.g., Cohere Rerank, cross-encoder/ms-marco-MiniLM). Cross-encoders attend to both query and document simultaneously, producing much better relevance scores than bi-encoder similarity. This is the highest-impact improvement for ranking. (3) **Hybrid search** — add BM25 keyword matching to boost exact-match documents. (4) **Query expansion** — use the LLM to generate multiple query variations and merge results. (5) **Metadata boosting** — boost recent documents, authoritative sources, or documents matching user context. (6) **Fine-tune embeddings** — if you have enough labeled data, fine-tune the embedding model on your domain. This is the nuclear option — high effort, high reward.

---

## Lesson 4.4 — Capstone P1 Planning

### Sub-topics
- Project scoping
- Architecture decisions
- Tech stack selection (Python + FastAPI + pgvector + React)
- DECISIONS.md writing
- Deployment planning

### Key Concepts

**Project Scoping**

Your Capstone P1 is a semantic search engine for a real dataset. The goal is not to build a toy demo but to build something that demonstrates production thinking: proper architecture, measured retrieval quality, deployment, and documented decisions.

Scope constraints for a 1-week timeline:
- Pick a focused domain (technical docs, legal documents, product catalog, academic papers)
- Aim for 1K-10K documents (enough to be meaningful, small enough to iterate fast)
- One main search interface with metadata filtering
- Measured retrieval quality (even a small eval set)
- Deployed and accessible via URL

Example projects:
- Technical documentation search (ingest docs from a framework/library)
- Job posting semantic search (scrape job boards, enable meaning-based search)
- Research paper finder (arxiv papers in your domain)
- Codebase search (embed and search code + documentation)

**Architecture Decisions**

Document every significant decision in your DECISIONS.md. The format:

```markdown
## Decision: [Title]
**Date:** YYYY-MM-DD
**Status:** Accepted

### Context
What situation prompted this decision?

### Options Considered
1. Option A — pros and cons
2. Option B — pros and cons
3. Option C — pros and cons

### Decision
Which option and why.

### Consequences
What are the tradeoffs? What did you give up?
```

Example decision entries for this project:

**Decision: pgvector over ChromaDB for storage**
Context: Need persistent vector storage with metadata filtering.
Options: (1) ChromaDB — simple, in-process, good for prototyping. (2) pgvector — production-grade, combines vector + relational in one DB, supports hybrid search with full-text. (3) Qdrant — purpose-built, best performance at scale.
Decision: pgvector. The dataset is <50K vectors so a dedicated vector DB is overkill. pgvector gives us SQL joins for metadata, full-text search for hybrid, and production deployment with standard Postgres hosting. Kamran already knows Postgres, which reduces ramp-up time.
Consequence: Limited to ~10M vectors before needing to migrate. Acceptable for P1 scope.

**Decision: text-embedding-3-small at 512 dimensions**
Context: Need to choose embedding model and dimensions.
Decision: OpenAI text-embedding-3-small at 512 dims. Benchmarked against 1536 dims on 100 sample queries — recall@10 dropped from 0.92 to 0.89, but cost and storage are 3x lower. For this project, the tradeoff is worth it.

**Tech Stack Selection**

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python | AI/ML ecosystem lives here; FastAPI is excellent for APIs |
| API Framework | FastAPI | Async, typed, auto-docs, production-ready |
| Vector Storage | pgvector (PostgreSQL) | Combines vector + relational, known technology |
| Embedding Model | text-embedding-3-small (512d) | Cost-effective, good quality for the domain |
| Frontend | React | Kamran's strength — leverage existing skill |
| Deployment | Railway / Render / Fly.io | Free tier available, Postgres included |

**Deployment Planning**

Deployment proves the system works outside your laptop. Plan for:

1. **Database hosting**: Use a managed Postgres service with pgvector support (Supabase, Neon, Railway, or Render all offer this on free tiers).
2. **API hosting**: Deploy the FastAPI backend as a containerized service. Dockerfile:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Frontend hosting**: Deploy React app to Vercel (free, Kamran already knows this).
4. **Environment variables**: API keys for OpenAI (embedding), database URL, CORS origins.
5. **Ingestion**: Run the embedding pipeline once as a script, or build a simple admin endpoint.

The deployment does not need to handle thousands of users. It needs to be accessible via a URL, return results in under 2 seconds, and not crash. That is the bar for P1.

### Hands-on

- [Semantic Search Engine (Capstone P1)](./assignments/w04-a1-semantic-search-engine.md)
- [Capstone P1 Deployment](./assignments/w04-a2-capstone-p1-deployment.md)

---

## Week 4 Summary

### What You Should Know Now
- How to generate embeddings with both commercial (OpenAI) and open-source (sentence-transformers) models
- The embedding dimensions vs quality tradeoff and how to benchmark it
- How to store and query vectors in ChromaDB (dev) and pgvector (production)
- HNSW vs IVF indexing and when to use each
- The full document ingestion pipeline: extract, clean, chunk, embed, store
- Chunking strategies and their impact on retrieval quality
- Hybrid search (vector + BM25) and why it outperforms either alone
- How to measure retrieval quality with precision, recall, and MRR
- How to scope, architect, and deploy a real project with documented decisions

### Checklist
- [ ] Generated embeddings with OpenAI API (text-embedding-3-small)
- [ ] Generated embeddings with sentence-transformers (local model)
- [ ] Benchmarked different dimension sizes on sample queries
- [ ] Stored and queried vectors in ChromaDB
- [ ] Set up pgvector in PostgreSQL and ran similarity queries
- [ ] Implemented recursive text chunking with overlap
- [ ] Built a document ingestion pipeline (extract -> chunk -> embed -> store)
- [ ] Implemented hybrid search (vector + keyword)
- [ ] Measured retrieval quality (precision@k, recall@k, MRR)
- [ ] Scoped Capstone P1 and wrote DECISIONS.md
- [ ] Deployed Capstone P1 (accessible via URL)
- [ ] Completed the Semantic Search Engine assignment
- [ ] Completed the Capstone P1 Deployment assignment
- [ ] System design study: continued (1 teardown this week)
- [ ] Blog post or tradeoff entry written

### Tradeoff Logged This Week
> "I chose ___ over ___ because ___; the cost was ___."

### Month 1 Complete
You now have: (1) a mental model of how LLMs work, (2) practical SDK skills across three providers, (3) prompt engineering mastery, (4) a working semantic search system, and (5) a deployed capstone project with documented decisions. You are ready for Month 2: RAG Architecture, Evals, and Observability.

---

Back to [Roadmap](../ROADMAP.md) | Next: Month 2, Week 5 — RAG Architecture Deep Dive
