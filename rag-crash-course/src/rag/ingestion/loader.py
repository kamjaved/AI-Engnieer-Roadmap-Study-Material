"""Loads seed documents and attaches per-file metadata.

Lesson 3 fills in load_documents() itself — for now this file only
stubs the metadata lookup table that load_documents() will use.
Lesson 2.5 adds two more entries here (the PDFs) once you reach it.
"""

from __future__ import annotations

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
    # Lesson 2.5 adds two more entries here once the PDFs are ready —
    # not added yet, since PyPDFLoader dispatch logic doesn't exist
    # until that lesson:
    #   "corporate_gifts_price_list.pdf": {"team": "sales", "doc_type": "catalog"},
    #   "company_overview.pdf": {"team": "leadership", "doc_type": "guide"},
}
