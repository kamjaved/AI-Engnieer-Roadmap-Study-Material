"""Preview script: loads seed documents, chunks them, and reports counts.

Lives at the project root, not under src/rag/ -- this is a one-off
developer entry point (a script a human runs), not reusable library
code that anything else imports. Keeping "library" (src/rag/) and
"entry point" (this file) separate matters once this project gets
packaged for real deployment later.
"""

from __future__ import annotations

from collections import defaultdict

from pinecone import Pinecone

from rag.config import settings
from rag.indexing.embed_and_index import get_or_create_index, index_chunks
from rag.ingestion.chunker import chunk_documents
from rag.ingestion.loader import load_documents


def main() -> None:
    docs = load_documents()
    chunks = chunk_documents(docs)

    # ------LEGACY CODE FROM LESSON 3 REPLACED BY ACTUAL PINECONE IN LESSON 5-------
    # print(f"Loaded {len(docs)} document(s) -> {len(chunks)} chunk(s) total\n")

    # # "Longest document" = the ORIGINAL source with the most total
    # # characters BEFORE chunking. Sum across ALL Documents sharing a
    # # source -- required because a PDF is spread across multiple
    # # page-Documents that all share the same source filename.
    # chars_by_source: dict[str, int] = defaultdict(int)
    # for doc in docs:
    #     chars_by_source[doc.metadata["source"]] += len(doc.page_content)

    # longest_source = max(chars_by_source, key=chars_by_source.get)
    # longest_chunks = [c for c in chunks if c.metadata["source"] == longest_source]

    # print(f"Longest document: {longest_source} ({chars_by_source[longest_source]} chars)")
    # print(f"  -> produced {len(longest_chunks)} chunk(s)")
    # for chunk in longest_chunks:
    #     # Printing chunk_id (not just an index) because that's the
    #     # actual identifier you'll rely on from Lesson 5 onward --
    #     # good habit to start reading it now, not just the length.
    #     print(f"     {chunk.metadata['chunk_id']}: {len(chunk.page_content)} chars")

    # -----------NEW CODE LESSON 5-----------
    # ONE Pinecone client, built once, reused for both steps below —
    # matches 5.2's dependency-injection design (get_or_create_index
    # takes pc as a parameter instead of building its own client).
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    get_or_create_index(pc)  # idempotent — safe to call on every run
    index_chunks(chunks)  # embeds + upserts, deterministic ids

    # describe_index_stats() asks Pinecone directly, not Python's own
    # memory — this is the real, server-side source of truth for what
    # actually landed in the index. This is what 5.5/5.6's Done-When
    # checks will read.
    stats = pc.Index(settings.PINECONE_INDEX_NAME).describe_index_stats()
    print(f"Ingested {len(chunks)} chunks.")
    print(
        f"Index '{settings.PINECONE_INDEX_NAME}' now reports {stats.total_vector_count} vectors."
    )


if __name__ == "__main__":
    main()
