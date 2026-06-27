# Week 14: Multimodal AI + Portfolio Polish

> **Month 4 -- Fine-Tuning, Multimodal, Portfolio & Job Hunt**
> [Back to Roadmap](../ROADMAP.md) | Previous: [Week 13](./week-13-fine-tuning-advanced.md) | Next: [Week 15](./week-15-interview-prep.md)

---

## Overview

This week has two goals: add multimodal capabilities to your skill set and polish your portfolio projects to interview-ready quality. You will work with vision models, multimodal RAG, and audio APIs, then spend significant time ensuring your three capstone projects are clean, documented, and demonstrable.

---

## Lesson 1: Vision Models

**Sub-topics:**
- GPT-4V (GPT-4 with vision): capabilities and API usage
- Claude Vision: image understanding, document analysis
- Gemini multimodal: native multimodal architecture
- Open-source vision models (LLaVA, InternVL)
- Image input formats: base64, URLs, file uploads
- Token costs for image inputs (resolution-dependent)

**Key Concepts:**

Vision models accept images alongside text, enabling a new class of applications. GPT-4V and Claude Vision are the production standards: they can describe images, extract text from screenshots, analyze charts and diagrams, compare visual elements, and answer questions about image content. They are NOT image generators -- they understand images, they do not create them.

Practical usage: encode images as base64 or pass URLs in the API message. Be aware of token costs -- a high-resolution image can consume 1000+ tokens. For production, resize images to the minimum resolution that preserves the information you need. Claude Vision excels at document and chart understanding; GPT-4V is stronger at general scene description. Gemini is natively multimodal (not a bolted-on vision encoder) and handles long-form visual content well.

**Interview Questions:**

1. *How do you choose between vision models for a production application?*
   Consider: task fit (Claude excels at documents/charts, GPT-4V at general scenes, Gemini at long multimodal context), cost per image (resolution-dependent token counts), latency requirements, and API reliability. For document understanding, Claude Vision. For diverse image types, GPT-4V. For mixed modality workflows with long context, Gemini.

2. *What are the cost implications of adding vision to an AI application?*
   Each image adds 500-2000 tokens depending on resolution. A high-throughput application processing thousands of images per day will see significant cost increases. Optimize by: downscaling images to minimum useful resolution, caching results for identical images, and using vision only when text extraction or OCR cannot solve the problem.

---

## Lesson 2: Image Understanding Use Cases

**Sub-topics:**
- Document understanding (invoices, receipts, forms, contracts)
- Chart and graph analysis (extracting data from visualizations)
- Screenshot analysis (UI testing, monitoring)
- Diagram understanding (architecture diagrams, flowcharts)
- Visual question answering (product images, medical images, real estate)
- Combining vision with structured output (extract data into Pydantic models)

**Key Concepts:**

The highest-value vision use cases in enterprise are document understanding and chart analysis. Instead of building complex OCR + layout analysis pipelines, you can send a document image to a vision model and get structured data back. An invoice image becomes a Pydantic model with vendor, amount, date, and line items -- using Instructor, the vision model's output is validated automatically.

Chart analysis is another strong use case: send a bar chart or line graph image and ask the model to extract the underlying data, describe trends, or compare against benchmarks. This enables applications that "read" dashboards, analyze competitor reports, or monitor visual KPIs. The key limitation: vision models can hallucinate numbers, so always validate extracted data against known constraints.

**Interview Questions:**

1. *How would you build a document processing system with vision models?*
   Accept document images (photos, scans, PDFs rendered as images). Send to a vision model with a structured output schema (Instructor + Pydantic). Extract fields: vendor, amounts, dates, line items. Validate against business rules (amounts must be positive, dates must be valid). Store structured data. For high-volume, compare cost vs traditional OCR pipelines.

---

## Lesson 3: Multimodal RAG

**Sub-topics:**
- The multimodal RAG challenge (images + text in the same corpus)
- Approach 1: Generate text descriptions of images, embed the descriptions
- Approach 2: Use multimodal embedding models (CLIP, Jina CLIP)
- Approach 3: Store images separately, retrieve with vision model at query time
- Handling mixed documents (PDFs with charts and text)
- Evaluation: how to measure multimodal retrieval quality

**Key Concepts:**

Standard RAG works with text. Multimodal RAG extends this to corpora containing images, charts, and diagrams alongside text. The simplest approach: use a vision model to generate text descriptions of each image, then embed and retrieve those descriptions like any other text. This works surprisingly well and requires no changes to your existing RAG pipeline.

For richer retrieval, use multimodal embedding models like CLIP or Jina CLIP v2 that embed both images and text into the same vector space. This allows querying with text and retrieving relevant images (or vice versa). The tradeoff: multimodal embeddings are less precise for text-text matching than dedicated text models, so a hybrid approach (text embeddings for text, multimodal for images) often works best.

**Interview Questions:**

1. *How do you add image retrieval to an existing RAG system?*
   Simplest: generate text descriptions of images using a vision model, embed the descriptions, and add them to the existing text index. More advanced: use a multimodal embedding model (CLIP) to embed images directly into the same vector space as text. Hybrid: maintain separate text and image indexes, query both, and fuse results.

2. *What are the tradeoffs between describing images vs embedding them directly?*
   Descriptions are simpler (no pipeline changes) but lossy -- the description may miss details the original image captures. Direct embedding preserves visual information but requires a multimodal embedding model and may reduce text retrieval quality if using a single index. A hybrid approach (separate indexes, fused results) is often the best tradeoff.

---

## Lesson 4: Audio and Speech APIs

