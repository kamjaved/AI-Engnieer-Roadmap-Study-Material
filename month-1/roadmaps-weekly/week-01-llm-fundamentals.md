# Week 1 — LLM Fundamentals

[Back to Roadmap](../ROADMAP.md)

**Estimated Time:** ~6-7 hours (lessons + review)
**Goal:** Build a solid mental model of how Large Language Models work — from architecture to alignment — so you can reason about their behavior, limitations, and design tradeoffs in real engineering conversations.

---

## Lesson 1.1 — How LLMs Work: The Big Picture

### Sub-topics
- Next Token Prediction
- True Data Distribution
- Autoregressive Generation
- Scale & Chinchilla Scaling Laws

### Key Concepts

**Next Token Prediction.** At the most fundamental level, an LLM is a function that takes a sequence of tokens and outputs a probability distribution over the entire vocabulary for what the next token should be. During training, the model sees billions of sequences and learns to predict the next token given all preceding tokens. This seemingly simple objective — predict the next word — turns out to be extraordinarily powerful. To predict well, the model must learn grammar, facts, reasoning patterns, code syntax, and even aspects of world knowledge. The training objective is: given tokens t1, t2, ..., tn, maximize the probability P(t_{n+1} | t1, ..., tn). Every capability you see in ChatGPT or Claude emerges from this single training signal.

**True Data Distribution.** The model is trying to approximate the true data distribution — the statistical patterns present in its training corpus. If 80% of the training data follows a certain grammatical pattern, the model learns to assign high probability to that pattern. This is why training data composition matters enormously. A model trained mostly on English text will be weaker in other languages. A model trained on code alongside natural language will be better at coding. The model does not "understand" in the human sense; it has learned an incredibly rich compressed representation of the statistical structure of human-generated text. This distinction matters for engineering because it explains both the model's strengths (fluent, knowledgeable-seeming text) and weaknesses (hallucinations, inability to truly verify facts).

**Autoregressive Generation.** Generation happens one token at a time. The model predicts token 1, appends it to the input, predicts token 2, appends it, and so on. This is called autoregressive generation. Each new token is conditioned on all previous tokens (both the original prompt and all generated tokens so far). This has critical engineering implications: (1) generation is inherently sequential — you cannot parallelize the generation of a single sequence; (2) errors compound — if the model generates a wrong token early, all subsequent tokens are conditioned on that mistake; (3) latency scales linearly with output length. This is why streaming responses is standard practice in production — users see tokens as they are generated rather than waiting for the full response.

**Scale & Chinchilla Laws.** The Chinchilla scaling laws (Hoffmann et al., 2022) established that model performance improves predictably with both model size (parameters) and training data (tokens). The key finding: for a fixed compute budget, there is an optimal ratio of parameters to training tokens. Many earlier models (like the original GPT-3 at 175B parameters) were actually undertrained relative to their size. Chinchilla (70B parameters, 1.4T tokens) outperformed the much larger Gopher (280B parameters) by training on 4x more data. The practical takeaway for engineers: bigger is not always better. A smaller, well-trained model can outperform a larger, undertrained one. This insight drives current trends toward smaller but heavily trained models (Llama 3 8B trained on 15T tokens).

### Interview Questions

**Q1: Explain how an LLM generates text. What is the core training objective?**
**A:** An LLM is trained with a next-token prediction objective. Given a sequence of tokens, it learns to predict the probability distribution of the next token. During generation, it samples from this distribution, appends the chosen token to the input, and repeats the process autoregressively. The training objective is to minimize cross-entropy loss between the model's predicted distribution and the actual next token across the entire training corpus.

**Q2: Why can LLMs hallucinate confidently? Connect this to how they work.**
**A:** LLMs approximate statistical patterns in training data. They assign probabilities to token sequences, not truth values to claims. A sequence like "The capital of Australia is Sydney" has high surface-level plausibility because similar patterns appear in training data (Sydney is the most well-known Australian city). The model has no built-in fact-verification mechanism — it produces whatever continuation has high probability given the context. This is why retrieval-augmented generation (RAG) and grounding are critical in production systems.

**Q3: What are the Chinchilla scaling laws, and why do they matter for choosing a model?**
**A:** The Chinchilla paper showed that for a fixed compute budget, model performance is maximized by balancing parameter count with training token count — roughly 20 tokens per parameter. This means a smaller model trained on more data can outperform a larger undertrained model. For engineers, this means: don't just look at parameter count. A 7B model trained on 15T tokens (like Llama 3) may outperform older 70B models trained on far fewer tokens. It also means smaller models are cheaper to serve while potentially delivering comparable quality.

**Q4: What is autoregressive generation, and what are its engineering implications?**
**A:** Autoregressive generation means tokens are produced sequentially, each conditioned on all previous tokens. Engineering implications: (1) generation latency scales linearly with output length; (2) you cannot parallelize generation of a single sequence; (3) streaming is essential for good UX — send tokens to the user as they are generated; (4) errors early in the sequence affect everything that follows, which is why techniques like chain-of-thought prompting help the model "think step by step."

