# Week 13: Fine-Tuning & Advanced Topics

> **Month 4 -- Fine-Tuning, Multimodal, Portfolio & Job Hunt**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 12](../month-3/week-12-agentic-capstone.md) | Next: [Week 14](./week-14-multimodal-portfolio.md)

---

## Overview

This week covers when and how to fine-tune LLMs, with a practical focus on QLoRA using Unsloth. You will learn the decision framework for fine-tuning vs RAG vs prompting, get hands-on with parameter-efficient fine-tuning, and master structured output generation with Instructor and Pydantic AI. The emphasis is on practical application and cost analysis, not ML theory.

---

## Lesson 1: When to Fine-Tune vs RAG vs Prompt

**Sub-topics:**
- The decision framework: task type, data availability, budget, latency requirements
- Prompting strengths: zero setup, fast iteration, works for most tasks
- RAG strengths: domain knowledge, freshness, auditability via citations
- Fine-tuning strengths: style/format consistency, latency (no retrieval), smaller model capability
- Combining approaches (fine-tuned model + RAG)
- Cost comparison across approaches

**Key Concepts:**

This is the most common GenAI interview question: "When would you fine-tune vs use RAG vs improve prompting?" The decision framework: Start with prompting -- it is free to iterate and works for most tasks. If the model needs domain knowledge it was not trained on, add RAG. If the model needs a consistent output style/format that prompting cannot achieve, or you need to distill expensive model behavior into a cheaper model, consider fine-tuning.

