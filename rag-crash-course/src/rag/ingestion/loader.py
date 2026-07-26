"""Loads seed documents and attaches per-file metadata.

Lesson 3 fills in load_documents() itself — for now this file only
stubs the metadata lookup table that load_documents() will use.
"""

from __future__ import annotations

# Centralized filename -> metadata lookup. Two keys only, matching
# exactly what Lesson 6's metadata filtering needs: `team` says who
# owns a doc, `doc_type` says what KIND of doc it is (a runbook you
# follow live during an incident reads very differently from a policy
# doc you reference occasionally).
DOC_METADATA: dict[str, dict[str, str]] = {
    "deploy.md": {"team": "platform", "doc_type": "runbook"},
    "auth.md": {"team": "security", "doc_type": "policy"},
    "rate_limits.md": {"team": "platform", "doc_type": "policy"},
    "on_call.md": {"team": "platform", "doc_type": "runbook"},
    "migrations.md": {"team": "data", "doc_type": "runbook"},
    "incident_response.md": {"team": "security", "doc_type": "runbook"},
}