**Q5: If a model is "175B parameters, trained on 300B tokens," what does that tell you?**
**A:** By Chinchilla standards (20 tokens per parameter), a 175B model should ideally be trained on ~3.5T tokens. At only 300B tokens, this model is severely undertrained — it has far more capacity than the training data can fill. You would expect it to underperform a smaller model (say 15B) trained on the same 300B tokens. Modern practice has shifted heavily toward the "train longer on more data" approach.

### Resources
- Andrej Karpathy — ["Intro to Large Language Models"](https://www.youtube.com/watch?v=zjkBMFhNj_g) (1hr talk, essential viewing)
- Lilian Weng — ["Large Language Model Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Chinchilla Paper — "Training Compute-Optimal Large Language Models" (Hoffmann et al., 2022)

---

## Lesson 1.2 — The Transformer Architecture

### Sub-topics
- Why RNNs Failed
- Self-Attention (Q/K/V)
- Multi-Head Attention
- Quadratic Cost O(n²)
- Feed-Forward Networks
- Layer Normalization
- Residual Connections

### Key Concepts

**Why RNNs Failed.** Before Transformers, recurrent neural networks (RNNs) and LSTMs were the standard for sequence modeling. They process tokens one at a time, maintaining a hidden state that theoretically carries information from earlier tokens. Two fatal problems: (1) the vanishing gradient problem made it extremely difficult to learn long-range dependencies — by the time gradients propagated back through 100+ time steps, they effectively vanished to zero; (2) sequential processing meant you could not parallelize training across positions in a sequence. A 1000-token sequence required 1000 sequential steps. Transformers solved both problems by processing all positions simultaneously through the attention mechanism.

**Self-Attention (Q/K/V).** Self-attention is the core mechanism that allows every token to directly attend to every other token. For each token, the model computes three vectors: Query (Q — "what am I looking for?"), Key (K — "what do I contain?"), and Value (V — "what information do I carry?"). Attention scores are computed as: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V. The dot product QK^T measures similarity between queries and keys. The softmax turns these into a probability distribution. The result is a weighted sum of value vectors, where the weights reflect how relevant each token is to the current token. The division by sqrt(d_k) prevents the dot products from growing too large in high dimensions, which would push the softmax into regions with near-zero gradients.

**Multi-Head Attention.** Rather than computing a single attention function, the model runs multiple attention "heads" in parallel. Each head has its own learned Q, K, V projection matrices, allowing it to attend to different aspects of the input. One head might learn to track syntactic relationships (subject-verb agreement), another might focus on semantic similarity, another on positional proximity. The outputs of all heads are concatenated and projected through a final linear layer. GPT-3 uses 96 heads; smaller models use 12-32. This is computationally equivalent to a single larger attention but far more expressive — each head can learn a different "type" of attention pattern.

**Quadratic Cost O(n²).** The QK^T computation produces an n×n attention matrix where n is the sequence length. This means both memory and computation scale quadratically with context length. Doubling the context window from 4K to 8K tokens quadruples the attention computation. This is the fundamental bottleneck limiting context windows. At 128K tokens, the attention matrix has 16 billion entries per head per layer. This is why techniques like FlashAttention (memory-efficient attention computation), sliding window attention, and sparse attention patterns are active research areas. For engineers, this means context window size directly impacts latency and cost.

**Feed-Forward Networks.** Each transformer layer contains a feed-forward network (FFN) applied independently to each position. It typically consists of two linear transformations with a non-linearity (usually GeLU) in between: FFN(x) = W2 * GeLU(W1 * x + b1) + b2. The inner dimension is typically 4x the model dimension (e.g., d_model=4096, d_ff=16384). Research suggests FFNs act as key-value memories — they store factual knowledge learned during training. The attention layers handle routing and composition of information, while FFNs store and retrieve the actual knowledge.

**Layer Normalization.** Layer normalization normalizes the activations across the feature dimension for each token independently. It stabilizes training by keeping activation magnitudes in a consistent range. Modern transformers use "pre-norm" (normalize before attention/FFN) rather than the original "post-norm" (normalize after), as pre-norm produces more stable training dynamics. This is a small but critical detail — without proper normalization, deep transformer training becomes unstable.

**Residual Connections.** Every sub-layer (attention and FFN) has a residual connection: output = sublayer(x) + x. The input is added directly to the output. This allows gradients to flow directly through the network without degradation, enabling training of very deep models (GPT-3 has 96 layers). Residual connections mean each layer only needs to learn the "delta" — what to add to the existing representation — rather than reconstructing the entire representation from scratch.

### Interview Questions

**Q1: Explain the self-attention mechanism. What are Q, K, and V?**
**A:** Self-attention allows each token to weigh the relevance of all other tokens. Each token position produces three vectors through learned linear projections: Query (what information this position seeks), Key (what information this position offers), and Value (the actual content to retrieve). Attention scores are computed as softmax(QK^T / sqrt(d_k)) * V. The dot product of Q and K measures relevance, softmax normalizes into weights, and these weights are used to create a weighted sum of V vectors. The sqrt(d_k) scaling prevents dot products from becoming too large in high-dimensional spaces.

**Q2: Why is transformer attention O(n²), and what does this mean practically?**
**A:** The attention computation requires computing the dot product between every pair of token positions, producing an n×n matrix. Both memory and compute scale quadratically with sequence length. Practically, this means: going from 4K to 32K context costs 64x more compute in the attention layers; context window size is a key factor in inference cost and latency; this drives research into efficient attention mechanisms like FlashAttention, sparse attention, and sliding window approaches.

**Q3: What is the role of multi-head attention? Why not use a single attention head?**
**A:** Multiple heads allow the model to attend to different types of relationships simultaneously. One head might learn syntactic dependencies, another coreference, another semantic similarity. Using a single head would force one attention pattern per layer. Multi-head attention is equivalent in parameter count to a single large head but far more expressive because each head learns an independent attention pattern. The outputs are concatenated and linearly projected to produce the final result.

**Q4: What problem do residual connections solve in transformers?**
**A:** Residual connections (output = sublayer(x) + x) create a direct path for gradients to flow through the network, preventing vanishing gradients in deep models. Without them, a 96-layer model would be nearly impossible to train. They also mean each layer only needs to learn an incremental update rather than a complete transformation, making optimization easier.

**Q5: Why did Transformers replace RNNs for language modeling?**
**A:** Two main reasons: (1) Parallelization — RNNs process tokens sequentially; transformers process all positions simultaneously during training, enabling massive speedups on GPUs. (2) Long-range dependencies — RNNs struggle with vanishing gradients over long sequences; self-attention gives every token direct access to every other token regardless of distance. The tradeoff is that attention is O(n²) while RNNs are O(n), but the parallelization advantage dominates in practice.

### Resources
- "Attention Is All You Need" (Vaswani et al., 2017) — the original Transformer paper
- Jay Alammar — ["The Illustrated Transformer"](http://jalammar.github.io/illustrated-transformer/)
- 3Blue1Brown — ["Attention in Transformers, visually explained"](https://www.youtube.com/watch?v=eMlx5fFNoYc)

---

## Lesson 1.3 — Tokenization & BPE

### Sub-topics
- Why Naive Approaches Fail
- Byte Pair Encoding (BPE) Algorithm
- SentencePiece
- tiktoken
- Token Counting
- Multilingual Costs

### Key Concepts

**Why Naive Approaches Fail.** You might think we can just split text on spaces — but that creates an enormous vocabulary (every unique word is a token), cannot handle new or misspelled words, and treats "run," "running," and "runner" as completely unrelated tokens. Character-level tokenization solves the vocabulary problem but makes sequences extremely long (a 1000-word document becomes ~5000 characters), crushing attention's O(n²) cost. Subword tokenization (BPE and variants) strikes the sweet spot: common words get their own tokens ("the" = 1 token), while rare words are decomposed into meaningful subword pieces ("unforgettable" = "un" + "forget" + "table").

**Byte Pair Encoding (BPE).** BPE starts with a base vocabulary of individual bytes (256 entries). It then iteratively finds the most frequently co-occurring pair of tokens in the training corpus and merges them into a new token. After thousands of merge operations, you get a vocabulary of 32K-100K tokens that efficiently represents the training data. The key insight: BPE is learned from the training corpus. Common sequences get their own tokens; rare sequences are decomposed into smaller pieces. This is why GPT models tokenize "the" as one token but might split an unusual name into 4-5 tokens.

**SentencePiece and tiktoken.** SentencePiece (Google) treats the input as a raw byte stream and does not require pre-tokenization — it works directly on Unicode text, making it language-agnostic. tiktoken (OpenAI) is the tokenizer used by GPT models. It is extremely fast (implemented in Rust) and uses a BPE variant with specific regex-based pre-tokenization patterns. When building production systems, you should use tiktoken (for OpenAI models) or the model's specific tokenizer to accurately count tokens before making API calls.

**Token Counting and Multilingual Costs.** Token counting is critical for cost estimation and context window management. English text averages ~0.75 tokens per word (4 characters per token). But this varies wildly by language: Chinese text often uses 2-3x more tokens per character because BPE was trained predominantly on English text. Code also tokenizes differently — Python keywords are usually single tokens, but variable names get split. In production, always count tokens with the actual tokenizer, never estimate by word count. A 4K token limit might fit 3000 English words but only 1500 words of Chinese text.

### Interview Questions

**Q1: What is BPE and why is it preferred over word-level or character-level tokenization?**
**A:** BPE (Byte Pair Encoding) is a subword tokenization algorithm that iteratively merges the most frequent character pairs. It balances vocabulary size (typically 32K-100K) against sequence length. Word-level tokenization creates unbounded vocabularies and cannot handle OOV words. Character-level creates very long sequences (expensive for O(n²) attention). BPE achieves a practical middle ground: common words are single tokens, rare words decompose into reusable subword units.

**Q2: Why does the same sentence cost more tokens in Chinese than in English for GPT models?**
**A:** BPE vocabularies are learned from training data. Since GPT models are trained predominantly on English text, the BPE merges heavily favor English character sequences. Common English words like "the" or "and" become single tokens. Chinese characters appear less frequently in training data, so fewer merges target them, resulting in less efficient encoding — often 2-3x more tokens per semantic unit compared to English.

**Q3: Why should you count tokens with the actual tokenizer rather than estimating by word count?**
**A:** Token counts vary significantly by content type and language. English averages ~0.75 tokens/word but code, technical text, and non-English languages can differ dramatically. Underestimating can cause truncation or API errors; overestimating wastes context budget. Using tiktoken (for OpenAI) or the model's tokenizer gives exact counts, which is essential for context window management, cost estimation, and chunking strategies in RAG systems.

**Q4: How does tokenization affect the "intelligence" of a model on different languages?**
**A:** Inefficient tokenization for a language means: (1) the same content consumes more of the context window, reducing effective context; (2) more tokens means more generation steps and higher cost; (3) the model has seen fewer tokens of that language during training relative to its representation in the vocabulary. All three factors degrade performance. This is why multilingual models (like those from Mistral or specialized builds) often use tokenizers trained on more balanced multilingual corpora.

### Hands-on
- [Assignment: Tokenizer Explorer](./assignments/w01-a1-tokenizer-explorer.md)

---

## Lesson 1.4 — Embeddings & Vector Space

### Sub-topics
- What Vectors Are (for engineers)
- Word Arithmetic
- Static vs Contextual Embeddings
- d_model
- Cosine Similarity

### Key Concepts

**What Vectors Are.** In the context of LLMs, an embedding is a dense vector (list of floating-point numbers) that represents a token, word, sentence, or document in a high-dimensional space. GPT-3 uses d_model=12288 — each token is represented by a vector of 12,288 numbers. These numbers are not hand-crafted; they are learned during training. The key property: semantically similar items end up close together in this vector space. "Dog" and "puppy" will have similar vectors; "dog" and "refrigerator" will be far apart. This geometric structure is what makes similarity search, clustering, and retrieval possible.

**Word Arithmetic.** The classic example: vector("king") - vector("man") + vector("woman") ≈ vector("queen"). This demonstrates that embedding spaces capture relational structure — gender, tense, plurality, and other linguistic properties are encoded as consistent directions in the vector space. For engineers, this means embeddings capture meaning, not just surface form. This property is what makes vector databases useful for semantic search — you can find documents that are conceptually related even if they use completely different words.

**Static vs Contextual Embeddings.** Static embeddings (Word2Vec, GloVe) assign one fixed vector per word regardless of context. The word "bank" gets the same embedding whether it means a river bank or a financial bank. Contextual embeddings (from transformers like BERT or GPT) produce different vectors for the same word depending on its surrounding context. Each layer of the transformer refines the token's representation based on its context. This is far more powerful and is why transformer-based embeddings dominate modern NLP. When you use an embedding API (OpenAI's text-embedding-ada-002, for instance), you are getting contextual embeddings.

**d_model and Dimensionality.** d_model is the core dimension of the transformer — every token's representation is a vector of this size throughout the model. GPT-3: 12,288. Llama 2 7B: 4,096. Larger d_model means more capacity to represent nuance but costs more memory and compute. Embedding models used for search/retrieval typically use 768-1536 dimensions. There is an interesting tradeoff: higher dimensions capture more nuance but require more storage and make similarity computation slower. For most RAG applications, 1536 dimensions (OpenAI's default) works well.

**Cosine Similarity.** The standard metric for comparing embeddings. Cosine similarity measures the angle between two vectors, ignoring their magnitude: cos_sim(A, B) = (A · B) / (||A|| * ||B||). It ranges from -1 (opposite) to 1 (identical direction). In practice, for normalized embeddings, cosine similarity equals the dot product. This is the foundation of vector search — "find the documents whose embeddings are most similar to the query embedding." Understanding this is essential for building and debugging RAG systems. A cosine similarity of 0.85+ typically indicates high semantic relevance; below 0.7 is usually weak.

### Interview Questions

**Q1: What is the difference between static and contextual embeddings?**
**A:** Static embeddings (Word2Vec, GloVe) assign one fixed vector per word regardless of context — "bank" always maps to the same point. Contextual embeddings (from transformers) produce different vectors for the same word based on surrounding context — "river bank" and "bank account" yield different embeddings for "bank." Contextual embeddings are far more powerful for downstream tasks because they capture polysemy and context-dependent meaning.

**Q2: Why is cosine similarity preferred over Euclidean distance for comparing embeddings?**
**A:** Cosine similarity measures the angle between vectors, making it invariant to vector magnitude. Two documents about the same topic but of different lengths will have similar directions but different magnitudes. Cosine similarity captures their semantic similarity regardless of length. Euclidean distance would incorrectly penalize the magnitude difference. Additionally, cosine similarity is bounded [-1, 1], making thresholds interpretable across different embedding models.

**Q3: Explain the concept of "word arithmetic" in embedding spaces. What does it reveal?**
**A:** Word arithmetic (e.g., king - man + woman ≈ queen) shows that embedding spaces encode semantic relationships as consistent geometric directions. The direction from "man" to "woman" represents a gender transformation that applies across concepts. This reveals that embeddings capture structured, composable meaning — not just surface-level word associations. It is the foundation for why vector search works: semantic relationships are geometric relationships.

**Q4: What is d_model, and how does it affect a model's capabilities?**
**A:** d_model is the dimensionality of token representations throughout the transformer. Higher d_model (e.g., 12,288 for GPT-3 vs 4,096 for Llama 7B) provides more capacity to encode nuance and relationships but increases memory, compute, and storage costs. For embedding models used in retrieval, typical dimensions are 768-1536. The choice involves a tradeoff: enough dimensions to capture meaningful semantic distinctions without excessive computational cost.

### Hands-on
- [Assignment: Embedding Playground](./assignments/w01-a2-embedding-playground.md)

---

## Lesson 1.5 — Pre-training & Loss Functions

### Sub-topics
- Cross-Entropy Loss (Conceptual)
- Dataset Composition (Common Crawl, Books, Code)
- Training vs Inference Cost
- Chinchilla Scaling
- "Trained on X Tokens" — What It Means

### Key Concepts

**Cross-Entropy Loss.** The loss function used in LLM pre-training measures how well the model's predicted probability distribution matches the actual next token. For each position, the model outputs a probability for every token in the vocabulary (e.g., 32K probabilities). Cross-entropy loss is -log(p_correct), where p_correct is the probability the model assigned to the actual next token. If the model is confident and correct (p=0.95), loss is low (-log(0.95) ≈ 0.05). If the model assigned low probability to the correct token (p=0.01), loss is high (-log(0.01) ≈ 4.6). The model is trained to minimize this loss averaged across all positions and all training examples. You do not need to understand the calculus — what matters is the intuition: the model is rewarded for assigning high probability to the correct next token.

**Dataset Composition.** What goes into training data defines what comes out. GPT-3 was trained on a mix: 60% filtered Common Crawl (web text), 16% WebText2 (high-quality web), 16% books, 8% Wikipedia. Llama included code (GitHub) and scientific papers (ArXiv). The composition directly affects capabilities: including code makes models better at coding and structured reasoning; including math papers improves mathematical ability. Data quality matters enormously — filtering, deduplication, and careful curation of training data often matters more than raw scale. This is a key competitive differentiator between model providers.

**Training vs Inference Cost.** Pre-training a frontier model is staggeringly expensive — Llama 2 70B required ~1.7 million GPU hours. But this cost is amortized across billions of inference calls. A single inference call (processing a prompt and generating a response) is comparatively cheap. The ratio is roughly 1000:1 or more. This economic structure means: (1) training is done by large labs with massive compute budgets; (2) inference optimization is where most engineering effort goes; (3) fine-tuning is much cheaper than pre-training (typically 100-1000x less compute); (4) the "build vs. buy" decision for most companies is clearly "buy the model, optimize the inference."

**"Trained on X Tokens."** When we say "Llama 3 8B was trained on 15 trillion tokens," this means the model processed 15T tokens during training — each token was seen exactly once (modern practice avoids repeating data). This is not the amount of raw text; it is the tokenized count. 15T tokens is roughly 11 trillion words or about 75 million books. The model's parameters (8B) compress the patterns from these 15T tokens into a much smaller representation. The ratio of training tokens to parameters is a key quality indicator — Chinchilla suggests ~20 tokens per parameter, but recent models often go far beyond this.

### Interview Questions

**Q1: What is cross-entropy loss in the context of LLM training?**
**A:** Cross-entropy loss measures the difference between the model's predicted probability distribution and the actual next token. It is computed as -log(p) where p is the probability assigned to the correct token. Lower loss means the model is better at predicting the training data. The model minimizes this loss across all token positions in the training corpus. Perplexity (2^loss or e^loss) is the more commonly reported metric — it roughly represents "how many tokens the model is confused between."

**Q2: Why does training data composition matter more than just training data size?**
**A:** Data composition directly determines model capabilities. Including code improves structured reasoning and coding. Including scientific papers improves technical knowledge. Low-quality or duplicated data wastes training compute and can introduce biases. Llama 3's improvements over Llama 2 came significantly from better data curation, not just more data. In practice, data filtering, deduplication, and quality scoring are some of the most impactful engineering decisions in model development.

**Q3: A model has 7B parameters and was trained on 1T tokens. Is this well-trained by Chinchilla standards?**
**A:** Chinchilla suggests roughly 20 tokens per parameter, so a 7B model ideally needs ~140B tokens. At 1T tokens (about 143x the parameter count), this model is trained well beyond the Chinchilla-optimal ratio. Modern models deliberately overtrain relative to Chinchilla because the additional compute during training reduces the per-query compute needed at inference — a smaller but longer-trained model is cheaper to serve than a larger Chinchilla-optimal model at equivalent quality.

**Q4: What is the approximate cost relationship between training and inference for an LLM?**
**A:** Training a frontier model costs tens to hundreds of millions of dollars in compute but happens once. Inference costs are per-request but vastly cheaper individually. The training cost is amortized across potentially billions of inference calls. This asymmetry is why most companies should use existing models via API rather than training from scratch, and why inference optimization (quantization, batching, caching) has massive economic impact.

---

## Lesson 1.6 — Alignment: RLHF, SFT, DPO

### Sub-topics
- Base Model vs Instruct Model
- Supervised Fine-Tuning (SFT) Pipeline
- RLHF Reward Modeling
- DPO (Direct Preference Optimization)
- Constitutional AI
- Safety vs Capability Tradeoff

### Key Concepts

**Base Model vs Instruct Model.** A base model (like GPT-3 base or Llama base) is the raw product of pre-training. It is excellent at continuing text — give it a news article prefix and it will write a plausible continuation. But it is terrible at following instructions. Ask it "What is the capital of France?" and it might continue with "What is the capital of Germany? What is the capital of Spain?" because in its training data, questions are often followed by more questions. An instruct model has gone through additional alignment training to follow user instructions, refuse harmful requests, and produce helpful responses. The transformation from base to instruct model is what makes ChatGPT feel "smart" compared to raw GPT-3.

**Supervised Fine-Tuning (SFT).** The first alignment step. Human annotators write thousands of high-quality (prompt, ideal_response) pairs. The model is fine-tuned on these examples using the same next-token prediction objective. This teaches the model the format of helpful responses — how to follow instructions, structure answers, and adopt the right tone. SFT is relatively simple and inexpensive compared to RLHF. Many open-source models (Alpaca, Vicuna) achieved surprisingly good instruction-following with SFT alone on small datasets (52K examples for Alpaca). The quality of SFT data matters enormously — a few thousand expert-written examples often outperform millions of low-quality ones.

**RLHF Reward Modeling.** Reinforcement Learning from Human Feedback goes beyond SFT. The process: (1) Generate multiple responses to the same prompt. (2) Human annotators rank the responses from best to worst. (3) Train a separate "reward model" to predict human preferences — given a prompt and response, it outputs a scalar score. (4) Use reinforcement learning (typically PPO — Proximal Policy Optimization) to fine-tune the LLM to maximize the reward model's score. RLHF is what made ChatGPT feel dramatically better than instruction-tuned GPT-3. It teaches subtle qualities: helpfulness, harmlessness, honesty — things hard to capture in SFT demonstrations alone.

**DPO (Direct Preference Optimization).** DPO (Rafailov et al., 2023) simplifies RLHF by eliminating the separate reward model and RL training loop. Instead, it directly optimizes the language model on preference pairs: given (prompt, preferred_response, rejected_response), adjust the model to increase the probability of the preferred response relative to the rejected one. DPO is mathematically equivalent to a specific form of RLHF but is far simpler to implement and more stable to train. It has become the dominant alignment technique in open-source models. For engineers, DPO means alignment is now accessible — you do not need RL expertise or massive compute.

**Constitutional AI and Safety.** Anthropic's Constitutional AI approach uses a set of principles (a "constitution") to guide model behavior. Instead of relying entirely on human annotators, the model critiques its own outputs against these principles and generates improved versions. This is more scalable than pure human annotation and makes the safety rules explicit and auditable. The safety vs. capability tradeoff is real: heavy safety training can make models refuse legitimate requests ("I can't help with that") or be overly cautious. Finding the right balance is an active challenge — too safe and the model is useless; too capable and it becomes dangerous.

### Interview Questions

**Q1: What is the difference between a base model and an instruct model?**
**A:** A base model is trained purely on next-token prediction and excels at text continuation but cannot follow instructions reliably. An instruct model has undergone additional alignment training (SFT, RLHF, or DPO) to follow user instructions, produce helpful structured responses, and refuse harmful requests. The same base model (e.g., Llama 3 base) underlies the instruct variant — the difference is purely in the post-training alignment stage.

**Q2: Explain the RLHF pipeline. What are its components?**
**A:** RLHF has four stages: (1) SFT — fine-tune the base model on demonstration data to get a good starting policy. (2) Reward model training — collect human rankings of multiple model responses to the same prompts, train a model to predict human preferences. (3) RL fine-tuning — use PPO to optimize the language model to maximize the reward model's score. (4) Iterate — repeat data collection and training. The reward model acts as a proxy for human judgment, enabling the model to optimize for qualities like helpfulness and safety that are hard to specify as a simple loss function.

**Q3: How does DPO differ from RLHF, and why has it become popular?**
**A:** DPO eliminates the separate reward model and RL training loop. It directly optimizes the LLM on preference pairs (chosen vs. rejected responses), treating the language model itself as an implicit reward model. This is simpler to implement, more stable to train, requires less compute, and is mathematically equivalent to a specific RLHF objective. Its simplicity and effectiveness have made it the dominant alignment method in open-source models.

**Q4: What is the "alignment tax" and why does it matter?**
**A:** The alignment tax refers to the capability reduction that comes from safety training. An aligned model may refuse legitimate requests, hedge excessively, or perform worse on certain benchmarks compared to the base model. For engineers, this matters because: over-aligned models frustrate users; under-aligned models produce harmful content. The goal is to minimize the alignment tax while maintaining safety. Techniques like Constitutional AI and DPO have reduced the tax compared to early RLHF approaches.

---

## Lesson 1.7 — Inference & Sampling

### Sub-topics
- Greedy Decoding
- Temperature
- Top-p (Nucleus Sampling)
- Top-k
- Beam Search
- Seed Parameter
- KV-Cache

### Key Concepts

**Greedy Decoding.** The simplest strategy: always pick the token with the highest probability. This produces deterministic, repetitive output. It is useful when you want a single "best" answer (e.g., classification tasks, structured extraction) but produces boring, predictable text for open-ended generation. Greedy decoding often gets stuck in loops because the most probable next token keeps being the same kind of token.

**Temperature.** Temperature controls the randomness of the probability distribution before sampling. The logits (raw model outputs) are divided by the temperature value before applying softmax. Temperature=1.0 uses the model's learned distribution as-is. Temperature<1.0 (e.g., 0.2) sharpens the distribution — high-probability tokens become even more likely, producing focused, deterministic output. Temperature>1.0 (e.g., 1.5) flattens the distribution — lower-probability tokens get a boost, producing more creative, diverse, sometimes incoherent output. For production systems: use 0.0-0.3 for factual/structured tasks (RAG, extraction, code); 0.7-1.0 for creative tasks (writing, brainstorming).

**Top-p (Nucleus Sampling).** Top-p dynamically selects the smallest set of tokens whose cumulative probability exceeds p. If top_p=0.9, the model considers only the tokens in the top 90% of the probability mass and renormalizes among them. This adaptively adjusts the number of candidates — when the model is confident (one token has 95% probability), only 1-2 tokens are considered; when uncertain, many tokens are considered. Top-p is generally preferred over top-k because it adapts to the model's confidence at each step rather than using a fixed cutoff.

**Top-k.** Top-k restricts sampling to the k most probable tokens. If k=50, only the top 50 tokens are candidates regardless of their probability distribution. The limitation: when the model is very confident, k=50 still includes many irrelevant tokens; when the model is uncertain, k=50 might exclude reasonable options. This inflexibility is why top-p is usually preferred, though some APIs support both (they are applied sequentially: first top-k filters, then top-p filters the remainder).

**Beam Search.** Beam search maintains multiple candidate sequences (beams) simultaneously, expanding the most promising ones at each step. With beam_width=5, the model tracks the 5 highest-probability partial sequences. It is primarily used for translation and summarization where finding the globally optimal sequence matters. It is rarely used for general LLM chat because it produces generic, high-probability text that lacks diversity. Most production LLM applications use nucleus sampling instead.

**Seed Parameter.** Setting a seed makes sampling deterministic — the same prompt with the same seed produces the same output. This is critical for reproducibility in testing, debugging, and evaluation. Without a seed, running the same prompt twice produces different outputs (at temperature>0), making it impossible to systematically compare prompt variations or debug issues.

**KV-Cache.** During autoregressive generation, each new token requires attending to all previous tokens. Without caching, this means recomputing the Key and Value vectors for all previous tokens at every step — O(n²) total computation for a sequence of length n. The KV-cache stores the K and V vectors from all previous positions so they are computed only once. This reduces generation from O(n²) to O(n) at the cost of memory. KV-cache size scales linearly with sequence length, batch size, and model size, and is often the memory bottleneck in production serving. Techniques like Multi-Query Attention (MQA) and Grouped-Query Attention (GQA) reduce KV-cache size by sharing Key/Value heads.

### Interview Questions

**Q1: Explain the difference between temperature, top-p, and top-k. When would you use each?**
**A:** Temperature scales the logit distribution (lower = more deterministic, higher = more random). Top-k restricts sampling to the k most probable tokens. Top-p dynamically selects the smallest token set covering p probability mass. In practice: use low temperature (0.0-0.3) for factual tasks, higher (0.7-1.0) for creative tasks. Top-p is preferred over top-k because it adapts to model confidence. A common production setting: temperature=0.7, top_p=0.95. For structured extraction, temperature=0.0 (greedy).

**Q2: What is the KV-cache and why is it important for inference performance?**
**A:** The KV-cache stores previously computed Key and Value vectors so they are not recomputed at each generation step. Without it, generating token n requires O(n) attention computation at each step, totaling O(n²) for the full sequence. With KV-cache, each step only computes attention for the new token against cached K/V vectors, reducing total compute to O(n). The tradeoff is memory: KV-cache grows linearly with sequence length and is often the bottleneck in serving long-context requests.

**Q3: Why would you set a seed parameter when calling an LLM API?**
**A:** Seeds ensure deterministic outputs for the same input, enabling: reproducible testing and evaluation, systematic A/B comparison of prompts, debugging specific failure cases, consistent behavior in automated pipelines. Without a seed, temperature>0 introduces randomness, making results non-reproducible. Note that seed determinism is best-effort in some APIs — infrastructure changes can break reproducibility.

**Q4: When is greedy decoding appropriate vs. nucleus sampling?**
**A:** Greedy decoding (temperature=0) is best for tasks with clear correct answers: classification, structured data extraction, code generation where you want the most likely completion. Nucleus sampling (top-p) is better for open-ended generation where diversity matters: creative writing, brainstorming, conversation. Using greedy decoding for creative tasks produces repetitive, generic text; using high-temperature sampling for factual extraction introduces unnecessary errors.

---

## Lesson 1.8 — Context Windows & Positional Encoding

### Sub-topics
- Why Position Matters
- Sinusoidal Encoding
- RoPE (Rotary Positional Embedding)
- ALiBi
- FlashAttention
- Sliding Window Attention
- "Lost in the Middle" Problem
- Context Extension Techniques

### Key Concepts

**Why Position Matters.** The self-attention mechanism is permutation-invariant — without positional information, "the cat sat on the mat" and "mat the on sat cat the" would produce identical representations. Positional encoding injects position information so the model knows token order. This is one of the most active research areas because the choice of positional encoding directly determines how well the model handles long sequences and whether the context window can be extended after training.

**Sinusoidal Encoding.** The original Transformer used fixed sinusoidal functions: PE(pos, 2i) = sin(pos / 10000^(2i/d_model)) and PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model)). These are added to token embeddings and provide a unique position signal at each dimension. The advantage: they are computed (not learned) and theoretically generalize to any sequence length. The disadvantage: in practice, they do not extrapolate well beyond training lengths. They are mostly of historical importance now.