Fine-tuning shines in specific scenarios: enforcing a strict output format across thousands of calls (cheaper than including format instructions in every prompt), teaching domain-specific terminology or reasoning patterns, reducing latency by eliminating the retrieval step, and distilling (training a small model to mimic a large model's behavior for a specific task). Fine-tuning does NOT help when: the model needs up-to-date information (use RAG), the task varies widely (use prompting), or you have fewer than 100 quality examples.

**Interview Questions:**

1. *Walk me through your decision framework for fine-tuning vs RAG vs prompting.*
   Start with prompting -- iterate on prompt design with few-shot examples. If the model needs external knowledge, add RAG. If output format consistency is critical across many calls, or you need to reduce cost by using a smaller model for a specific task, fine-tune. Often the best solution combines approaches: a fine-tuned model that also uses RAG for knowledge-grounding.

2. *Give an example where fine-tuning is better than RAG.*
   A customer support bot that must always respond in a specific tone, structure, and format (greeting, acknowledgment, solution, follow-up). Prompting can approximate this but varies. Fine-tuning on 500 examples of ideal responses makes the format consistent, reduces prompt length (no format instructions needed), and allows using a smaller, cheaper model.

3. *When does fine-tuning NOT make sense?*
   When you have fewer than 100 quality examples, when the information changes frequently (RAG handles freshness better), when the task is too diverse to capture in training data, or when prompt engineering achieves acceptable results (fine-tuning has upfront cost and maintenance burden).

---

## Lesson 2: Fine-Tuning Fundamentals

**Sub-topics:**
- What changes in the model during fine-tuning (weight updates)
- Full fine-tuning vs parameter-efficient fine-tuning (PEFT)
- LoRA: Low-Rank Adaptation (how it works, why it is efficient)
- QLoRA: Quantized LoRA (4-bit quantization + LoRA)
- Adapter merging and inference
- Overfitting risks and mitigation

**Key Concepts:**

Full fine-tuning updates all model parameters, requiring enormous compute and memory. LoRA freezes the pretrained weights and adds small trainable "adapter" matrices at each layer. Instead of updating a 7B-parameter matrix, LoRA trains two small matrices (rank 8-64) whose product approximates the weight update. This reduces trainable parameters by 100x while achieving similar quality for task-specific fine-tuning.

QLoRA goes further: it quantizes the frozen base model to 4-bit precision (reducing memory by 4x) while training the LoRA adapters in full precision. This means you can fine-tune a 7B model on a single consumer GPU (16GB VRAM) or even for free on Google Colab. After training, the adapter can be merged into the base model for inference or kept separate for hot-swapping different fine-tuned behaviors.

**Interview Questions:**

1. *Explain how LoRA reduces the cost of fine-tuning.*
   LoRA freezes all pretrained weights and injects small trainable matrices (rank 8-64) at each transformer layer. Instead of updating billions of parameters, you train millions -- reducing memory, compute, and time by 100x. The adapter matrices are small enough to store and swap, enabling multiple fine-tunes on the same base model.

2. *What does the "Q" in QLoRA add?*
   QLoRA quantizes the frozen base model to 4-bit precision, reducing memory usage by 4x. The LoRA adapter layers still train in full precision. This combination means you can fine-tune a 7B model on a 16GB GPU, making fine-tuning accessible without expensive hardware.

---

## Lesson 3: Hands-On with Unsloth

**Sub-topics:**
- Why Unsloth (2x faster training, 60% less memory, free)
- Setting up Unsloth with Google Colab
- Loading a base model (Llama 3, Mistral, Gemma)
- Configuring LoRA parameters (rank, alpha, target modules)
- Training loop and monitoring loss
- Saving and exporting the fine-tuned model
- Uploading to Hugging Face Hub

**Key Concepts:**

Unsloth is the recommended tool for fine-tuning because it is free, fast, and simple. It provides optimized kernels that make training 2x faster and use 60% less memory than standard Hugging Face training. The workflow: load a base model from Hugging Face, configure LoRA parameters (rank=16 and alpha=16 is a good starting point), prepare your dataset, train with the SFTTrainer, and export.

The practical workflow in Colab: install unsloth, load a 7B model in 4-bit quantization, apply LoRA adapters, train on your dataset for 1-3 epochs (usually sufficient to avoid overfitting), evaluate on a held-out test set, merge the adapter into the base model, and push to Hugging Face Hub. The entire process takes 20-60 minutes on a free Colab T4 GPU.

**Interview Questions:**

1. *What is your practical workflow for fine-tuning a model?*
   Prepare a high-quality dataset (instruction-input-output format, 200-1000 examples). Load a base model with Unsloth in 4-bit quantization. Apply QLoRA with rank=16. Train for 1-3 epochs monitoring loss. Evaluate on a held-out test set. Compare against the base model with prompting. If improved, merge adapters and deploy. Total wall time: under 1 hour on free Colab.

---

## Lesson 4: Dataset Preparation

**Sub-topics:**
- Instruction format (system, user, assistant turns)
- Dataset quality > quantity (200 excellent > 5000 mediocre)
- Data cleaning and deduplication
- Synthetic data generation (using a stronger model to create training data)
- Dataset splits: train/validation/test
- ChatML and other conversation formats
- Common dataset mistakes and how to avoid them

**Key Concepts:**

Dataset quality is the single biggest factor in fine-tuning success. Two hundred carefully curated, diverse, high-quality examples consistently outperform five thousand auto-generated mediocre ones. Each example should represent the exact input-output behavior you want the model to learn: realistic inputs, ideal outputs, consistent format.

Format your data as instruction-following conversations: a system message defining the role, a user message with the input, and an assistant message with the ideal output. Ensure diversity -- cover edge cases, different input lengths, various subtopics. Split into train (80%), validation (10%), test (10%). Use the validation set to detect overfitting during training (validation loss starts increasing). Evaluate on the test set only once, after training is complete.

**Interview Questions:**

1. *How do you prepare a dataset for fine-tuning?*
   Curate 200-1000 high-quality examples in instruction format. Ensure diversity across subtopics, edge cases, and input variations. Clean and deduplicate. Split 80/10/10 for train/val/test. Validate format consistency. Use a stronger model to generate initial examples, then manually review and refine. Quality matters far more than quantity.

2. *How do you generate synthetic training data?*
   Use a strong model (GPT-4 or Claude) to generate initial examples based on detailed prompts describing the desired behavior. Then manually review every example, fix errors, improve quality, and remove duplicates. The synthetic data is a starting point, not the final dataset -- human curation is essential.

---

## Lesson 5: Evaluating Fine-Tuned Models

**Sub-topics:**
- Evaluation metrics: task-specific accuracy, perplexity, human preference
- A/B comparison: fine-tuned vs base model vs prompted model
- LLM-as-judge for fine-tuned model evaluation
- Regression testing: does fine-tuning hurt general capability?
- Benchmark suites (MMLU, HellaSwag) for general capability checks

**Key Concepts:**

Evaluation must answer three questions: (1) Does the fine-tuned model perform the target task better than the base model with prompting? (2) Did fine-tuning hurt the model's general capabilities? (3) Is the improvement worth the cost of maintaining a fine-tuned model?

For task-specific evaluation, use the same metrics you would use for any model: accuracy, F1, or LLM-as-judge on your test set. Run the identical evaluation on three configurations: base model with zero-shot prompt, base model with your best few-shot prompt, and fine-tuned model. If the fine-tuned model does not meaningfully beat the prompted base model, fine-tuning was not worth it. For general capability, run a small subset of standard benchmarks (MMLU, HellaSwag) to check for catastrophic forgetting.

**Interview Questions:**

1. *How do you evaluate whether fine-tuning was worth it?*
   Compare three configurations on the same test set: zero-shot prompting, best few-shot prompting, and fine-tuned model. If the fine-tuned model does not meaningfully outperform the prompted version, the ongoing cost of maintaining the fine-tuned model is not justified. Also check for capability regression on general benchmarks.

---

## Lesson 6: Instructor + Pydantic AI for Structured Outputs

**Sub-topics:**
- The structured output problem (LLMs return strings, you need objects)
- Instructor library: patching LLM clients for Pydantic output
- Pydantic AI: type-safe agent framework
- Function calling vs JSON mode vs constrained generation
- Retry logic for malformed outputs
- When to use structured output vs free-text

**Key Concepts:**

Most production GenAI applications need structured output: JSON objects, typed fields, validated data. The Instructor library patches OpenAI/Anthropic clients so you can pass a Pydantic model as the response type and get back a validated Python object. Under the hood, it uses function calling or JSON mode and automatically retries if the output does not validate.

Pydantic AI takes this further as a full agent framework built on type safety. You define tools with typed parameters, the agent's output as a Pydantic model, and dependencies as typed injection. This makes your agent code type-safe end-to-end: the IDE catches errors, your tests are meaningful, and production failures from malformed data are nearly eliminated.

**Interview Questions:**

1. *How do you get structured output from an LLM reliably?*
   Use the Instructor library with Pydantic models. Define the expected output schema as a Pydantic class. Instructor patches the LLM client to use function calling or JSON mode, validates the response against the schema, and retries automatically if validation fails. This gives you typed Python objects instead of raw strings.

2. *What is the advantage of Pydantic AI over raw LangChain?*
   Type safety end-to-end: tool parameters, agent state, and output are all Pydantic models validated at runtime. This catches errors early, enables IDE autocomplete, and makes testing straightforward. LangChain uses more dynamic typing which can lead to runtime type errors in production.

---

## Assignment: Fine-Tune and Compare

**Objective:** Fine-tune a small model on a specific task and compare performance against prompting.

**Requirements:**
- Choose a specific task (e.g., classifying support tickets, generating product descriptions, converting natural language to SQL)
- Prepare a dataset of 200+ examples in instruction format
- Fine-tune a 7B model (Llama 3 or Mistral) using QLoRA via Unsloth on Colab
- Evaluate: fine-tuned model vs base model with zero-shot vs base model with few-shot
- Use LLM-as-judge for qualitative comparison
- Document cost analysis: fine-tuning cost vs API call savings over N queries
- Use Instructor/Pydantic AI for structured output in your evaluation pipeline

**Stretch goals:**
- Fine-tune on two different dataset sizes (200 vs 1000) and compare quality
- Run general capability benchmarks to check for regression
- Deploy the fine-tuned model via Hugging Face Inference Endpoints
- Build a simple A/B testing interface to compare model outputs side-by-side

---

## Summary Checklist

- [ ] Can articulate the fine-tuning vs RAG vs prompting decision framework
- [ ] Understand LoRA and QLoRA at a conceptual level (what changes, why it is efficient)
- [ ] Successfully fine-tuned a model using Unsloth on free Colab
- [ ] Prepared a high-quality dataset with proper train/val/test splits
- [ ] Evaluated fine-tuned model against prompted baseline with clear metrics
- [ ] Understand Instructor and Pydantic AI for structured outputs
- [ ] Completed cost analysis: when is fine-tuning cheaper than API calls?
- [ ] Completed assignment: fine-tuned model with comparison evaluation
- [ ] System design sketch: fine-tuning pipeline for a team (data collection, training, evaluation, deployment)
- [ ] Weekly writing: 1 post about your fine-tuning experience, results, or the decision framework
