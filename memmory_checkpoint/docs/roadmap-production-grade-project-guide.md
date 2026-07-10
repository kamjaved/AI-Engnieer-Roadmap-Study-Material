# Project Outcome

By the end, you should be able to demo:

```text
User: When does Ocean Majesty sail next?
Assistant: Ocean Majesty next sails on 2026-08-04 from Rome to Barcelona.

User: Show my booking confirmation.
Assistant: Your booking confirmation is CNF-10021...

User: What sailings are available in August?
Assistant: I found 3 August sailings...

User: Calculate total fare for 2 adults and 1 child.
Assistant: Adult fare..., child fare..., taxes..., total...

```

And explain production concepts:

```text
Messages table = canonical transcript
LangGraph checkpoint = recoverable graph state
Summary = compressed old conversation context
Long-term memory = durable reusable user facts/preferences
Thread ID = conversation continuity key

```

LangGraph’s memory model separates short-term thread-scoped memory persisted by checkpointers from long-term memory stored across sessions.

---

# Recommended Final Stack

```text
Backend:
  FastAPI
  Python 3.13
  Pydantic v2
  SQLAlchemy async ORM
  PostgreSQL local
  Alembic migrations
  uv
  Ruff

Agent:
  LangGraph
  LangChain ChatOpenAI
  LangMem
  OpenAI API key

Frontend:
  React
  Tailwind CSS
  Vite

Database:
  PostgreSQL local
  LangGraph Postgres checkpointer

```

Use **SQLAlchemy async** for your own app tables. Use **LangGraph Postgres checkpointer** for LangGraph state persistence. Do not manually implement LangGraph checkpoint tables unless you are only storing demo metadata. LangGraph checkpointers persist graph state by thread and PostgreSQL is suitable for production-style persistence.

---

# Week 1 — Backend Foundation, Domain Model, and Tool Layer

**Estimated Time:** ~10–12 hours

**Goal:** Build a clean FastAPI + PostgreSQL backend and deterministic cruise domain tools before adding the LLM.

---

## Lesson 1.1: Project Setup and Engineering Baseline 🔴 Essential

### Objective

Create a clean Python backend foundation that feels production-oriented from day one.

### Topics Covered

1. `uv` project setup 🔴
2. Ruff formatting/linting 🔴
3. FastAPI project structure 🔴
4. Pydantic v2 settings 🔴
5. Async SQLAlchemy setup 🔴
6. Local PostgreSQL connection 🔴

### Subtopics

1. `uv` Setup 🔴
    - Create project with `uv`
    - Add FastAPI, Uvicorn, SQLAlchemy, asyncpg, Alembic, Pydantic settings
    - Add LangGraph, LangChain, LangMem later, not immediately

2. Ruff 🔴
    - Configure formatting
    - Use import sorting
    - Keep the codebase clean from the beginning

3. FastAPI Structure 🔴
   Use this structure:

```text
src/
  app/
    main.py
    core/
      config.py
      logging.py
    db/
      session.py
      base.py
    domain/
      models.py
      repositories.py
      services.py
    api/
      routes_health.py
      routes_cruise.py
    agent/
    memory/
    tools/

```

4. Pydantic v2 Settings 🔴
    - Load database URL
    - Load OpenAI API key
    - Load app environment

5. Async SQLAlchemy 🔴
    - `AsyncEngine`
    - `AsyncSession`
    - session dependency
    - repository pattern

---

### What to Build

Build:

```text
GET /health

```

Expected response:

```json
{
	"status": "ok",
	"service": "cruise-ai-agent"
}
```

Also configure:

```text
.env
pyproject.toml
ruff config
database session dependency

```

---

### Key Concepts That Need to Understand During This Lesson

- Difference between app config, database session, and request dependency
- Why async DB sessions should be request-scoped
- Why clean project structure matters before adding LangGraph
- Why you should not mix API, database, and agent logic in one file

---

## Lesson 1.2: Cruise Booking Domain Model 🔴 Essential

### Objective

Create the minimum database schema needed for a realistic travel agent demo.

### Topics Covered

1. Users 🔴
2. Ships 🔴
3. Sailings 🔴
4. Bookings 🔴
5. Conversation threads 🔴
6. Messages 🔴
7. Summaries 🔴
8. Long-term memories 🔴
9. Checkpoint metadata 🟡

