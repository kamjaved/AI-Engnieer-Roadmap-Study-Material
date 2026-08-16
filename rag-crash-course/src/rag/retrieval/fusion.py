# src/rag/retrieval/fusion.py

from collections import defaultdict

from langchain_core.documents import Document


def reciprocal_rank_fusion(ranked_lists: list[list[Document]], k: int = 60) -> list[Document]:
    # defaultdict(float) means a chunk_id we haven't seen yet starts at
    # 0.0 automatically — no KeyError, no manual "if not in dict" check.
    scores: dict[str, float] = defaultdict(float)
    doc_lookup: dict[str, Document] = {}

    for ranked_list in ranked_lists:
        # enumerate(..., start=1): rank 1 is the BEST result in this
        # list, not index 0. RRF's formula is defined in terms of rank
        # (1st, 2nd, 3rd...), so this off-by-one matters.
        for rank, doc in enumerate(ranked_list, start=1):
            chunk_id = doc.metadata[
                "chunk_id"
            ]  # the deterministic ID from Lesson 3 — same one used everywhere else

            # THE WHOLE FORMULA. A chunk ranked #1 contributes more than
            # one ranked #10 (rank is in the denominator), but the gap
            # between adjacent ranks shrinks fast — going from #1 to #2
            # matters a lot more than going from #50 to #51.
            scores[chunk_id] += 1 / (k + rank)

            # Keep a way to get back from chunk_id -> the actual Document,
            # same reasoning as sparse_retriever's chunks list — the score
            # dict only ever deals in IDs, not real objects.
            doc_lookup[chunk_id] = doc

    # Sort chunk_ids by their FUSED score, highest first.
    fused_ids = sorted(scores, key=lambda cid: scores[cid], reverse=True)
    return [doc_lookup[cid] for cid in fused_ids]


# A worked example, so the formula isn't just symbols

# Say k=60, and you're fusing one dense list and one sparse list:

# Chunk A ranks #1 in dense, doesn't appear in sparse's top-10 at all.
# Score = 1/(60+1) = 0.0164
# Chunk B ranks #5 in dense AND #1 in sparse.
# Score = 1/(60+5) + 1/(60+1) = 0.0154 + 0.0164 = 0.0318
# Chunk B wins — despite never being the #1 result in either individual list.
