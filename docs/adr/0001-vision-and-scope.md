# ADR 0001 — Vision & Scope for $\mathrm{dejai^2}$

## Status
Proposed

## Context
We need an always-on assistant that uses a hosted LLM (no GPU ops), runs safe tools, and retrieves from our notes. It must be cheap to host and easy to test.

## Decision
- Build a FastAPI service that orchestrates a hosted LLM via function calling.
- Maintain a tool registry with JSON schemas and strict validation.
- Use FAISS for Retrieval v1 (offline embeddings, online search).
- Defer self-hosting of model weights; focus on low-ops deployment first.

## Consequences
+ Minimal infra cost and complexity
+ Clear boundaries (LLM, tools, RAG, safety)
− Vendor dependency for inference
− Requires embedding pipeline maintenance

## Milestones
1) Repo + docs
2) Core `/v1/chat` (no tools)
3) Tool registry (calc, py_eval)
4) RAG v1 + Obsidian link
5) Safety & observability
6) Cheap hosting & CI/CD