**Sub-topics:**
- Speech-to-text: OpenAI Whisper API, Deepgram
- Text-to-speech: OpenAI TTS, ElevenLabs
- Voice agents: real-time speech-to-speech patterns
- Transcription + summarization pipelines
- Audio in multimodal context (podcast analysis, meeting notes)
- Cost and latency considerations for audio processing

**Key Concepts:**

Audio capabilities round out the multimodal stack. OpenAI's Whisper API provides production-quality speech-to-text at low cost. The pattern: transcribe audio with Whisper, then process the text with your existing LLM pipelines (summarize, extract action items, Q&A). This enables applications like meeting summarizers, podcast analyzers, and voice-controlled agents.

Text-to-speech (TTS) enables voice responses from your agents. OpenAI's TTS API and ElevenLabs produce natural-sounding speech with multiple voice options. For voice agents (real-time speech-to-speech), the pipeline is: streaming transcription, LLM processing, streaming TTS. Latency is the critical challenge -- users expect sub-second response times in voice interactions.

**Interview Questions:**

1. *How would you build a meeting summarizer with audio input?*
   Accept audio files or live audio streams. Transcribe with Whisper API (handles multiple speakers with diarization). Send the transcript to an LLM with a summarization prompt that extracts: key decisions, action items with owners, open questions. Use structured output (Pydantic model) for the summary. Store for search and retrieval.

---

## Lesson 5: Portfolio Polish

**Sub-topics:**
- README as a design document (not just setup instructions)
- Architecture diagrams (Excalidraw, Mermaid)
- Demo quality: live URL, screenshots, GIF/video walkthrough
- Code quality: consistent style, type hints, docstrings, tests
- Consistent styling across all 3 capstone projects
- GitHub profile optimization (pinned repos, profile README, contribution graph)

**Key Concepts:**

Your portfolio is your resume. Each capstone project should have a README that reads like a design document: problem statement, architecture diagram, key design decisions, evaluation results, and a live demo link. A hiring manager spends 30 seconds on your repo -- the README must immediately communicate competence and thoughtfulness.

Clean up your code: consistent formatting (ruff), type hints everywhere, docstrings on public functions, and at least basic tests. Remove dead code, TODO comments, and debug print statements. Ensure all three capstones have consistent README structure, similar architecture diagram style, and professional presentation. Pin your best repos on your GitHub profile.

**Interview Questions:**

1. *What makes a GenAI portfolio project stand out?*
   A live demo URL (not just code), a README that reads like a design doc (architecture diagram, design decisions, evaluation results), clean and well-typed code, comprehensive DECISIONS.md showing engineering judgment, and honest evaluation results including known limitations. The meta-signal is: this person ships production-quality work with thoughtful engineering decisions.

---

## Lesson 6: Vercel AI SDK for Multimodal React Apps

**Sub-topics:**
- Extending useChat for multimodal input (image upload + text)
- Displaying multimodal responses (text + images + citations)
- File upload handling and image preprocessing
- Streaming multimodal content
- Building a polished chat interface with image support

**Key Concepts:**

Your React/TypeScript skills become a differentiator when building multimodal frontends. The Vercel AI SDK's `useChat` hook can be extended to handle image uploads: encode the image as base64, include it in the message, and send to your FastAPI backend which forwards it to a vision model. On the response side, render text, images, and citations in a rich chat interface.

A polished multimodal chat UI includes: drag-and-drop image upload, image thumbnails in the message thread, streaming text responses, expandable source citations, and responsive design. This is where your frontend expertise creates a portfolio piece that stands out from the sea of CLI-only projects.

**Interview Questions:**

1. *How do you handle image input in a chat application built with Vercel AI SDK?*
   Add a file input or drag-and-drop zone for image upload. Encode the image as base64 on the client side. Include it in the chat message payload alongside the text query. The backend extracts the image, sends both text and image to the vision model API, and streams the text response back. Display the uploaded image as a thumbnail in the message thread.

---

## Assignment: Add Multimodal + Polish Capstones

**Objective:** Add multimodal capability to one capstone project and polish all three for portfolio.

**Requirements:**
- Choose one capstone (RAG or agent) and add image understanding:
  - Option A: Add image Q&A to your RAG system (upload a chart, ask questions about it)
  - Option B: Add a vision tool to your agent (analyze screenshots, read documents)
- Use Instructor + Pydantic for structured output from the vision model
- Polish all 3 capstone projects:
  - README as design doc with architecture diagram
  - Clean code: consistent formatting, type hints, docstrings
  - Live demo URLs working
  - DECISIONS.md and EVALS.md complete
  - Consistent styling across all projects

**Stretch goals:**
- Build a multimodal RAG system with both text and image retrieval
- Add voice input/output to one project (Whisper + TTS)
- Create a 2-minute demo video for each capstone
- Write a blog post about your multimodal implementation

---

## Summary Checklist

- [ ] Can use GPT-4V, Claude Vision, or Gemini for image understanding tasks
- [ ] Understand multimodal RAG approaches (descriptions vs multimodal embeddings)
- [ ] Know audio APIs (Whisper, TTS) and their use cases
- [ ] Added multimodal capability to at least one capstone project
- [ ] All 3 capstones have polished READMEs with architecture diagrams
- [ ] All 3 capstones have clean, typed, well-documented code
- [ ] All 3 capstones have live demo URLs
- [ ] DECISIONS.md and EVALS.md complete on all projects
- [ ] GitHub profile optimized: pinned repos, profile README
- [ ] System design sketch: multimodal document processing pipeline at enterprise scale
- [ ] Weekly writing: 1 post about multimodal AI or portfolio preparation