### Subtopics

1. `users` 🔴
    - Static seeded users
    - No authentication
    - User ID used for memory and bookings

2. `ships` 🔴
    - Ship name
    - Description
    - Capacity
    - Amenities

3. `sailings` 🔴
    - Ship ID
    - Departure port
    - Arrival port
    - Departure date
    - Return date
    - Adult fare
    - Child fare
    - Currency

4. `bookings` 🔴
    - User ID
    - Sailing ID
    - Confirmation number
    - Adults
    - Children
    - Cabin type
    - Total fare
    - Status

5. `conversation_threads` 🔴
    - Thread ID
    - User ID
    - Title
    - Summary mode: `manual` or `langmem`
    - Created/updated timestamps

6. `messages` 🔴
    - Thread ID
    - Role: `user`, `assistant`, `tool`, `system`
    - Content
    - Metadata
    - Created timestamp

7. `summaries` 🔴
    - Thread ID
    - Summary text
    - Covered until message ID
    - Strategy: `manual` or `langmem`
    - Token/message count metadata

8. `long_term_memories` 🔴
    - User ID
    - Memory type
    - Content
    - Confidence
    - Source thread ID
    - Status

9. `checkpoint_metadata` 🟡
    - Thread ID
    - User ID
    - Latest checkpoint timestamp
    - Used only for your debug/demo UI
    - Actual checkpoints should be handled by LangGraph’s Postgres checkpointer

LangGraph checkpointers store graph state snapshots, including channel values and version tracking, under a `thread_id`.

---

### What to Build

Create SQLAlchemy models and Alembic migrations for:

```text
users
ships
sailings
bookings
conversation_threads
messages
summaries
long_term_memories
checkpoint_metadata

```

Seed:

```text
3 users
3 ships
8-10 sailings
4-6 bookings

```

---

### Key Concepts That Need to Understand During This Lesson

- Difference between business data and agent state
- Why messages are stored separately from checkpoints
- Why summaries need `covered_until_message_id`
- Why long-term memories need source tracking and confidence

---

## Lesson 1.3: Deterministic Cruise Services and Tools 🔴 Essential

### Objective

Build your cruise business logic before adding any LLM.

### Topics Covered

1. Ship details service 🔴
2. Sailing search service 🔴
3. Booking lookup service 🔴
4. Fare calculation service 🔴
5. Pydantic input/output schemas 🔴

### Subtopics

1. Ship Details 🔴
    - Search ship by name
    - Return description, capacity, amenities

2. Sailing Search 🔴
    - Search by ship
    - Search by month
    - Search by destination
    - Search next sailing for a ship

3. Booking Lookup 🔴
    - Find bookings by static user ID
    - Return confirmation number and sailing details

4. Fare Calculation 🔴
    - Adults × adult fare
    - Children × child fare
    - Add taxes
    - Optional discount

5. Pydantic Schemas 🔴
    - Separate request schema from response schema
    - Keep tool input schema strict

---

### What to Build

Build plain service functions first:

```text
get_ship_details()
search_sailings()
get_user_bookings()
calculate_fare()

```

Expose simple test endpoints:

```text
GET /ships
GET /ships/{ship_name}
GET /sailings
GET /users/{user_id}/bookings
POST /fare/calculate

```

---

### Key Concepts That Need to Understand During This Lesson

- LLM tools should wrap reliable deterministic functions
- Business logic should be testable without LangGraph
- Tool inputs should be explicit and typed
- The model does not calculate or query directly; your backend does

---

# Week 2 — LangGraph Agent, Checkpointing, and Manual Memory

**Estimated Time:** ~14–16 hours

**Goal:** Convert your backend into a real AI assistant with tools, thread persistence, checkpoint recovery, message history, and manual summarization.

---

## Lesson 2.1: First LangGraph Cruise Agent 🔴 Essential

### Objective

Build the first working agent that can call your cruise tools.

### Topics Covered

1. LangGraph state 🔴
2. Message state 🔴
3. Tool binding 🔴
4. Agent node 🔴
5. Tool execution node 🔴
6. Chat endpoint 🔴

### Subtopics

1. State Schema 🔴
    - `messages`
    - `user_id`
    - `thread_id`
    - `retrieved_memories`
    - `conversation_summary`

