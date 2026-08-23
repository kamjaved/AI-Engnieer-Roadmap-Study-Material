from langchain_core.prompts import ChatPromptTemplate

# This is the single highest-leverage sentence in the whole RAG
# pipeline for reducing hallucination. It's a SYSTEM message, not
# folded into the human question, because system messages set
# standing behavior for the whole exchange — the model treats them
# as a constraint on how to behave, not just more context to read.
SYSTEM_PROMPT = """You are an internal HR & operations assistant for
Turab Industries employees. Answer ONLY using the numbered sources
below. If the sources don't contain the answer, say "I don't have
that in the knowledge base" instead of guessing. Cite sources inline
like [1], [2]."""


# from_messages() builds a reusable TEMPLATE, not a finished prompt.
# "{context}" and "{question}" are placeholders — nothing fills them
# in until Lesson 7.3 invokes this template with real values. Built
# once at module import time (same pattern retriever.py already uses
# for _hyde_llm) — not rebuilt on every request.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Sources:\n{context}\n\nQuestion: {question}"),
    ]
)
