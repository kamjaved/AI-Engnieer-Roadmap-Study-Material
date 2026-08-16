from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


def _tokenize(text: str) -> list[str]:
    # BM25 works on TOKENS (words), not raw text. A simple lowercase +
    # whitespace split is enough for this corpus's size and keeps the
    # lesson focused on the fusion mechanism, not tokenizer engineering.
    # Production BM25 usually adds punctuation stripping and stemming
    # (so "travels" / "traveling" / "travel" all count as one token) —
    # deliberately skipped here.
    return text.lower().split()


def build_bm25_index(chunks: list[Document]) -> tuple[BM25Okapi, list[Document]]:
    """
    Fits a BM25 index over the given chunks — the "write path" for
    sparse retrieval, same idea as Lesson 5's embed_and_index.py, just
    entirely in-memory instead of upserted to Pinecone.
    """
    tokenized_corpus = [_tokenize(chunk.page_content) for chunk in chunks]

    # This is the "fit" step: BM25Okapi walks the whole tokenized corpus
    # ONCE here and precomputes the corpus-wide stats (word rarity, average
    # chunk length) that every future score() call will reuse.
    bm25_index = BM25Okapi(tokenized_corpus)

    # WHY return chunks too, not just the index: BM25Okapi has no concept
    # of a Document or a chunk_id — it only ever returns scores as a plain
    # list of floats, POSITIONED by index (score[3] belongs to whatever
    # chunk was 4th in tokenized_corpus). This chunks list — kept in the
    # exact same order — is what lets you map a score's position back to
    # a real Document later, in sparse_retrieve().
    return bm25_index, chunks


def sparse_retrieve(
    bm25_index: BM25Okapi,
    chunks: list[Document],
    query: str,
    k: int = 10,
) -> list[Document]:
    """
    Scores every chunk in the corpus against the query using BM25,
    returns the top-k Documents, highest score first.
    """
    # CRITICAL: if the corpus was tokenized one way and the query
    # another, the "word overlap" BM25 is counting stops meaning
    # anything. No crash either way,
    tokenized_query = _tokenize(query)

    scores = bm25_index.get_scores(tokenized_query)

    scored_chunks = list(zip(chunks, scores))
    scored_chunks.sort(key=lambda pair: pair[1], reverse=True)

    return [chunk for chunk, _ in scored_chunks[:k]]
