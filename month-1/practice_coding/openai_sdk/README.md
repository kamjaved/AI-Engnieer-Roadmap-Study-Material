openai_service/
├── main.py                    # FastAPI app entry + router registration
├── config.py                  # Pydantic Settings (API keys, model config)
├── dependencies.py            # Shared FastAPI dependencies (OpenAI client)
│
├── routers/
│   ├── chat.py               # Topic 1: Chat Completions endpoint
│   ├── responses.py          # Topic 2: Responses API endpoint
│   ├── streaming.py          # Topic 3: SSE Streaming endpoint
│   ├── tools.py              # Topic 4: Tool Calling endpoint
│   ├── structured.py         # Topic 5: Structured Outputs endpoint
│   └── tokens.py             # Topic 7: Token Counting endpoint
│
├── schemas/
│   ├── chat.py               # Pydantic request/response models (Topic 1)
│   ├── tools.py              # Tool schemas (Topic 4)
│   └── structured.py         # Structured output schemas (Topic 5)
│
└── services/
    ├── chat_service.py       # Core OpenAI logic for chat
    ├── tool_service.py       # Tool execution logic
    └── token_service.py      # Token counting logic


### Forward References (Python + Pydantic v2)

* **Normal:** Define referenced models first whenever possible. This is the simplest and preferred production approach.
* **Quoted annotation:** `field: "User"` delays type resolution until later. Useful when the referenced class is defined below or for circular references.
* **`from __future__ import annotations`:** Automatically treats **all** type annotations as forward references (strings), so you can write `field: User` even if `User` is defined later. Recommended for modern Python projects.
* **`model_rebuild()`:** Forces Pydantic to resolve unresolved forward references. Usually only needed for complex or circular models; avoid it when proper model ordering is possible.