**RoPE (Rotary Positional Embedding).** RoPE (Su et al., 2021) encodes position by rotating the query and key vectors in pairs of dimensions. The rotation angle depends on position, so the dot product between q and k naturally encodes their relative distance. RoPE has become the dominant positional encoding in modern LLMs (Llama, Mistral, Qwen). Its key advantage: it encodes relative position through rotation, which is more natural than additive encoding. It also supports context window extension through techniques like YaRN (Yet another RoPE extensioN) that adjust the rotation frequencies to handle longer sequences than seen during training.

**ALiBi (Attention with Linear Biases).** ALiBi adds a linear bias to attention scores based on the distance between tokens — closer tokens get a boost, distant tokens get a penalty. It requires no learned parameters and has shown good extrapolation to longer sequences than seen during training. It is simpler than RoPE but used less frequently in the latest models.

**FlashAttention.** FlashAttention is not a positional encoding but an IO-aware attention implementation that dramatically reduces memory usage and improves speed. Standard attention materializes the full n×n attention matrix in GPU memory. FlashAttention computes attention in blocks, never materializing the full matrix. This reduces memory from O(n²) to O(n) and provides 2-4x speedup through better GPU memory hierarchy utilization. FlashAttention v2 further improves this. It is now the standard attention implementation in most production models and enables longer context windows that would be impossible with naive attention.