2. Message Reducer 🔴
    - Use append behavior for messages
    - Understand that state evolves per graph run

3. Tool Binding 🔴
    - Wrap cruise services as tools
    - Keep tool descriptions clear
    - Do not create too many tools

4. Agent Node 🔴
    - Model receives context
    - Model decides whether tool call is needed

5. Tool Node 🔴
    - Executes backend function
    - Returns tool result to graph

6. Chat Endpoint 🔴
    - `POST /chat`
    - Takes `user_id`, `thread_id`, `message`

---

### What to Build

Build:

```text
POST /chat

```

Request:

```json
{
	"user_id": "user_001",
	"thread_id": "thread_user_001_demo_001",
	"message": "When does Ocean Majesty sail next?"
}
```

Response:

```json
{
	"thread_id": "thread_user_001_demo_001",
	"answer": "Ocean Majesty next sails on..."
}
```

---

### Key Concepts That Need to Understand During This Lesson

- LangGraph is the orchestrator, not the database
- The model chooses tool calls, but your code executes tools
- Graph state is not the same as long-term memory
- Tool results become part of short-term context

---

## Lesson 2.2: Conversation Threads and Message Persistence 🔴 Essential

### Objective

Persist the full transcript independently from LangGraph checkpoint state.

### Topics Covered

1. Thread creation 🔴
2. Message persistence 🔴
3. Canonical transcript 🔴
4. User-specific thread IDs 🔴
5. Debug endpoints 🟡

### Subtopics

1. Thread Creation 🔴
    - Create thread per user conversation
    - Use deterministic demo IDs if needed

2. Message Persistence 🔴
    - Save user message before graph execution
    - Save assistant response after graph execution

3. Canonical Transcript 🔴
    - Messages table is used for UI, audit, replay, and debugging
    - Do not depend only on LangGraph checkpoints for transcript

4. User-Specific Thread IDs 🔴
   Use a pattern like:

```text
thread_{user_id}_{uuid}

```

Example:

```text
thread_user_001_01HX...

```

5. Debug Endpoints 🟡
    - Show messages for a thread
    - Show current user
    - Show thread metadata

---

### What to Build

Build:

```text
POST /threads
GET /threads/{thread_id}/messages
POST /chat

```

Persist:

```text
user messages
assistant messages
tool metadata if useful

```

---

### Key Concepts That Need to Understand During This Lesson

- `thread_id` keeps conversation continuity
- `user_id` scopes bookings and long-term memory
- transcript persistence is separate from graph state
- production systems need auditable message history

---

## Lesson 2.3: LangGraph Checkpointing and Thread Recovery 🔴 Essential

### Objective

Add checkpoint persistence so the graph can recover conversation state.

### Topics Covered

1. LangGraph checkpointer 🔴
2. PostgreSQL checkpointer 🔴
3. Thread recovery 🔴
4. Restart test 🔴
5. Checkpoint metadata 🟡

### Subtopics

1. Checkpointer 🔴
    - Compile graph with checkpointer
    - Invoke graph with `thread_id`

2. PostgreSQL Checkpointer 🔴
    - Use LangGraph Postgres checkpointer
    - Call setup once during startup
    - Use local PostgreSQL connection string

3. Thread Recovery 🔴
    - Same `thread_id`
    - Graph reloads latest persisted state
    - New user message is appended

4. Restart Test 🔴
    - Chat once
    - Stop backend
    - Restart backend
    - Continue same thread

5. Checkpoint Metadata 🟡
    - Store latest checkpoint info for debug UI
    - Do not duplicate full checkpoint content manually

LangGraph requires `thread_id` in graph config when using checkpointers, and the checkpointer stores snapshots of graph state for that thread.

---

### What to Build

Add:

```text
LangGraph Postgres checkpointer
checkpoint recovery test
GET /debug/threads/{thread_id}/checkpoint

```

---

### Key Concepts That Need to Understand During This Lesson

- Checkpoint is graph state snapshot
- Checkpoint is not the same as message table
- Checkpointing enables recovery, retries, and continuity
- PostgreSQL checkpointer is production-style; in-memory saver is only for testing

---

## Lesson 2.4: Manual Conversation Summarization 🔴 Essential

### Objective

