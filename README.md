# Dejai²

**Dejai²** is a general math & physics API for operator-based computation, tool orchestration, and retrieval-augmented problem solving.
It targets pedagogy (solid state, materials) and modular research workflows.

> *Name origin:* *Dejai* is Ilocano for “that.” Squared → **that²** ($x^2$, $\\psi^2$, $r^2$).

## Goals
- Deterministic agent loop with function calling
- Safe tool execution (calc, sandboxed Python)
- RAG over Markdown/Quarto notes
- Cheap hosting; clear observability

## Repo map (planned)
- `apps/api/` — FastAPI service
- `agent/` — core loop, tools, rag, safety, config
- `notes/` — (to link with Obsidian; see ADR-0002 later)
- `data/` — FAISS index files (ignored in Git)
- `docs/adr/` — decision records

## License
TBD (MIT/Apache-2.0 recommended).