**"Lost in the Middle" Problem.** Research (Liu et al., 2023) showed that LLMs perform worse when relevant information is in the middle of a long context compared to the beginning or end. Models tend to attend more strongly to the first and last portions of the input. This has critical implications for RAG system design: place the most important retrieved documents at the beginning or end of the context, not in the middle. It also suggests that simply increasing context windows does not proportionally increase the model's ability to use all that context.

**Context Extension Techniques.** Several techniques extend a model's effective context beyond its training length: (1) YaRN adjusts RoPE frequencies for longer contexts; (2) Sliding window attention (used in Mistral) limits attention to a local window, reducing O(n²) to O(n·w) where w is the window size; (3) Sparse attention patterns attend to selected positions rather than all; (4) Ring attention distributes long sequences across multiple GPUs. These techniques enable models trained on 4K context to function at 32K or 128K, though performance typically degrades somewhat compared to models natively trained at longer lengths.

### Interview Questions

**Q1: What is the "lost in the middle" problem, and how does it affect RAG system design?**
**A:** LLMs exhibit a U-shaped attention pattern — they attend more strongly to information at the beginning and end of the context, with weaker attention to the middle. In RAG systems, this means placing the most relevant retrieved documents at the start or end of the context, not buried in the middle. Some systems reverse-sort by relevance (least relevant first, most relevant last) or use a "sandwich" approach (important context at both ends). This is also an argument for keeping retrieved context concise rather than dumping maximum context.

