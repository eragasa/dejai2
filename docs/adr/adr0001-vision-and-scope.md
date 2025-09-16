# ADR 0001 — Vision & Scope for $\mathrm{dejai^2}$

## Status
Proposed

## Context
We need an always-on assistant for physics teaching that:
- Retrieves from our structured notes (atomic Markdown/LaTeX)
- Runs safe tools (solvers, autograder, generator)
- Is cheap to host and easy to test
- Avoids GPU complexity

The assistant is primarily for the **instructor** (preparing notes, slides, sets, solutions). Secondary users may be students via Canvas, but not as direct LLM consumers.

## Decision
- Build a FastAPI service that orchestrates a hosted LLM via function calling.
- Maintain a tool registry with JSON schemas and strict validation.
- Use FAISS for Retrieval v1 (offline embeddings, online search).
- Defer self-hosting of model weights; focus on low-ops deployment first.

## Consequences
**Positive**
+ Minimal infra cost and complexity
+ Clear boundaries (LLM, tools, RAG, safety)
+ Enables iterative build-out with teaching workflow in mind

**Negative**
− Vendor dependency for inference
− Requires embedding pipeline maintenance
− No student-facing autonomy (must mediate via Canvas export)

## Out of Scope (for v1)
- Large-scale grading (beyond small classes)
- Student-facing chatbot access
- GPU-based training/inference
- Complex interactive simulations

## Milestones
1. Repo + docs
2. Core `/v1/chat` (no tools)
3. Tool registry (calc, py_eval)
4. RAG v1 + Obsidian link
5. Safety & observability
6. Cheap hosting & CI/CD

## See Also
- [[adr0002-units]]
- [[adr0003-numerics_architecture]]
- 
- ADR-0002 (Units Handling)
- ADR-0003 (Numerical Backend)
- ADR-0004 (Slide Engine)
