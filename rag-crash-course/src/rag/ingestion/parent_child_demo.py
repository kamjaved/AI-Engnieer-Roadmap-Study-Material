"""Standalone demo: parent-child chunking vs plain recursive chunking.

NOT wired into the real indexing pipeline -- chunker.py (Lesson 3.1)
stays as the production path. This file exists purely to make the
tradeoff visible before Lesson 5 decides whether the extra storage
layer parent-child requires is worth adopting for real.

Matching here is plain substring search, not real vector search --
embeddings don't exist until Lesson 4. The point is structural: which
chunk BOUNDARIES contain the search term, not how retrieval ranks
results.
"""

from __future__ import annotations

import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.ingestion.chunker import chunk_documents
from rag.ingestion.loader import load_documents

# Parent chunks: big enough to hold a whole table section -- its
# heading, its column headers, several rows -- so whatever gets handed
# to the LLM has enough surrounding context to be self-explanatory.
_parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# Child chunks: small and narrow on purpose -- close to "one price-list
# line" scale. Small chunks make sharp, specific search targets; the
# linked parent is what supplies context, not the child itself.
_child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=180,
    chunk_overlap=20,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def build_parent_child(docs: list[Document]) -> tuple[list[Document], list[Document]]:
    """Build two linked layers: parent chunks and child chunks.

    Every child's metadata carries parent_id, pointing back to the
    exact parent it was cut from -- the link that lets you search on
    the small, precise child, then hand the LLM the bigger parent.
    """
    parents: list[Document] = []
    children: list[Document] = []

    # Group by source first -- same reason as chunk_documents() in
    # 3.1: parent/child IDs restart per source file instead of running
    # as one long counter across the whole corpus.
    docs_by_source: dict[str, list[Document]] = {}
    for doc in docs:
        docs_by_source.setdefault(doc.metadata["source"], []).append(doc)

    for source, source_docs in docs_by_source.items():
        source_parents = _parent_splitter.split_documents(source_docs)

        for p_index, parent in enumerate(source_parents):
            parent_id = f"{source}::parent::{p_index}"
            parent.metadata["parent_id"] = parent_id
            parents.append(parent)

            # Split THIS parent's own text further into children --
            # every child's boundaries sit inside a single parent,
            # never spanning two parents.
            source_children = _child_splitter.split_documents([parent])
            for c_index, child in enumerate(source_children):
                child.metadata["parent_id"] = parent_id
                child.metadata["chunk_id"] = f"{source}::child::{p_index}.{c_index}"
                children.append(child)

    return parents, children


def _normalize(text: str) -> str:
    """Lowercase + strip ALL whitespace (not just collapse repeats).

    PyPDFLoader's text extraction can plant a stray space mid-word
    where the PDF used custom letter-spacing/kerning -- confirmed on
    THIS exact file: "Steel Water Bottle" extracts as "Steel W ater
    Bottle". Collapsing repeated whitespace wouldn't fix a single
    misplaced space, so both sides of the comparison get ALL
    whitespace stripped instead, sidestepping the artifact entirely.
    """
    return re.sub(r"\s+", "", text.lower())


def compare(term: str, docs: list[Document]) -> None:
    """Print, side by side, what plain recursive chunking returns for
    `term` vs what parent-child chunking returns for the same term.
    """
    normalized_term = _normalize(term)

    # Path 1: plain recursive chunking (chunker.py, Lesson 3.1) --
    # exactly what's live in the real pipeline today.
    recursive_chunks = chunk_documents(docs)
    recursive_hits = [
        c for c in recursive_chunks if normalized_term in _normalize(c.page_content)
    ]

    # Path 2: parent-child -- find matching CHILDREN, then look up
    # each match's PARENT for the context comparison.
    parents, children = build_parent_child(docs)
    parents_by_id = {p.metadata["parent_id"]: p for p in parents}
    child_hits = [c for c in children if normalized_term in _normalize(c.page_content)]

    print(f'Searching for: "{term}"\n')

    print(f"=== Plain recursive chunking: {len(recursive_hits)} match(es) ===")
    for chunk in recursive_hits:
        print(f"[{chunk.metadata['chunk_id']}] ({len(chunk.page_content)} chars)")
        print(chunk.page_content)
        print()

    print(f"=== Parent-child chunking: {len(child_hits)} child match(es) ===")
    for child in child_hits:
        parent = parents_by_id[child.metadata["parent_id"]]
        print(f"CHILD [{child.metadata['chunk_id']}] ({len(child.page_content)} chars)")
        print(child.page_content)
        print()
        print(
            f"  -> linked PARENT [{parent.metadata['parent_id']}] ({len(parent.page_content)} chars)"
        )
        print(f"  {parent.page_content}")
        print()


if __name__ == "__main__":
    docs = load_documents()
    pdf_docs = [d for d in docs if d.metadata["source"] == "corporate_gifts_price_list.pdf"]
    compare("steel water bottle", pdf_docs)
