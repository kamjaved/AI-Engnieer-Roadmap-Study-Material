# Month 1 — GenAI Engineer Roadmap

**Goal:** Build a solid foundation in LLM fundamentals, Python for AI, LLM APIs, prompt engineering, embeddings, and vector search.
**Duration:** 4 Weeks | 17 Lessons

---

## Overview

| Week   | Theme                         | Lessons   |
| ------ | ----------------------------- | --------- |
| Week 1 | LLM Fundamentals              | 1.1 – 1.8 |
| Week 2 | Python for AI Engineering     | 2.1 – 2.5 |
| Week 3 | LLM APIs & Prompt Engineering | 3.1 – 3.6 |
| Week 4 | Embeddings & Vector Search    | 4.1 – 4.4 |

---

## Lable Info

- 🔴 Essential / Must Know
- 🟡 Important / Good to Know
- 🟢 Optional / Nice to Have

# Week 1 — LLM Fundamentals

**Estimated Time:** ~6–7 hours
**Goal:** Build a solid mental model of how LLMs work so you can reason about their behavior, limitations, and tradeoffs in real engineering conversations.

---

## Lesson 1.1: How LLMs Work — The Big Picture 🔴 Essential

### Objective

Understand how LLMs generate text and why this seemingly simple objective produces capable models.

### Topics Covered

1. Next Token Prediction 🔴
2. True Data Distribution 🟡
3. Autoregressive Generation 🔴
4. Scale & Chinchilla Scaling Laws 🟡

### Subtopics

1. Next Token Prediction 🔴
   - Probability distribution over vocabulary
   - Training objective: maximize P(t\_{n+1} | t1...tn)
   - Why all capabilities emerge from this signal
2. True Data Distribution 🟡
   - What the model actually learns
   - Why training data composition matters
   - Strengths and weaknesses this creates
3. Autoregressive Generation 🔴
   - Sequential token generation
   - Why errors compound
   - Engineering implications (latency, streaming)
4. Scale & Chinchilla Scaling Laws 🟡
   - Optimal parameter-to-token ratio
   - Why smaller well-trained models can outperform larger ones
   - Modern trends: train longer, not necessarily bigger

---

### Key Concepts That Need to Understand During This Lesson

- Next-token prediction as the single training objective
- Autoregressive generation and its sequential nature
- Chinchilla scaling laws and compute-optimal training
- True data distribution vs. "understanding"
- Why hallucinations occur by design

---

### Interview Preparation

**Beginner Questions**

1. What is the core training objective of an LLM?
2. What does "autoregressive generation" mean?
3. Why can LLMs hallucinate confidently?

**Intermediate Questions**

1. What are the Chinchilla scaling laws and why do they matter when choosing a model?
2. If a model has 175B parameters trained on 300B tokens, what does Chinchilla say about it?
3. What are the engineering implications of autoregressive generation?

### Suggested Resources

