"""Loads seed documents (markdown + PDF) and attaches per-file metadata."""

from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# Centralized filename -> metadata lookup. Two keys only, matching
# exactly what Lesson 6's metadata filtering needs: `team` says who
# owns a doc, `doc_type` says what KIND of doc it is (an HR policy you
# reference occasionally reads very differently from the sales team's
# product catalog).
DOC_METADATA: dict[str, dict[str, str]] = {
    "hr_policies.md": {"team": "hr", "doc_type": "policy"},
    "employee_benefits_leave.md": {"team": "hr", "doc_type": "policy"},
    "travel_expense_policy.md": {"team": "finance", "doc_type": "policy"},
    "procurement_guidelines.md": {"team": "operations", "doc_type": "guide"},
    "product_catalog_faq.md": {"team": "sales", "doc_type": "faq"},
    "product_catalog_services_guide.md": {"team": "sales", "doc_type": "guide"},
    # Added ahead of Lesson 2.5 (Kamran had both PDFs ready already) —
    # the DICT entries are correct and ready to use. What's still
    # missing is Lesson 2.5's actual load_documents() dispatch logic
    # (the PyPDFLoader code path) — these two keys just sit unused
    # until that lesson wires up the .pdf branch.
    "corporate_gifts_price_list.pdf": {"team": "sales", "doc_type": "catalog"},
    "company_overview.pdf": {"team": "leadership", "doc_type": "guide"},
}

DATA_DIR = Path("data/docs")


def load_documents() -> list[Document]:
    """One Document per markdown FILE, but one Document per PDF PAGE.
    That asymmetry is real, not a bug -- PyPDFLoader is page-granular
    (see the .pdf branch below), plain text reading is not.
    """
    documents: list[Document] = []

    for filename, metadata in DOC_METADATA.items():
        path = DATA_DIR / filename

        if path.suffix == ".md":
            # Whole markdown file -> ONE Document. No page/section
            # structure to preserve here -- Lesson 3's chunker is what
            # splits this up later, not this function.
            documents.append(
                Document(
                    page_content=path.read_text(encoding="utf-8"),
                    metadata={"source": filename, **metadata},
                )
            )

        elif path.suffix == ".pdf":
            # PyPDFLoader returns ONE Document PER PAGE. Every page of
            # the SAME pdf needs the SAME team/doc_type (it's the same
            # source doc) -- but PyPDFLoader already stamped its own
            # "page" key onto each Document's metadata, so we .update()
            # rather than overwrite, or we'd lose that page number.
            pages = PyPDFLoader(str(path)).load()
            for page in pages:
                page.metadata.update({"source": filename, **metadata})
            documents.extend(pages)

        else:
            raise ValueError(f"No loader configured for: {filename}")

    return documents


if __name__ == "__main__":
    # Quick, throwaway verification script -- not part of the real
    # pipeline. Lesson 3 will build a proper ingest preview once
    # chunking exists; this only needs to prove the PDF branch works
    # before we move on, per this lesson's own Done-When check.
    docs = load_documents()

    for filename in ("corporate_gifts_price_list.pdf", "company_overview.pdf"):
        # Filter down to just this PDF's pages -- load_documents()
        # returns ONE Document per page, remember, so a 3-page PDF
        # shows up here as 3 separate entries in `docs`, all sharing
        # the same "source" value.
        pages = [d for d in docs if d.metadata["source"] == filename]
        print(f"{filename}: {len(pages)} page(s)")
        print(f"  first page metadata keys: {list(pages[0].metadata.keys())}")
