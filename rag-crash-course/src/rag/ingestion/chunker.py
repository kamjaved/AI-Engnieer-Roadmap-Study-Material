from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

_splitter_ = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=75,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def chunk_documents(docs: list[Document]) -> list[Document]:
    chunks: list[Document] = []

    # Group by source BEFORE splitting, specifically so `index` can
    # restart at 0 for each file instead of being one running counter
    # across the whole corpus.
    docs_by_source: dict[str, list[Document]] = {}
    for doc in docs:
        docs_by_source.setdefault(doc.metadata["source"], []).append(doc)

    for source, source_docs in docs_by_source.items():
        split = _splitter_.split_documents(source_docs)
        for index, chunk in enumerate(split):
            chunk.metadata["chunk_id"] = f"{source}::{index}"
            chunks.append(chunk)
    return chunks