Implement summarization yourself to understand production context management deeply.

### Topics Covered

1. Message threshold 🔴
2. Token threshold 🟡
3. Summary generation 🔴
4. Summary persistence 🔴
5. Summary injection 🔴
6. Recent message window 🔴

### Subtopics

1. Message Threshold 🔴
   Start simple:

```text
If message_count > 10, summarize older messages.

```

2. Token Threshold 🟡
   Improve later:

```text
If estimated_tokens > 5000, summarize older messages.

```

LangChain provides `trim_messages` to keep messages below token/message limits before sending them to the model.

3. Summary Generation 🔴
   Summarize:

```text
all messages except the latest 6

```

4. Summary Persistence 🔴
   Store in `summaries` table:

```text
thread_id
summary_text
covered_until_message_id
strategy = manual

```

5. Summary Injection 🔴
   Inject summary before recent messages:

```text
system prompt
+ conversation summary
+ long-term memories
+ recent messages
+ current user message

```

6. Recent Message Window 🔴
   Keep latest 6–8 raw messages because they carry immediate conversational nuance.

---

### What to Build

Build a manual summarization service:

```text
memory/manual_summarizer.py

```

Add flow:

```text
Before LLM call:
  load existing summary
  count messages
  if threshold reached:
    summarize older messages
    persist summary
  build context with summary + recent messages

```

Add debug endpoint:

```text
GET /debug/threads/{thread_id}/summary

```

---

### Key Concepts That Need to Understand During This Lesson

- Summary is compressed short-term context
- Summary is not automatically long-term memory
- Full message history should still be stored
- Summary must be explicitly injected into the model context
- `covered_until_message_id` prevents summarizing the same messages repeatedly

---

# Week 3 — Long-Term Memory, LangMem Summarization, UI, and Interview Polish

**Estimated Time:** ~14–18 hours

**Goal:** Add long-term memory, LangMem summarization, frontend UI, and interview-ready polish.

---

## Lesson 3.1: Short-Term vs Long-Term Memory 🔴 Essential

### Objective

Classify what should remain thread-scoped versus what should be remembered across conversations.

### Topics Covered

1. Short-term memory 🔴
2. Long-term memory 🔴
3. Memory classification 🔴
4. Memory persistence 🔴
5. Memory retrieval 🔴
6. Memory injection 🔴

### Subtopics

1. Short-Term Memory 🔴
   Store in:

```text
LangGraph state
checkpoint
conversation summary
recent messages

```

Examples:

```text
current sailing search filters
current booking lookup
current fare calculation parameters
latest tool result

```

2. Long-Term Memory 🔴
   Store in:

```text
long_term_memories table

```

Examples:

```text
User prefers balcony cabins.
User usually travels in August.
User wants prices in INR.
User prefers concise answers.

```

3. Memory Classification 🔴
   Add a classifier step after assistant response:

```text
ignore
short_term
long_term_preference
long_term_travel_preference
long_term_profile

```

4. Memory Persistence 🔴
   Store only if:

```text
stable
reusable
user-specific
safe
useful across future threads

```

5. Memory Retrieval 🔴
   On each message:

```text
load active memories for user_id
inject relevant memories into context

```

6. Memory Injection 🔴
   Add a memory block into the system/context prompt:

```text
Relevant user memories:
- User prefers balcony cabins.
- User usually travels in August.

```

LangGraph’s memory docs describe short-term memory as thread-scoped and long-term memory as user/application-scoped data reusable across threads.

---

### What to Build

Build:

```text
memory/memory_classifier.py
memory/memory_repository.py
memory/memory_injector.py

```

Add endpoints:

```text
GET /debug/users/{user_id}/memories
DELETE /debug/users/{user_id}/memories/{memory_id}

```

---

### Key Concepts That Need to Understand During This Lesson

- Not every message should become memory
- Long-term memory needs source tracking
- Memory should be user-scoped
- Memory should be editable/deletable
- Short-term memory helps current conversation; long-term memory helps future conversations

---

## Lesson 3.2: LangMem Summarization with `summarize_messages` 🔴 Essential

### Objective

Implement framework-assisted summarization and compare it with your manual approach.

### Topics Covered

1. LangMem purpose 🔴
2. `summarize_messages` 🔴
3. Running summary 🔴
4. Token threshold 🔴
5. Manual vs LangMem comparison 🔴

