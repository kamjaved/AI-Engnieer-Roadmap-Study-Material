from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from rag.config import settings
from rag.generation.prompt import prompt
from rag.retrieval.retriever import retrieve


def format_docs(scored_docs: list[tuple[Document, float]]) -> str:
    """
    Turns retrieve()'s raw output into the single string that fills
    the {context} placeholder in prompt.py's human message.

    Input shape matches retrieve()'s return type EXACTLY —
    list[tuple[Document, float]] — so this can be called directly on
    retrieve()'s output with no reshaping step in between.
    """
    return "\n\n".join(
        # i + 1, not i: numbering starts at 1 because that's what
        # SYSTEM_PROMPT's "cite sources inline like [1], [2]" promised
        # the model. Starting at 0 would silently break that contract.
        f"[{i + 1}] (source: {doc.metadata['source']})\n{doc.page_content}"
        for i, (doc, _score) in enumerate(scored_docs)
    )


_llm = ChatOpenAI(model=settings.CHAT_MODEL, temperature=0)

# The actual LCEL chain (LangChain Expression Language). Built once, reused across every call below.
generation_chain = prompt | _llm | StrOutputParser()


def answer_question(
    vector_store: PineconeVectorStore,
    question: str,
    k: int = 5,
    team: str | None = None,
    doc_type: str | None = None,
) -> dict:
    """
    Full read path: retrieve -> format -> generate.
    """
    # Plain reuse of Lesson 6's retrieve() — no new retrieval logic
    # written here. This function only orchestrates + generates.

    scored_docs = retrieve(vector_store, question, k=k, team=team, doc_type=doc_type)
    context = format_docs(scored_docs)

    # The dict keys here MUST match the prompt template's
    # input_variables exactly — {"context", "question"}, confirmed
    # back in 7.1. Get a key name wrong and this raises a KeyError,
    # not a silently wrong answer — fail loud, not quiet.
    answer = generation_chain.invoke({"context": context, "question": question})

    # Only report sources the model actually CITED, not every source
    # that was merely RETRIEVED. format_docs() numbered chunks
    cited_sources = [
        doc.metadata["source"]
        for i, (doc, _score) in enumerate(scored_docs)
        if f"[{i + 1}]" in answer
    ]

    return {
        "answer": answer,
        # dict.fromkeys() dedups while preserving first-seen order —
        # unlike set(), which would shuffle the source list.
        "sources": list(dict.fromkeys(cited_sources)),
        # Raw chunks returned alongside the answer, not just the
        # final string — the full reasoning for this is 7.6's concept
        # check, but in short: you can't debug a wrong answer without
        # knowing exactly what it was grounded in.
        "raw_chunks": scored_docs,
    }


# src/rag/generation/chain.py (append below answer_question)

if __name__ == "__main__":
    from rag.retrieval.retriever import get_vector_store

    vector_store = get_vector_store()

    demo_questions = [
        # 1. Answerable — should cite hr_policies.md, no refusal.
        "How many earned leave days do I accrue per month?",
        # 2. NOT in the docs — should trigger SYSTEM_PROMPT's refusal
        # sentence, not a fabricated number.
        "What was Turab Industries' revenue last year?",
        # 3. Spans two docs — probation notice period lives in
        # hr_policies.md, health insurance eligibility lives in
        # employee_benefits_leave.md — should cite both.
        "If I'm still on probation, what's my notice period, and do I have health insurance yet?",
    ]

    for question in demo_questions:
        result = answer_question(vector_store, question)
        print(f"Q: {question}")
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 60)