**Q2: How does RoPE encode positional information, and why is it preferred over sinusoidal encoding?**
**A:** RoPE rotates query and key vectors by an angle proportional to their position. The dot product between rotated q and k vectors naturally depends on their relative position (the rotation angles subtract). Unlike sinusoidal encoding (which adds position to embeddings), RoPE integrates position directly into the attention computation through rotation. This encodes relative position more naturally, supports context extension through frequency adjustment (YaRN), and has shown better performance on long-context tasks.

**Q3: What is FlashAttention and why is it important?**
**A:** FlashAttention is an IO-aware implementation of attention that avoids materializing the full n×n attention matrix in GPU HBM. It computes attention in tiles/blocks using on-chip SRAM, reducing memory from O(n²) to O(n) and providing 2-4x speedup. This is critical because it enables: longer context windows without OOM errors, higher throughput in production serving, and training on longer sequences. It does not change the mathematical result — it produces identical outputs to standard attention, just far more efficiently.

**Q4: Explain sliding window attention and its tradeoff.**
**A:** Sliding window attention restricts each token to attending only to the nearest w tokens (e.g., w=4096). This reduces attention cost from O(n²) to O(n·w), making it linear in sequence length. The tradeoff: the model cannot directly attend to information more than w tokens away in a single layer, though information propagates through multiple layers (each layer shifts the window). Mistral uses this approach. It works well for many tasks but may struggle when the answer requires directly connecting information from very distant positions.

---

## Week 1 Summary Checklist

After completing this week, you should be able to:

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

**Next:** [Week 2 — Python for AI Engineering](./week-02-python-for-ai.md)