- Andrej Karpathy — ["Intro to Large Language Models"](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- Chinchilla Paper — "Training Compute-Optimal Large Language Models" (Hoffmann et al., 2022)

---

## Lesson 1.2: The Transformer Architecture 🔴 Essential

### Objective

Understand the core components of the Transformer and why it replaced RNNs for language modeling.

### Topics Covered

1. Why RNNs Failed 🟡
2. Self-Attention (Q/K/V) 🔴
3. Multi-Head Attention 🔴
4. Feed-Forward Networks & Layer Normalization 🟡
5. Residual Connections 🟡
6. Quadratic Cost O(n²) 🔴

### Subtopics

1. Why RNNs Failed 🟡
   - Vanishing gradient problem
   - Sequential processing bottleneck
2. Self-Attention (Q/K/V) 🔴
   - Query, Key, Value roles
   - Attention formula: softmax(QKᵀ / sqrt(d_k)) \* V
   - Scaling factor and why it matters
3. Multi-Head Attention 🔴
   - Parallel attention heads
   - Each head learns a different relationship type
   - Concatenation and projection
4. Feed-Forward Networks & Layer Normalization 🟡
   - FFN as knowledge storage
   - Pre-norm vs post-norm
5. Residual Connections 🟡
   - Why they enable deep models
   - Gradient flow through identity paths
6. Quadratic Cost O(n²) 🔴
   - Why context window length is expensive
   - Implications for production serving

---

### Key Concepts That Need to Understand During This Lesson

- Self-attention mechanism (Q, K, V roles)
- Why attention is O(n²) and why it matters
- Multi-head attention and what each head learns
- Residual connections enabling deep training
- Why RNNs failed and Transformers succeeded

---

### Interview Preparation

**Beginner Questions**

1. What problem do residual connections solve?
2. What are Q, K, and V in self-attention?
3. Why did Transformers replace RNNs?

**Intermediate Questions**

1. Why is transformer attention O(n²) and what does this mean practically?
2. What is the role of multi-head attention versus a single attention head?
3. What does the feed-forward network do in a transformer layer?

### Suggested Resources

- "Attention Is All You Need" (Vaswani et al., 2017)
- Jay Alammar — ["The Illustrated Transformer"](http://jalammar.github.io/illustrated-transformer/)
- 3Blue1Brown — ["Attention in Transformers, visually explained"](https://www.youtube.com/watch?v=eMlx5fFNoYc)

---

## Lesson 1.3: Tokenization & BPE 🔴 Essential

### Objective

Understand how text is converted to tokens, why subword tokenization is the standard, and why it matters for engineering.

### Topics Covered

1. Why Naive Approaches Fail 🟡
2. Byte Pair Encoding (BPE) Algorithm 🔴
3. SentencePiece & tiktoken 🔴
4. Token Counting & Cost Estimation 🔴
5. Multilingual Tokenization Costs 🟡

### Subtopics

1. Why Naive Approaches Fail 🟡
   - Word-level: unbounded vocabulary, OOV problem
   - Character-level: sequence length explosion
   - Subword: the sweet spot
2. Byte Pair Encoding (BPE) 🔴
   - Starts with 256 byte vocabulary
   - Iterative merge of most frequent pairs
   - Vocabulary size: 32K–100K tokens
3. SentencePiece & tiktoken 🔴
   - SentencePiece: language-agnostic, raw Unicode
   - tiktoken: OpenAI's Rust-based tokenizer
   - When to use each
4. Token Counting & Cost Estimation 🔴
   - ~0.75 tokens/word for English
   - Always count with actual tokenizer
5. Multilingual Tokenization Costs 🟡
   - Non-English text: 2–3x more tokens
   - Code tokenization differences

---

### Key Concepts That Need to Understand During This Lesson

- BPE algorithm and why it produces subword units
- How vocabulary is learned from training data
- Why multilingual text uses more tokens for GPT models
- Token counting for context window management
- tiktoken usage for OpenAI models

---

### Hands-on Exercises

- Tokenize the same sentence with tiktoken in multiple languages and compare token counts
- Write a function that counts tokens before sending to the OpenAI API and truncates if needed

### Assignment

📄 Assignment File: `assignments/w01-a1-tokenizer-explorer.md`

Short description: Build a tokenizer explorer that compares token counts across languages, models, and content types.

---

### Interview Preparation

**Beginner Questions**

1. What is BPE and why is it preferred over word-level tokenization?
2. Why does the same sentence cost more tokens in Chinese than in English?
3. Why should you count tokens with the actual tokenizer rather than estimating?

**Intermediate Questions**

1. How does tokenization inefficiency affect model performance on non-English languages?
2. What is tiktoken and when would you use it over SentencePiece?
3. What happens if your prompt exceeds the model's context window?

---

## Lesson 1.4: Embeddings & Vector Space 🔴 Essential

### Objective

Understand what embeddings are, how they encode meaning geometrically, and how to use cosine similarity for comparison.

### Topics Covered

1. What Embeddings Are (for engineers) 🔴
2. Word Arithmetic 🟡
3. Static vs Contextual Embeddings 🔴
4. d_model and Dimensionality 🟡
5. Cosine Similarity 🔴

### Subtopics

1. What Embeddings Are 🔴
   - Dense vector representation of tokens/sentences
   - Learned during training, not hand-crafted
   - Semantic proximity in vector space
2. Word Arithmetic 🟡
   - king - man + woman ≈ queen
   - Relational structure as geometric directions
   - Why this enables semantic search
3. Static vs Contextual Embeddings 🔴
   - Word2Vec / GloVe: one vector per word
   - BERT / GPT: context-dependent vectors
   - "bank" example
4. d_model and Dimensionality 🟡
   - GPT-3: 12,288 | Llama 7B: 4,096
   - Trade-off: capacity vs compute/memory
5. Cosine Similarity 🔴
   - Formula: (A·B) / (‖A‖·‖B‖)
   - Range: -1 to 1
   - Threshold intuition for relevance

---

### Key Concepts That Need to Understand During This Lesson

- Embeddings as dense vector representations of meaning
- Static vs contextual embeddings and why contextual dominates
- Cosine similarity as the standard for comparing embeddings
- d_model and its role in model capacity
- Word arithmetic demonstrating relational structure

---

### Hands-on Exercises

- Compute cosine similarity between pairs of sentences using NumPy
- Visualize embedding similarity with a simple heatmap

### Assignment

📄 Assignment File: `assignments/w01-a2-embedding-playground.md`

Short description: Experiment with embeddings — compute similarities, explore vector arithmetic, and visualize the embedding space.

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between static and contextual embeddings?
2. Why is cosine similarity preferred over Euclidean distance for comparing embeddings?
3. What is d_model?

**Intermediate Questions**

1. Explain word arithmetic in embedding spaces. What does it reveal?
2. How are embeddings used in production retrieval systems?
3. What embedding dimensions would you choose for a RAG system and why?

---

## Lesson 1.5: Pre-training & Loss Functions 🟡 Important

### Objective

Understand how LLMs are trained, what data goes in, and how training scale relates to quality.

### Topics Covered

1. Cross-Entropy Loss 🟡
2. Dataset Composition 🟡
3. Training vs Inference Cost 🟡
4. Chinchilla Scaling (revisited in context of training) 🟢
5. "Trained on X Tokens" — What It Means 🟡

### Subtopics

1. Cross-Entropy Loss 🟡
   - -log(p_correct) intuition
   - What it means for the model to minimize loss
   - Perplexity as a reported metric
2. Dataset Composition 🟡
   - Common Crawl, Books, Wikipedia, Code, ArXiv
   - How composition drives capability
   - Data quality > raw scale
3. Training vs Inference Cost 🟡
   - Frontier training: millions of GPU hours
   - Inference: comparatively cheap
   - Fine-tuning: 100–1000x cheaper than pre-training
4. Chinchilla in Context 🟢
   - Overtraining smaller models: modern practice
   - Why inference cost drives the decision
   - Know the intuition from Lesson 1.1; the formula math is not tested at engineer level
5. What "Trained on X Tokens" Means 🟡
   - Tokenized count, not raw text
   - Parameters as compressed representation

---

### Key Concepts That Need to Understand During This Lesson

- Cross-entropy loss as the training signal
- How dataset composition determines model capabilities
- Training vs inference cost asymmetry
- Why modern models deliberately overtrain vs Chinchilla-optimal
- Perplexity as a measure of model uncertainty

---

### Interview Preparation

**Beginner Questions**

1. What is cross-entropy loss in LLM training?
2. Why does training data composition matter more than just size?
3. What is the approximate cost difference between training and inference?

**Intermediate Questions**

1. A model has 7B parameters trained on 1T tokens. Is this well-trained by Chinchilla standards?
2. Why do modern models deliberately exceed the Chinchilla-optimal token ratio?
3. How does data quality affect model performance?

---

## Lesson 1.6: Alignment — RLHF, SFT, DPO 🟡 Important

### Objective

Understand how base models are transformed into instruction-following assistants through alignment techniques.

### Topics Covered

1. Base Model vs Instruct Model 🔴
2. Supervised Fine-Tuning (SFT) 🟡
3. RLHF Reward Modeling 🟡
4. DPO (Direct Preference Optimization) 🟡
5. Constitutional AI 🟡
6. Safety vs Capability Tradeoff 🟡

### Subtopics

1. Base Model vs Instruct Model 🔴
   - Base model: text continuation
   - Instruct model: instruction-following, refusals
   - Same weights, different post-training
2. Supervised Fine-Tuning (SFT) 🟡
   - Human-written (prompt, ideal_response) pairs
   - Same next-token objective, different data
   - Why data quality >> quantity
3. RLHF 🟡
   - Step 1: SFT
   - Step 2: Reward model from human rankings
   - Step 3: PPO to maximize reward score
4. DPO 🟡
   - Eliminates separate reward model
   - Directly optimizes on (prompt, chosen, rejected) triples
   - Why it dominates open-source alignment
5. Constitutional AI & Safety Tradeoff 🟡
   - Self-critique against a constitution
   - Alignment tax: capability reduction from safety training

---

### Key Concepts That Need to Understand During This Lesson

- The gap between base and instruct models
- SFT as the first alignment step
- RLHF pipeline: reward model + PPO
- DPO as a simpler, stable RLHF alternative
- Alignment tax

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between a base model and an instruct model?
2. What is Supervised Fine-Tuning (SFT)?
3. What is the "alignment tax"?

**Intermediate Questions**

1. Explain the RLHF pipeline and its components.
2. How does DPO differ from RLHF and why has it become popular?
3. What is Constitutional AI and how does it scale safety training?

---

## Lesson 1.7: Inference & Sampling 🔴 Essential

### Objective

Understand how LLMs generate output at inference time and how to control generation quality through sampling parameters.

### Topics Covered

1. Greedy Decoding 🔴
2. Temperature 🔴
3. Top-p (Nucleus Sampling) 🔴
4. Top-k 🟡
5. Beam Search 🟢
6. Seed Parameter 🟡
7. KV-Cache 🔴

### Subtopics

1. Greedy Decoding 🔴
   - Always pick highest probability token
   - Deterministic but repetitive
2. Temperature 🔴
   - Scales logits before softmax
   - <1.0: focused; >1.0: creative
   - Production rules: low for factual, high for creative
3. Top-p (Nucleus Sampling) 🔴
   - Dynamic candidate set by cumulative probability
   - Preferred over top-k for adaptability
4. Top-k 🟡
   - Fixed candidate set regardless of distribution
   - When and why top-p is better
5. Beam Search 🟢
   - Multiple candidate sequences in parallel
   - Rarely used for chat; better for translation
   - Know the concept; not used for modern chat LLMs — deprioritized
6. Seed Parameter 🟡
   - Deterministic outputs for testing/debugging
   - Why reproducibility matters in production
7. KV-Cache 🔴
   - Caches computed K and V vectors
   - Reduces O(n²) to O(n) per step
   - Memory bottleneck at long contexts

---

### Key Concepts That Need to Understand During This Lesson

- Temperature and its effect on output diversity
- Top-p vs Top-k sampling
- Greedy decoding as a deterministic baseline
- KV-cache and its memory/speed tradeoffs
- When to use which sampling strategy

---

### Interview Preparation

**Beginner Questions**

1. What is temperature and how does it affect LLM outputs?
2. What is the KV-cache and why is it important?
3. When would you use greedy decoding vs nucleus sampling?

**Intermediate Questions**

1. Explain the difference between temperature, top-p, and top-k. When would you use each?
2. Why does KV-cache matter for serving long-context requests?
3. Why would you set a seed parameter when calling an LLM API?

---

## Lesson 1.8: Context Windows & Positional Encoding 🟡 Important

### Objective

Understand how transformers encode position, the constraints of context windows, and the engineering implications of long contexts.

### Topics Covered

1. Why Position Matters 🔴
2. Sinusoidal Encoding 🟡
3. RoPE (Rotary Positional Embedding) 🔴
4. ALiBi 🟢
5. FlashAttention 🔴
6. Sliding Window Attention 🟡
7. "Lost in the Middle" Problem 🔴
8. Context Extension Techniques 🟢

### Subtopics

1. Why Position Matters 🔴
   - Self-attention is permutation-invariant without position
   - Positional encoding adds order information
2. Sinusoidal Encoding 🟡
   - Fixed, computed (not learned)
   - Poor extrapolation beyond training length
3. RoPE 🔴
   - Rotation of Q and K vectors by position angle
   - Encodes relative position through dot product
   - Used in Llama, Mistral, Qwen
   - Context extension via YaRN
4. ALiBi 🟢
   - Linear distance bias on attention scores
   - No learned parameters, good extrapolation
   - Rarely used in modern architectures; RoPE dominates — know the name only
5. FlashAttention 🔴
   - IO-aware attention: tiles computed in on-chip SRAM
   - Memory O(n²) → O(n); 2–4x speedup
   - Enables practical long-context training
6. Sliding Window Attention 🟡
   - Local attention window of size w
   - O(n²) → O(n·w)
   - Used in Mistral models
7. "Lost in the Middle" 🔴
   - U-shaped attention: strong at start and end
   - RAG implication: place key docs at start or end
8. Context Extension Techniques 🟢
   - YaRN, sparse attention, ring attention

---

### Key Concepts That Need to Understand During This Lesson

- Why positional encoding is necessary in transformers
- RoPE as the dominant modern approach
- FlashAttention and its memory efficiency
- "Lost in the middle" and its RAG design implications
- Sliding window attention as a linear-cost alternative

---

### Interview Preparation

**Beginner Questions**

1. Why do transformers need positional encoding?
2. What is the "lost in the middle" problem?
3. What is FlashAttention?

**Intermediate Questions**

1. How does RoPE encode positional information and why is it preferred over sinusoidal?
2. Explain sliding window attention and its tradeoff.
3. How does "lost in the middle" affect RAG system design?

---

## Week 1 Summary Checklist

- [ ] Explain next-token prediction and why it produces capable models
- [ ] Describe the Transformer architecture: attention, FFN, residuals, layer norm
- [ ] Explain Q/K/V attention and why it is O(n²)
- [ ] Describe BPE tokenization and why multilingual text costs more tokens
- [ ] Explain the difference between static and contextual embeddings
- [ ] Discuss cosine similarity and its role in vector search
- [ ] Describe the pre-training process: data, loss function, scale
- [ ] Explain the alignment pipeline: SFT → RLHF/DPO → deployed model
- [ ] Choose appropriate sampling parameters for different use cases
- [ ] Explain KV-cache and why it matters for inference
- [ ] Describe positional encoding approaches (RoPE, ALiBi) and context extension
- [ ] Discuss the "lost in the middle" problem and its RAG implications

---

# Week 2 — Python for AI Engineering

**Estimated Time:** ~6–7 hours
**Goal:** Sharpen Python skills specifically for AI engineering — async, Pydantic, FastAPI, NumPy, and project structure.

---

## Lesson 2.1: Python Core for AI Engineers 🔴 Essential

### Objective

Master the Python patterns used daily in AI engineering: async, generators, type hints, and logging.

### Topics Covered

1. Type Hints Deep Dive 🔴
2. Async/Await for Concurrent API Calls 🔴
3. Generators & Iterators for Streaming 🔴
4. Decorators 🟡
5. Context Managers 🟡
6. f-strings & Structured Logging 🔴

### Subtopics

1. Type Hints 🔴
   - `Optional`, `Literal`, `TypedDict`, `Generic[T]`
   - Python 3.10+: `str | None`, `list[str]`
   - How type hints power Pydantic validation
2. Async/Await 🔴
   - `asyncio.gather()` for concurrent API calls
   - `asyncio.Semaphore` for rate limiting
   - Analogy: Python `Promise.all()` ≈ `asyncio.gather()`
3. Generators & Iterators 🔴
   - `yield` for lazy token streaming
   - `async for` in async generators
   - SSE stream consumption pattern
4. Decorators 🟡
   - Retry, caching, timing, observability
   - `@retry`, `@lru_cache`
5. Context Managers 🟡
   - `async with httpx.AsyncClient()`
   - Custom `@contextmanager` for tracing
6. Structured Logging 🔴
   - `structlog` for searchable production logs
   - Always log: prompt, params, response, latency, tokens

---

### Key Concepts That Need to Understand During This Lesson

- Async/await pattern for IO-bound API calls
- Generator-based streaming with `yield`
- Type hints and their runtime role via Pydantic
- Decorator pattern for cross-cutting concerns
- Structured logging vs print statements in production

---

### Hands-on Exercises

- Write an async function that makes 20 concurrent OpenAI API calls with a semaphore
- Write an async generator that consumes an SSE stream and yields parsed tokens

### Assignment

📄 Assignment File: `assignments/w02-a1-python-ai-toolkit.md`

Short description: Build a reusable Python toolkit covering async batch API calls, streaming, retry logic, and structured logging.

---

### Interview Preparation

**Beginner Questions**

1. How would you make 100 LLM API calls efficiently in Python?
2. Why are type hints important in AI engineering?
3. What is a context manager and when would you use one?

**Intermediate Questions**

1. Explain Python generators and why they matter for LLM streaming.
2. How does `asyncio.Semaphore` prevent API rate limit errors?
3. Why should production AI systems use structured logging instead of print?

---

## Lesson 2.2: Pydantic v2 for Structured AI 🔴 Essential

### Objective

Use Pydantic to define, validate, and parse structured LLM outputs in a type-safe pipeline.

### Topics Covered

1. BaseModel 🔴
2. Field Validators 🔴
3. JSON Schema Generation 🔴
4. model_validate / model_validate_json 🔴
5. Discriminated Unions 🟡
6. Why Pydantic is Infrastructure for LLM Output Parsing 🔴

### Subtopics

1. BaseModel 🔴
   - Typed fields with auto-validation
   - `Field(description=...)` for schema metadata
   - Replacing raw dict patterns
2. Field Validators 🔴
   - `@field_validator`: single-field constraints
   - `@model_validator`: cross-field logic
   - Running validation on LLM output before use
3. JSON Schema Generation 🔴
   - `MyModel.model_json_schema()`
   - Passes schema to LLM API for constrained output
   - Single source of truth pattern
4. model_validate 🔴
   - `model_validate(dict)` and `model_validate_json(str)`
   - `ValidationError` gives exact failure details
5. Discriminated Unions 🟡
   - Union type with a literal discriminator field
   - Used for agent tool selection (multi-type responses)
6. Why Pydantic is Infrastructure 🔴
   - OpenAI SDK: `client.beta.chat.completions.parse()`
   - LangChain, Instructor, Marvin all build on it

---

### Key Concepts That Need to Understand During This Lesson

- BaseModel as the contract between LLM and application code
- Field validators as runtime safety net on LLM outputs
- JSON Schema generation as the LLM API communication format
- Discriminated unions for multi-type agent responses
- Single source of truth: one model, one schema, one validator

---

### Hands-on Exercises

- Define a Pydantic model for an LLM extraction task and validate a sample JSON response
- Build a discriminated union for an agent with 3 different tool output types

### Assignment

📄 Assignment File: `assignments/w02-a2-pydantic-structured-outputs.md`

Short description: Use Pydantic to extract structured data from LLM responses with full validation and error handling.

---

### Interview Preparation

**Beginner Questions**

1. What is a Pydantic BaseModel?
2. What does `model_json_schema()` return and why is it useful?
3. What is `model_validate_json()` and when do you use it?

**Intermediate Questions**

1. How does Pydantic bridge the gap between LLM outputs and typed Python code?
2. What is a discriminated union in Pydantic and when would you use it in an AI application?
3. How does `model_json_schema()` relate to OpenAI's structured outputs feature?

---

## Lesson 2.3: UV Package Manager & Project Structure 🟡 Important

### Objective

Set up a professional Python project for AI engineering with UV, pyproject.toml, and a clean directory structure.

### Topics Covered

1. Why UV over pip/poetry 🟡
2. pyproject.toml 🟡
3. Virtual Environments 🔴
4. Project Layout for AI Apps 🟡

### Subtopics

1. Why UV 🟡
   - 10–100x faster than pip (Rust-based)
   - Unified: venv + resolution + lockfiles
   - Compatible with pip and pyproject.toml
2. pyproject.toml 🟡
   - Project metadata, dependencies, dev dependencies
   - Tool configurations: ruff, mypy
3. Virtual Environments 🔴
   - `uv venv` + `uv pip install`
   - Why isolation matters for AI projects (conflicting torch versions)
4. Project Layout 🟡
   - `src/app/api/`, `agents/`, `prompts/`, `models/`, `services/`
   - Prompts separate from logic (change independently)
   - Config via pydantic-settings, never global vars

---

### Key Concepts That Need to Understand During This Lesson

- UV as the modern Python package manager
- pyproject.toml as the single project config file
- Virtual environment isolation for AI projects
- Separation of concerns in AI app structure

---

### Interview Preparation

**Beginner Questions**

1. Why would you choose UV over pip for an AI project?
2. What is pyproject.toml and what goes in it?
3. Why is a virtual environment mandatory for AI projects?

**Intermediate Questions**

1. How would you structure a production AI application in Python?
2. Why should prompt templates be separated from application logic?
3. How does pydantic-settings handle environment variables for configuration?

---

## Lesson 2.4: NumPy Essentials for Embeddings 🟡 Important

### Objective

Learn the minimal NumPy needed to work with embeddings: dot products, cosine similarity, and vectorized batch operations.

### Topics Covered

1. Vectors & Matrices Basics 🟡
2. Dot Product 🟡
3. Cosine Similarity Implementation 🟡
4. Broadcasting 🟡

### Subtopics

1. Vectors & Matrices Basics 🟡
   - 1D array = single embedding; 2D = batch
   - `.shape`, indexing, array creation
2. Dot Product 🟡
   - `np.dot(a, b)` or `a @ b`
   - `batch @ query`: all-in-one similarity scores
3. Cosine Similarity 🟡
   - Full implementation without library
   - Batch cosine similarity with normalization
   - `np.argsort` for top-k retrieval
4. Broadcasting 🟡
   - Subtract mean from all embeddings without a loop
   - Normalization across a batch

---

### Key Concepts That Need to Understand During This Lesson

- Vectorized operations vs Python loops (performance)
- Dot product as fast cosine similarity for normalized vectors
- Batch operations for embedding similarity at scale
- L2 normalization before dot product

---

### Hands-on Exercises

- Implement cosine similarity from scratch using NumPy
- Write a function that returns top-5 most similar embeddings from a batch

### Interview Preparation

**Beginner Questions**

1. Implement cosine similarity for two embedding vectors without using a library.
2. What is the shape of a batch of 100 embeddings with 1536 dimensions?
3. What does `np.argsort` do and how is it used in retrieval?

**Intermediate Questions**

1. Why is vectorized NumPy computation important for embedding operations?
2. When can you replace cosine similarity with a simple dot product?
3. What is broadcasting and how does it apply to batch normalization?

---

## Lesson 2.5: FastAPI Fundamentals 🔴 Essential

### Objective

Build async AI backends with FastAPI: streaming endpoints, typed request/response models, dependency injection, and CORS.

### Topics Covered

1. Why FastAPI for AI Backends 🔴
2. Route Handlers 🔴
3. Request/Response Models with Pydantic 🔴
4. SSE Streaming 🔴
5. Dependency Injection 🟡
6. CORS for React Frontends 🟡

### Subtopics

1. Why FastAPI 🔴
   - Native async for concurrent LLM calls
   - Built on Pydantic (same models for validation + docs)
   - Automatic OpenAPI/Swagger docs
2. Route Handlers 🔴
   - `@app.post("/chat")` + `async def`
   - Automatic 422 on invalid input
3. Request/Response Models 🔴
   - Always define Pydantic models per endpoint
   - Anti-pattern: accepting raw `dict`
4. SSE Streaming 🔴
   - `StreamingResponse` with async generator
   - `data: {json}\n\n` SSE format
   - React consumption with `fetch` + `ReadableStream`
5. Dependency Injection 🟡
   - `Depends()` for shared LLM clients and DB connections
   - Override in tests with mock clients
6. CORS 🟡
   - `CORSMiddleware` setup for localhost:3000
   - Why SSE streams can fail silently due to CORS

---

### Key Concepts That Need to Understand During This Lesson

- FastAPI's native async support for LLM workloads
- SSE streaming pattern end-to-end (backend + frontend)
- Pydantic models as the API contract in FastAPI
- Dependency injection for testable AI services
- CORS configuration for React frontends

---

### Hands-on Exercises

- Build a `/chat` endpoint that calls OpenAI and returns a non-streaming response
- Build a `/chat/stream` endpoint using `StreamingResponse` with SSE format

### Assignment

📄 Assignment File: `assignments/w02-a3-fastapi-llm-endpoint.md`

Short description: Build a FastAPI service with both streaming and non-streaming LLM endpoints, proper error handling, and CORS configured for a React frontend.

---

### Interview Preparation

**Beginner Questions**

1. Why is FastAPI well-suited for AI backends compared to Flask?
2. What is `StreamingResponse` and when do you use it?
3. How do you configure CORS in FastAPI?

**Intermediate Questions**

1. How would you implement streaming LLM responses to a React frontend?
2. Explain FastAPI's dependency injection and why it matters for AI applications.
3. How do you test a FastAPI endpoint that calls an external LLM without making real API calls?

---

## Week 2 Summary Checklist

- [ ] Use modern Python type hints including Union, Literal, TypedDict
- [ ] Write async code for concurrent LLM API calls with asyncio.gather and Semaphore
- [ ] Implement streaming with async generators and understand the SSE protocol
- [ ] Define Pydantic v2 models with field and model validators
- [ ] Generate JSON Schema from Pydantic models for LLM structured output
- [ ] Use discriminated unions for multi-type LLM responses
- [ ] Set up a Python project with UV and pyproject.toml
- [ ] Structure an AI application with proper separation of concerns
- [ ] Compute cosine similarity using NumPy
- [ ] Build a FastAPI endpoint that calls an LLM and streams the response
- [ ] Configure CORS for a React frontend
- [ ] Use FastAPI dependency injection for testable AI services

---

# Week 3 — LLM APIs & Prompt Engineering

**Estimated Time:** ~12–15 hours
**Goal:** Go from understanding LLMs conceptually to controlling them programmatically across multiple providers.

---

## Lesson 3.1: OpenAI SDK Deep Dive 🔴 Essential

### Objective

Master the OpenAI Python SDK for production use: completions, streaming, tool calling, structured outputs, error handling, and prompt caching.

### Topics Covered

1. Chat Completions API (`/v1/chat/completions`) 🔴
2. Responses API (`/v1/responses`) — New Primary API 🔴
3. Streaming via Server-Sent Events (SSE) 🔴
4. Function / Tool Calling 🔴
5. Structured Outputs (JSON mode & `response_format`) 🔴
6. Error Handling & Retries 🔴
7. Token Counting & Cost Estimation 🔴
8. Prompt Caching 🔴

### Subtopics

1. Chat Completions API 🔴
   - Roles: `system`, `user`, `assistant`, `tool`
   - Key params: `temperature`, `max_tokens`, `top_p`, `stop`
   - Stateless: every call must include full context
2. Responses API 🔴 _(new — replaces Assistants API)_
   - `client.responses.create()` — the new unified stateful API
   - Concept mapping: Assistants → Prompts; Threads → Conversations; Runs → Responses
   - **Assistants API is deprecated (sunset August 26, 2026)** — do NOT start new projects on it
   - Supports native MCP server connections
   - Chat Completions API remains supported for stateless calls; Responses API for stateful/agentic workflows
3. Streaming (SSE) 🔴
   - `stream=True` → chunk-by-chunk delta
   - `finish_reason`: `stop`, `tool_calls`, `length`
   - Production pattern: pipe to WebSocket or SSE endpoint
4. Tool Calling 🔴
   - Define tools with JSON Schema
   - Model returns `tool_calls` array
   - You execute; model never runs code
   - `tool_choice`: `auto`, `required`, `none`
5. Structured Outputs 🔴
   - JSON mode: valid JSON, no schema enforcement
   - `response_format=MyPydanticModel`: guaranteed schema
   - `client.beta.chat.completions.parse()` → typed object
6. Error Handling 🔴
   - `RateLimitError`, `APITimeoutError`, `BadRequestError`
   - `client = OpenAI(max_retries=3, timeout=30.0)`
7. Token Counting 🔴
   - `tiktoken.encoding_for_model("gpt-4o")`
   - Count before sending; estimate cost
8. Prompt Caching 🔴 _(new)_
   - Automatic for OpenAI — zero code changes required
   - Activates on prompts ≥ 1,024 tokens; cache hits in 128-token increments
   - Discount: ~50% on gpt-4o family; ~90% on GPT-5.x models
   - Cache TTL: 5–10 minutes of inactivity
   - Best practice: static content first (system prompt, tool schemas), dynamic content last (user message)
   - Monitor via `usage.cached_tokens` in every response

---

### Key Concepts That Need to Understand During This Lesson

- Message roles and stateless API design
- Tool calling loop: define → model calls → you execute → return result
- Difference between JSON mode and structured outputs
- Error types and exponential backoff retry strategy
- Token counting for context management and cost estimation
- Responses API as the replacement for the deprecated Assistants API
- Prompt caching as a production cost optimization (50–90% savings on cached input tokens)

---

### Interview Preparation

**Beginner Questions**

1. What happens if you exceed the context window with your input tokens?
2. What is tool calling and how does it work?
3. What is the difference between JSON mode and structured outputs?
4. What is prompt caching and how does OpenAI implement it automatically?

**Intermediate Questions**

1. Explain the difference between `tool_choice="auto"` and `tool_choice="required"`.
2. Why is streaming important in production LLM applications, and what are the tradeoffs?
3. How do structured outputs differ from JSON mode, and when would you still choose JSON mode?
4. How would you structure a system prompt to maximize OpenAI's prompt cache hit rate?

---

## Lesson 3.2: Anthropic SDK (Claude) 🔴 Essential

### Objective

Understand the Claude Messages API structure, tool use patterns, prompt caching, and key differences from OpenAI.

### Topics Covered

1. Messages API Structure 🔴
2. Tool Use in Claude 🔴
3. System Prompts Best Practices 🔴
4. Streaming with Anthropic 🔴
5. Prompt Caching with `cache_control` 🔴
6. Key Differences from OpenAI API 🔴

### Subtopics

1. Messages API Structure 🔴
   - `system` as top-level param (not a message)
   - Strict `user`/`assistant` alternation
   - `content` as array of content blocks
   - `stop_reason`, `usage` in response
2. Tool Use 🔴
   - `input_schema` instead of `parameters`
   - Tool inputs returned as parsed dict (not JSON string)
   - `tool_result` blocks reference `tool_use` id
3. System Prompts Best Practices 🔴
   - XML tags for structured system prompts
   - Identity + constraints first
   - Dynamic context in user messages, not system
4. Streaming 🔴
   - `client.messages.stream()` context manager
   - Event types: `content_block_delta`, `message_stop`
   - `stream.text_stream` high-level abstraction
5. Prompt Caching with `cache_control` 🔴 _(new)_
   - **90% discount** on cached input tokens (reads cost 10% of base input rate)
   - Explicit opt-in: add `cache_control: {"type": "ephemeral"}` to static content blocks
   - Place cache breakpoints on: system prompt, tool definitions, large reference documents
   - Supports up to 4 cache breakpoints per request
   - TTL: 5 minutes (default) or 1 hour (extended, costs 2× write fee)
   - Write cost: 1.25× base input on first request — break-even after just 2 reads
   - Monitor via `cache_creation_input_tokens` and `cache_read_input_tokens` in response usage
   - At scale: saves 60–90% of total token costs for high-traffic apps
6. Key Differences from OpenAI 🔴
   - System prompt location
   - Content block format
   - `max_tokens` required vs optional
   - Message alternation constraints

---

### Key Concepts That Need to Understand During This Lesson

- Claude's content block model vs OpenAI's string response
- Strict message alternation and how to handle multi-tool responses
- Why system prompt placement matters for Claude
- Tool input as a parsed dict (not JSON string)
- When to choose Claude vs GPT-4o
- Prompt caching with `cache_control` for 90% cost reduction on repeated context

---

### Interview Preparation

**Beginner Questions**

1. How does Claude's Messages API structure differ from OpenAI's?
2. Where does the system prompt go in the Anthropic SDK?
3. What is `stop_reason` in a Claude response?
4. What is `cache_control` in an Anthropic request and what does it enable?

**Intermediate Questions**

1. How does Claude's tool use differ from OpenAI's, and what are the practical implications?
2. Why does Anthropic require strict user/assistant message alternation?
3. When would you choose Claude over GPT-4o for a production system?
4. You have a 10K-token system prompt sent with every request at 50K requests/day. How do you use Anthropic prompt caching and what is the cost math?

---

## Lesson 3.3: Google Gemini API 🟡 Important

### Objective

Understand the Gemini API's multimodal capabilities and pricing position in the provider landscape.

### Topics Covered

1. Generative AI SDK (`google-genai`) 🟡
2. Multimodal Inputs (text, images, audio, video, PDFs) 🟡
3. Function Calling in Gemini 🟡
4. Key Differences from OpenAI/Anthropic 🟡

### Subtopics

1. Generative AI SDK 🟡
   - `client.models.generate_content()`
   - `GOOGLE_API_KEY` env var
2. Multimodal Inputs 🟡
   - `types.Part.from_uri()` for video/audio
   - Use cases: video summarization, audio analysis, PDF understanding
3. Function Calling 🟡
   - `types.FunctionDeclaration` and `types.Tool`
   - `GenerateContentConfig(tools=[...])`
4. Key Differences 🟡
   - Native video/audio vs image+text
   - Gemini Flash: cheapest at scale
   - Context: up to 2M tokens
   - `generate_content` SDK style vs messages array
   - Gemini 2.5 Pro/Flash support implicit prompt caching (automatic, no code changes)

---

### Key Concepts That Need to Understand During This Lesson

- Gemini's multimodal-first design
- Pricing advantage for high-volume workloads (Gemini Flash)
- Function calling with `FunctionDeclaration`
- When Gemini's 2M context window is the right choice

---

### Interview Preparation

**Beginner Questions**

1. What makes Gemini different from OpenAI and Anthropic at a high level?
2. What types of inputs can Gemini handle natively?
3. Which Gemini model tier is best for high-volume, cost-sensitive workloads?

**Intermediate Questions**

1. When would Gemini be the right choice over OpenAI/Anthropic for a production system?
2. How would you design a system that uses all three providers?
3. What is Gemini Flash and what workloads is it optimized for?

---

## Lesson 3.4: Prompt Engineering Mastery 🔴 Essential

### Objective

Master the full prompt engineering toolkit for production systems: few-shot, CoT, ReAct, system prompt design, and injection defense.

### Topics Covered

1. Zero-shot vs Few-shot Prompting 🔴
2. Chain-of-Thought (CoT) Prompting 🔴
3. ReAct Pattern (Thought → Action → Observation) 🔴
4. Role Prompting 🟡
5. System Prompt Design 🔴
6. Prompt Templates & Variables 🔴
7. Output Formatting Techniques 🔴
8. Prompt Injection Defense Basics 🔴

### Subtopics

1. Zero-shot vs Few-shot 🔴
   - When zero-shot fails; when few-shot fixes it
   - Choosing representative edge-case examples
2. Chain-of-Thought 🔴
   - "Think step by step" trigger phrase
   - Accuracy improvement on multi-step reasoning
   - Structured outputs to separate reasoning from answer
3. ReAct Pattern 🔴
   - Thought → Action (tool call) → Observation → repeat
   - Max iteration limit to prevent infinite loops
   - Foundation of all agent systems
4. Role Prompting 🟡
   - Expertise level + domain + behavioral constraints
   - Why vague roles add nothing
5. System Prompt Design 🔴
   - Sections: Identity, Capabilities, Rules, Context, Output Format
   - XML tags for structure (especially Claude)
   - Version control prompts alongside code
6. Prompt Templates & Variables 🔴
   - `string.Template` or Jinja2 for variable injection
   - Prompts as versioned, testable artifacts
7. Output Formatting 🔴
   - JSON/markdown/XML output instructions
   - Providing the exact schema inline
8. Prompt Injection Defense 🔴
   - Direct vs indirect injection
   - Delimiters, input sanitization, privilege separation
   - Output validation before action execution

---

### Key Concepts That Need to Understand During This Lesson

- Few-shot examples as task definition by demonstration
- CoT as accuracy improvement for multi-step tasks
- ReAct as the mental model for all agent loops
- System prompt structure for production applications
- Prompt injection as the #1 LLM security concern

---

### Hands-on Exercises

- Write a zero-shot, few-shot, and CoT version of the same classification prompt; compare accuracy
- Design a production system prompt with all required sections

### Assignment

📄 Assignment File: `assignments/w03-a1-prompt-engineering-lab.md`

Short description: A structured lab comparing zero-shot vs few-shot vs CoT accuracy on a classification task, plus system prompt design.

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between zero-shot and few-shot prompting?
2. What is Chain-of-Thought prompting and when does it help?
3. What is prompt injection?

**Intermediate Questions**

1. How would you implement the ReAct pattern in a production system?
2. You have a classification task where zero-shot gets 70% and few-shot gets 85%. Client needs 95%+. What do you do?
3. How do you design a system prompt for a production customer-facing application?

### Suggested Resources

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

---

## Lesson 3.5: Multi-Provider Patterns 🟡 Important

### Objective

Build provider-agnostic LLM systems with fallback routing, cost optimization, and rate limit handling.

### Topics Covered

1. Provider Abstraction Layer 🟡
2. Fallback Routing 🟡
3. Cost Optimization via Model Routing 🟡
4. Rate Limiting Strategies 🟡

### Subtopics

1. Provider Abstraction Layer 🟡
   - Common `LLMResponse` dataclass
   - Abstract `LLMProvider` base class
   - Provider-specific adapters: system prompt placement, tool format normalization
2. Fallback Routing 🟡
   - Ordered provider list; try next on failure
   - Log which provider served which request
   - Quality monitoring per provider
3. Model Routing by Task Complexity 🟡
   - Cheap model for classification/extraction
   - Mid-tier for reasoning/code
   - Premium for complex multi-step analysis
   - 60–80% cost reduction with proper routing
4. Rate Limiting 🟡
   - Client-side token bucket
   - Exponential backoff + jitter
   - Request queuing and provider spreading

---

### Key Concepts That Need to Understand During This Lesson

- Provider abstraction as the foundation for multi-provider systems
- Fallback routing for reliability
- Model routing for cost optimization
- Client-side rate limiting to prevent 429s
- The cost/latency/quality triangle

---

### Hands-on Exercises

- Build a `LLMProvider` abstract class and implement OpenAI and Anthropic adapters
- Add a `FallbackRouter` that tries the next provider on failure

### Assignment

📄 Assignment File: `assignments/w03-a2-multi-provider-api-lab.md`

Short description: Build a provider-agnostic LLM client with OpenAI and Anthropic adapters, fallback routing, and basic rate limiting.

---

### Interview Preparation

**Beginner Questions**

1. Why would you build a provider abstraction layer?
2. What is model routing and why does it reduce costs?
3. What is exponential backoff and when do you use it?

**Intermediate Questions**

1. Design a provider abstraction layer. What are the trickiest parts to normalize across OpenAI, Anthropic, and Gemini?
2. A production system is hitting OpenAI's rate limits during peak hours. Walk through your solution.
3. How would you implement cost-based model routing in a production RAG system?

---

## Lesson 3.6: Introduction to MCP (Model Context Protocol) 🔴 Essential

> **Why this is here:** MCP has 97M+ monthly SDK downloads, is adopted by every major AI vendor (Anthropic, OpenAI, Google, Microsoft, AWS), and appears in the majority of 2026 Agentic AI Engineer job descriptions. It was donated to the Linux Foundation in December 2025. Not knowing what MCP is at Month 1 is a visible interview gap.

### Objective

Understand what MCP is, why it exists, its architecture, and why it has become the production standard for connecting AI agents to tools and data — before implementing it in Month 2.

### Topics Covered

1. The N×M Problem MCP Solves 🔴
2. What MCP Is (Conceptual Model) 🔴
3. MCP Architecture: Host, Client, Server 🔴
4. Three MCP Primitives: Tools, Resources, Prompts 🔴
5. Transport Modes (stdio and Streamable HTTP) 🟡
6. MCP vs REST APIs — When to Use Each 🔴
7. Real-World Ecosystem Snapshot 🟡

### Subtopics

1. The N×M Problem MCP Solves 🔴
   - Without MCP: N AI models × M tools = N×M bespoke integrations to maintain
   - With MCP: one server per tool, consumed by any MCP-compatible client → N+M
   - Before MCP: custom adapter per model per tool; switching models meant rewriting integrations
2. What MCP Is 🔴
   - Open standard for connecting AI assistants to external tools, data sources, and services
   - Think of it as USB-C for AI: one protocol, any device
   - Released by Anthropic, November 2024; donated to Linux Foundation (AAIF), December 2025
   - Adopted by OpenAI, Google DeepMind, Microsoft, and AWS by mid-2025
   - Built on JSON-RPC 2.0; 97M+ monthly SDK downloads as of March 2026
3. MCP Architecture: Host, Client, Server 🔴
   - **Host:** the AI application that needs tools (Claude Desktop, your custom agent, Cursor)
   - **Client:** lives inside the host; manages one stateful session per MCP server
   - **Server:** exposes tools/data; can be local or remote; one server per integration
   - Hosts create one client per server; all communicate via JSON-RPC 2.0
4. Three MCP Primitives 🔴
   - **Tools:** functions the AI can call (query a DB, call an API, execute code)
   - **Resources:** read-only data the AI can access (files, documents, DB records)
   - **Prompts:** reusable prompt templates the server exposes
   - AI discovers available tools and resources at runtime — nothing is hardcoded
5. Transport Modes 🟡
   - **stdio (local):** inter-process communication; default for local servers (Claude Desktop, Claude Code)
   - **Streamable HTTP (remote):** for production remote MCP servers; replaced HTTP+SSE in November 2025 spec
   - Note: HTTP+SSE transport was deprecated in March 2025 — treat it as legacy in any tutorial you encounter
6. MCP vs REST APIs 🔴
   - REST: developer hardcodes which endpoint to call at write-time
   - MCP: AI discovers available tools at runtime and decides when/how to call them
   - REST exposes capabilities to developers; MCP exposes capabilities to reasoning systems
   - MCP wraps REST/GraphQL APIs underneath — they coexist, not compete
7. Real-World Ecosystem Snapshot 🟡
   - 97M+ monthly SDK downloads (Python + TypeScript) as of March 2026
   - 10,000+ public MCP servers in production
   - Pre-built servers available: Google Drive, Slack, GitHub, Postgres, Puppeteer
   - Enterprise vendors with production MCP connectors: Atlassian, Salesforce, SAP

---

### Key Concepts That Need to Understand During This Lesson

- The N×M integration problem and how MCP reduces it to N+M
- MCP three-layer architecture: Host creates Clients → Clients connect to Servers
- The three primitives: Tools (callable), Resources (readable), Prompts (reusable templates)
- Why MCP is the production standard over bespoke function-call adapters
- Difference between stdio (local) and Streamable HTTP (remote) transports
- MCP vs A2A: MCP = agent-to-tool; A2A = agent-to-agent (A2A covered in Month 2)

---

### Interview Preparation

**Beginner Questions**

1. What is MCP and what problem does it solve?
2. What is the difference between an MCP Host, a Client, and a Server?
3. What are the three types of capabilities an MCP server can expose?

**Intermediate Questions**

1. How is MCP different from calling a REST API directly through LLM tool calling?
2. Why was the HTTP+SSE transport deprecated and what replaced it?
3. Your team needs an AI agent to access Postgres, GitHub, and an internal knowledge base. How does MCP change the integration design compared to building custom function-call adapters?

### Suggested Resources

- [MCP Official Specification](https://modelcontextprotocol.io/specification)
- [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — debug MCP servers locally without an LLM

---

## Week 3 Summary Checklist

- [ ] Built working chat completions with OpenAI, Anthropic, and Gemini
- [ ] Implemented streaming responses and displayed tokens incrementally
- [ ] Built a tool-calling loop with at least one tool per provider
- [ ] Used structured outputs to extract typed data from unstructured text
- [ ] Wrote a production system prompt with all required sections
- [ ] Implemented few-shot + CoT and measured accuracy improvement
- [ ] Built a basic provider abstraction that can swap between OpenAI and Anthropic
- [ ] Completed the Prompt Engineering Lab assignment
- [ ] Completed the Multi-Provider API Lab assignment
- [ ] Implemented prompt caching on Anthropic (cache_control) and verified cache hits via cache_read_input_tokens
- [ ] Implemented prompt caching on OpenAI and monitored cached_tokens in response usage
- [ ] Can explain what MCP is, its three-layer architecture, and why it replaced bespoke integrations

---

# Week 4 — Embeddings & Vector Search

**Estimated Time:** ~12–15 hours
**Goal:** Build a working semantic search pipeline — from embedding models to vector databases to search quality measurement.

---

## Lesson 4.1: Embedding Models in Practice 🔴 Essential

### Objective

Choose and use embedding models effectively, with an understanding of dimensions, batch processing, and cost tradeoffs.

### Topics Covered

1. OpenAI text-embedding-3-small / text-embedding-3-large 🔴
2. Sentence-Transformers (open-source) 🔴
3. Embedding Dimensions vs Quality Tradeoff 🔴
4. Batch Embedding Strategies 🔴
5. Normalization 🔴

### Subtopics

1. OpenAI Embedding Models 🔴
   - `text-embedding-3-small` (1536d) vs `text-embedding-3-large` (3072d)
   - `dimensions` parameter via Matryoshka learning
   - Start at 512 dims, benchmark before scaling
2. Sentence-Transformers 🔴
   - `all-MiniLM-L6-v2`: fast baseline (384d)
   - `BAAI/bge-large-en-v1.5`: high quality (1024d); `BAAI/bge-m3` for multilingual
   - Check the **MTEB Leaderboard** (huggingface.co/spaces/mteb/leaderboard) before choosing a model — rankings evolve
   - When to prefer local vs API (privacy, cost, latency)
3. Dimensions vs Quality 🔴
   - 512 → 1536: meaningful gains; 1536 → 3072: diminishing returns
   - Storage costs scale linearly with dimensions
4. Batch Embedding 🔴
   - OpenAI: up to 2048 inputs per request
   - Async batch calls for throughput
5. Normalization 🔴
   - Unit length (L2 norm = 1)
   - Normalized embeddings: cosine = dot product

---

### Key Concepts That Need to Understand During This Lesson

- Matryoshka embeddings and their production advantage
- When to use commercial vs open-source embedding models
- Embedding dimensions as the cost/quality tradeoff knob
- Batch embedding for large-scale ingestion
- Why normalization matters for similarity metrics
- MTEB leaderboard as the standard benchmark for comparing open-source embedding models

---

### Interview Preparation

**Beginner Questions**

1. What is the difference between `text-embedding-3-small` and `text-embedding-3-large`?
2. When would you choose open-source embeddings over OpenAI's API?
3. Why should you normalize embeddings?

**Intermediate Questions**

1. Explain Matryoshka embeddings and why they matter for production systems.
2. You have 5 million documents to embed. Design the embedding pipeline.
3. How do you choose the right embedding dimension for a RAG system?

---

## Lesson 4.2: Vector Databases 🔴 Essential

### Objective

Choose and use the right vector database for the task: ChromaDB for development, pgvector for production, with awareness of Qdrant, Pinecone, Weaviate, and FAISS.

### Topics Covered

1. ChromaDB (local development) 🔴
2. pgvector (production — PostgreSQL extension) 🔴
3. Qdrant (awareness) 🟡
4. Pinecone / Weaviate (awareness) 🟢
5. FAISS (awareness) 🟢
6. Indexing Strategies (HNSW, IVF) 🔴
7. Distance Metrics (cosine, Euclidean, dot product) 🔴

### Subtopics

1. ChromaDB 🔴
   - In-process, no server, local directory persistence
   - `PersistentClient`, `collection.add()`, `collection.query()`
   - Good up to ~100K docs
2. pgvector 🔴
   - PostgreSQL extension: `vector(512)` column type
   - HNSW index: `CREATE INDEX USING hnsw`
   - `<=>` cosine distance operator
   - Hybrid search: vector + full-text SQL in one query
3. Qdrant 🟡
   - Purpose-built, Rust-based, horizontally scalable
   - Use at 10M+ vectors or advanced filtering
4. Pinecone / Weaviate 🟢 _(awareness only)_
   - **Pinecone:** fully managed cloud vector database; serverless option available; common in US/global job descriptions
   - **Weaviate:** open-source; supports hybrid search natively; GraphQL API; self-hostable
   - Both appear frequently alongside Qdrant in 2026 hiring requirements
   - For Month 1: know their names and positioning; production usage covered in Month 3+
5. FAISS 🟢
   - Library, not a database
   - In-memory, no persistence, no metadata
   - Use for batch benchmarking or custom pipelines
6. Indexing: HNSW vs IVF 🔴
   - HNSW: layered graph, excellent recall, high memory
   - IVF: k-means clusters, lower memory, sensitive to tuning
   - Default: HNSW; IVF only under memory constraint
7. Distance Metrics 🔴
   - Cosine: direction-based, magnitude-invariant (default for text)
   - Dot product: equivalent to cosine if normalized (faster)
   - Euclidean: avoid for text embeddings

---

### Key Concepts That Need to Understand During This Lesson

- ChromaDB vs pgvector decision criteria
- HNSW index parameters: `m` and `ef_construction`
- Why cosine similarity is the default for text embeddings
- How pgvector enables hybrid search without extra infrastructure
- When to add a dedicated vector DB vs staying on pgvector

---

### Interview Preparation

**Beginner Questions**

1. What is ChromaDB and when would you use it?
2. What is pgvector and what does the `<=>` operator do?
3. What is HNSW indexing?

**Intermediate Questions**

1. Compare pgvector and Qdrant. When would you choose each?
2. Explain HNSW indexing. How do the parameters `m` and `ef_construction` affect performance?
3. How would you handle a schema migration when your embedding model changes?

---

## Lesson 4.3: Semantic Search Architecture 🔴 Essential

### Objective

Build a complete semantic search system: ingestion pipeline, chunking strategies, hybrid search, and retrieval quality measurement.

### Topics Covered

1. Document Ingestion Pipeline 🔴
2. Chunking Strategies 🔴
3. Metadata Filtering 🔴
4. Hybrid Search (Vector + BM25) 🔴
5. Search Quality Measurement 🔴

### Subtopics

1. Document Ingestion Pipeline 🔴
   - Extract → Clean → Chunk → Enrich → Embed → Store → Index
   - Batch async pipeline for large datasets
2. Chunking Strategies 🔴
   - Fixed-size: simple, splits mid-thought
   - Overlap chunking: 10–20% overlap prevents boundary loss
   - Recursive chunking: split on paragraphs → sentences → words
   - Semantic chunking: embedding-based topic boundary detection
   - Production default: recursive at 400–600 tokens, 10–15% overlap
3. Metadata Filtering 🔴
   - Filter before vector search to narrow candidates
   - Essential fields: source, date, doc type, access control
   - pgvector: SQL `WHERE` clause + vector order
4. Hybrid Search 🔴
   - Vector: semantic meaning
   - BM25: exact keyword/identifier matching
   - Reciprocal Rank Fusion (RRF) to merge results
   - Start: 70% vector / 30% keyword
5. Search Quality Measurement 🔴
   - Precision@k: fraction of top-k that are relevant
   - Recall@k: fraction of relevant found in top-k
   - MRR: rank of first relevant result
   - NDCG: are most relevant results ranked highest?
   - Golden dataset: 50–100 query-relevance pairs minimum

---

### Key Concepts That Need to Understand During This Lesson

- The two-pipeline architecture (ingestion vs query)
- Chunking as the highest-impact retrieval decision
- Why hybrid search consistently outperforms either approach alone
- Retrieval quality as the ceiling for RAG quality
- Precision@k, Recall@k, MRR as standard retrieval metrics

---

### Hands-on Exercises

- Build a recursive text chunker with configurable size and overlap
- Implement Reciprocal Rank Fusion for combining vector and keyword results
- Compute precision@5 and MRR on a small golden dataset

### Interview Preparation

**Beginner Questions**

1. What is recursive chunking and why is it preferred over fixed-size?
2. What is hybrid search and why does it outperform vector-only search?
3. What is precision@k?

**Intermediate Questions**

1. Compare fixed-size, recursive, and semantic chunking. When would you use each?
2. Design a hybrid search system. How do you determine the weight between vector and keyword search?
3. How do you evaluate retrieval quality, and how does it affect the overall RAG system?

---

## Lesson 4.4: Capstone P1 — Semantic Search Engine (Planning & Build) 🔴 Essential

### Objective

Scope, architect, build, and deploy a production-quality semantic search engine as the Month 1 capstone project.

### Topics Covered

1. Project Scoping 🔴
2. Architecture Decisions (DECISIONS.md) 🔴
3. Tech Stack Selection 🔴
4. Deployment Planning 🔴

### Subtopics

1. Project Scoping 🔴
   - Focused domain: 1K–10K docs
   - One search interface with metadata filtering
   - Measurable retrieval quality
2. DECISIONS.md 🔴
   - Format: Context → Options → Decision → Consequences
   - Document every tech choice with tradeoffs
3. Tech Stack 🔴
   - Python + FastAPI + pgvector + React
   - Deployment: Railway / Render / Fly.io (free tier + Postgres)
4. Deployment 🔴
   - Managed Postgres with pgvector (Supabase, Neon, Railway)
   - Dockerized FastAPI backend
   - React frontend on Vercel
   - Environment variables for API keys

---

### Key Concepts That Need to Understand During This Lesson

- How to scope a realistic project for a 1-week timeline
- DECISIONS.md as the artifact that shows engineering maturity
- Deployment as a required deliverable (not optional)
- Retrieval eval as proof the system works

---

### Hands-on Exercises

- Write DECISIONS.md entries for at least 3 architectural choices
- Deploy the ingestion pipeline and run it on a real dataset

### Assignment

📄 Assignment File: `assignments/w04-a1-semantic-search-engine.md`

Short description: Build and deploy a semantic search engine over a real dataset with hybrid search, metadata filtering, and measured retrieval quality.

---

### Interview Preparation

**Beginner Questions**

1. How would you scope a capstone project to fit a 1-week timeline?
2. What is DECISIONS.md and why do senior engineers write it?
3. What is the minimum viable deployment for a capstone project?

**Intermediate Questions**

1. Walk through the architecture of a semantic search system end-to-end.
2. How would you measure whether your search system is actually good?
3. What tradeoffs did you make in your tech stack selection, and why?

---

## Week 4 Summary Checklist

- [ ] Generated embeddings with OpenAI API (text-embedding-3-small)
- [ ] Generated embeddings with sentence-transformers (local model)
- [ ] Benchmarked different dimension sizes on sample queries
- [ ] Stored and queried vectors in ChromaDB
- [ ] Set up pgvector in PostgreSQL and ran similarity queries
- [ ] Implemented recursive text chunking with overlap
- [ ] Built a document ingestion pipeline (extract → chunk → embed → store)
- [ ] Implemented hybrid search (vector + keyword)
- [ ] Measured retrieval quality (precision@k, recall@k, MRR)
- [ ] Wrote DECISIONS.md with at least 3 architecture decisions
- [ ] Deployed Capstone P1 (accessible via URL)
- [ ] Completed the Semantic Search Engine assignment

---

# Month 1 Complete ✓

You now have:

1. A mental model of how LLMs work at an engineering level
2. Production Python skills: async, Pydantic, FastAPI
3. Practical SDK skills across OpenAI, Anthropic, and Gemini — including prompt caching on all three
4. Prompt engineering mastery
5. Conceptual fluency with MCP — the production standard for AI tool integration (implementation in Month 2)
6. A deployed semantic search capstone with documented decisions

**Next → Month 2: RAG Architecture, Agents, MCP Implementation, Evals, and Observability**