### Subtopics

1. LangMem Purpose 🔴
   LangMem helps manage long context by summarizing older messages when thresholds are reached.

2. `summarize_messages` 🔴
   Use it before the model call to produce:

```text
summarized message list
running summary

```

3. Running Summary 🔴
   Store running summary in graph state or persist it into your `summaries` table.

4. Token Threshold 🔴
   Example policy:

```text
max_tokens_before_summary = 3000
max_summary_tokens = 512

```

5. Manual vs LangMem 🔴
   Manual gives more application control. LangMem gives faster integration and cleaner graph-native summarization.

---

### What to Build

Add `summary_mode` support:

```text
manual
langmem_function

```

When thread uses `langmem_function`, call `summarize_messages`.

Update:

```text
conversation_threads.summary_mode

```

---

### Key Concepts That Need to Understand During This Lesson

- LangMem summarization is still part of your orchestration
- You still decide thresholds and persistence
- LangMem helps reduce custom summarization code
- Your database remains the source of truth for transcript and summaries

---

## Lesson 3.3: LangMem `SummarizationNode` 🔴 Essential

### Objective

Use `SummarizationNode` as a dedicated LangGraph node and compare it with direct `summarize_messages`.

### Topics Covered

1. Dedicated summarization node 🔴
2. Graph state keys 🔴
3. Input/output message keys 🔴
4. Summary replacement behavior 🔴
5. Production tradeoffs 🔴

### Subtopics

1. Dedicated Node 🔴
   Add summarization as part of graph flow:

```text
START
  ↓
summarization_node
  ↓
retrieve_memory
  ↓
agent
  ↓
tools
  ↓
memory_classifier
  ↓
END

```

2. State Keys 🔴
   Keep separate:

```text
messages
summary
summarized_messages
retrieved_memories

```

3. Input/Output Message Keys 🔴
   `SummarizationNode` can read from one state key and write summarized messages into another. LangMem’s `SummarizationNode` summarizes messages when they exceed a token limit and can replace them with a summary message.

4. Summary Replacement 🔴
   Understand that this approach changes what gets sent to the model, but you should still keep full message history in your database.

5. Production Tradeoffs 🔴
   Use `SummarizationNode` when your graph wants summary handling as a first-class graph step.

---

### What to Build

Add third summary mode:

```text
langmem_node

```

Support:

```text
manual
langmem_function
langmem_node

```

Add debug output:

```text
summary_mode
raw_message_count
summary_exists
recent_message_count

```

---

### Key Concepts That Need to Understand During This Lesson

- `summarize_messages` is function-style
- `SummarizationNode` is graph-node style
- Both reduce context size
- Neither replaces your database transcript
- Summary strategy should be visible in debug/demo mode

---

## Lesson 3.4: React + Tailwind Demo UI 🟡 Important

### Objective

Build a simple UI that makes your backend demo interview-friendly.

### Topics Covered

1. React + Vite setup 🔴
2. Tailwind setup 🔴
3. Chat screen 🔴
4. User selector 🔴
5. Thread selector 🔴
6. Debug panels 🟡

### Subtopics

1. React + Vite 🔴
   Create a small frontend app.

2. Tailwind 🔴
   Use simple clean UI. Do not overdesign.

3. Chat Screen 🔴
   Required:

```text
message list
input box
send button
loading state

```

4. User Selector 🔴
   Static seeded users:

```text
Kamran
Sarah
Arjun

```

5. Thread Selector 🔴
   Allow:

```text
create new thread
continue existing thread

```

6. Debug Panels 🟡
   Show:

```text
current thread_id
summary mode
current summary
long-term memories
message count
checkpoint status

```

---

### What to Build

Frontend pages/components:

```text
src/
  components/
    ChatWindow.tsx
    MessageBubble.tsx
    UserSelector.tsx
    ThreadSelector.tsx
    DebugPanel.tsx
  api/
    client.ts
  App.tsx

```

Backend endpoints needed:

```text
GET /users
GET /threads?user_id=user_001
POST /threads
POST /chat
GET /debug/threads/{thread_id}/summary
GET /debug/users/{user_id}/memories

```

---

### Key Concepts That Need to Understand During This Lesson

- Frontend should show conversation continuity clearly
- Debug panels make memory/checkpointing visible
- UI is for demonstration, not production polish
- Keep frontend simple and backend-focused

---

## Lesson 3.5: Final Production Polish and Interview Demo 🔴 Essential

### Objective

Make the project explainable, testable, and interview-ready.

### Topics Covered

1. README architecture 🔴
2. Demo script 🔴
3. Logging 🔴
4. Tests 🟡
5. Known limitations 🔴
6. Interview talking points 🔴

### Subtopics

1. README Architecture 🔴
   Include:

```text
system diagram
database model
agent graph
memory architecture
summary strategies
checkpoint recovery flow

```

2. Demo Script 🔴
   Prepare fixed prompts:

```text
1. Ask ship details
2. Search August sailings
3. Show booking confirmation
4. Calculate fare
5. Trigger manual summary
6. Trigger LangMem summary
7. Restart backend and recover thread
8. Start new thread and reuse long-term memory

```

3. Logging 🔴
   Log:

```text
thread_id
user_id
tool called
summary created
memory stored
checkpoint used
latency

```

4. Tests 🟡
   Add lightweight tests for:

```text
fare calculation
sailing search
booking lookup
manual summary threshold
memory classification

```

5. Known Limitations 🔴
   Be honest:

```text
No auth
No real payment
No real cruise supplier API
No vector database initially
No production permissions model

```

6. Interview Talking Points 🔴
   Practice this:

```text
I separated raw transcript, short-term state, long-term memory, and checkpointing.

Messages are the canonical transcript.
LangGraph checkpoints recover graph state.
Summaries compress old conversation context.
Long-term memories store stable user preferences.

```

---

### What to Build

Add:

```text
README.md
docs/architecture.md
docs/demo-script.md
docs/memory-design.md

```

Add final debug endpoint:

```text
GET /debug/threads/{thread_id}/state

```

---

### Key Concepts That Need to Understand During This Lesson

- Great AI projects are judged by architecture clarity, not just model output
- Memory must be inspectable
- Recovery must be demonstrable
- The project should show engineering judgment

---

# Final 2–3 Week Execution Plan

## Week 1 — Foundation and Domain Tools

### Target Outcome

A working FastAPI + PostgreSQL backend with cruise data and deterministic tools.

### Build

```text
Project setup
Database schema
Seed data
Cruise services
Tool-like service functions
Basic endpoints

```

### Lessons

```text
Lesson 1.1: Project Setup and Engineering Baseline
Lesson 1.2: Cruise Booking Domain Model
Lesson 1.3: Deterministic Cruise Services and Tools

```

### Done When

You can call:

```text
GET /ships
GET /sailings
GET /users/{user_id}/bookings
POST /fare/calculate

```

without using the LLM.

---

## Week 2 — Agent, Threads, Checkpoints, Manual Summary

### Target Outcome

A working LangGraph assistant with tool calling, persisted messages, checkpoint recovery, and manual summarization.

### Build

```text
LangGraph agent
Tool calling
POST /chat
conversation_threads
messages
LangGraph Postgres checkpointer
manual summary service
summary injection

```

### Lessons

```text
Lesson 2.1: First LangGraph Cruise Agent
Lesson 2.2: Conversation Threads and Message Persistence
Lesson 2.3: LangGraph Checkpointing and Thread Recovery
Lesson 2.4: Manual Conversation Summarization

```

### Done When

You can:

```text
Ask cruise questions
Use tools
Store messages
Restart backend
Recover thread
Trigger manual summary after threshold
Inject summary into future context

```

---

## Week 3 — Long-Term Memory, LangMem, UI, Demo Polish

### Target Outcome

A demo-ready app with long-term memory, LangMem summarization, React UI, and interview documentation.

### Build

```text
long_term_memories
memory classifier
memory retrieval
LangMem summarize_messages mode
LangMem SummarizationNode mode
React + Tailwind UI
debug panels
README and demo script

```

### Lessons

```text
Lesson 3.1: Short-Term vs Long-Term Memory
Lesson 3.2: LangMem Summarization with summarize_messages
Lesson 3.3: LangMem SummarizationNode
Lesson 3.4: React + Tailwind Demo UI
Lesson 3.5: Final Production Polish and Interview Demo

```

### Done When

You can demo:

```text
Manual summarization
LangMem summarization
Thread recovery
Long-term user preference reuse
Cruise booking tool calls
Debug visibility from UI

```

---

# Exactly When to Persist What

Use this as your production rulebook.

## Persist Raw Messages

Persist every user and assistant message in `messages`.

Use for:

```text
UI transcript
audit
debugging
replay
summary generation
analytics

```

Do this always.

---

## Persist Summaries

Persist summaries in `summaries`.

Use when:

```text
conversation becomes long
old context must be compressed
future turns need continuity
you need inspectable summary state

```

Do not treat summaries as full truth. They are compressed context.

---

## Persist Long-Term Memories

Persist structured facts/preferences in `long_term_memories`.

Use only when information is:

```text
stable
reusable
user-specific
safe
future-useful

```

Examples:

```text
User prefers balcony cabins.
User usually travels in August.
User prefers prices in INR.

```

---

## Persist Checkpoints

Let LangGraph Postgres checkpointer persist checkpoints.

Use for:

```text
graph recovery
short-term state
tool workflow continuation
thread-level memory

```

Do not use checkpoints as your only transcript store.

---

# Manual Summarization vs LangMem Summarization

## Manual Summarization Is Preferable When

Use manual summarization when you need:

```text
full database control
custom summary format
auditability
covered_until_message_id
business-specific summary rules
debug UI visibility
predictable persistence

```

This is best for learning and for enterprise-style apps.

---

## LangMem `summarize_messages` Is Preferable When

Use `summarize_messages` when you want:

```text
quick token-threshold summarization
less custom code
simple graph integration
running summary support

```

LangMem provides helpers for summarizing long contexts and maintaining running summaries.

---

## LangMem `SummarizationNode` Is Preferable When

Use `SummarizationNode` when:

```text
summarization should be a formal graph node
you want summarization visible in graph flow
you want cleaner LangGraph orchestration
you want less manual pre-processing

```

---

# Suggested Summary Thresholds

Start simple:

```text
Manual mode:
  summarize when message_count > 10
  keep last 6 messages raw

```

Then improve:

```text
Token-based mode:
  summarize when estimated_tokens > 5000
  keep last 1500-2000 tokens raw
  summary budget: 400-600 tokens

```

For LangMem:

```text
max_tokens_before_summary: 3000-5000
max_summary_tokens: 512

```

---

# Suggested Long-Term Memory Categories

Use these categories:

```text
travel_preference
communication_preference
profile
booking_preference
currency_preference
ignore

```

Examples:

```text
"I prefer balcony cabins."
→ travel_preference

"Always show prices in INR."
→ currency_preference

"Make this answer shorter."
→ ignore or short-term only

"I usually travel with my family."
→ profile or travel_preference

"For this search, only show August sailings."
→ short-term only

```

---

# Core Concepts You Must Be Able to Explain

By the end, you should clearly explain:

```text
Context:
  The final information sent to the model now.

Conversation history:
  Raw sequence of messages stored in DB.

Short-term memory:
  Thread-scoped state used during current conversation.

Long-term memory:
  Durable user-specific facts/preferences reused across threads.

Checkpoint:
  LangGraph state snapshot used for recovery and continuation.

Summary:
  Compressed representation of older conversation turns.

```

---

# What Not to Build Yet

Avoid these until the core project is done:

```text
Authentication
real cruise APIs
payment flow
Redis
Kafka
vector database
Kubernetes
multi-agent architecture
complex role permissions
full admin dashboard
mobile UI
voice interface

```

These will distract from the main learning goal.

---

# Final Interview Positioning

In interviews, describe the project like this:

> “I built a cruise booking AI assistant using FastAPI, PostgreSQL, SQLAlchemy, LangGraph, and OpenAI. The assistant can call deterministic cruise tools for ship details, sailing search, booking lookup, and fare calculation. I separated raw transcript persistence from LangGraph checkpointing. I implemented manual conversation summarization with thresholds and PostgreSQL persistence, then added LangMem-based summarization using both `summarize_messages` and `SummarizationNode`. I also added long-term memory classification for stable user preferences and demonstrated thread recovery using LangGraph checkpointers.”

That answer sounds like you understand production AI architecture, not just prompt engineering.
