dejai.docs.graphrag.architecture.20260109

# Architecure v 20260109
name: dejai.docs.graphrag.architecture.20260109
location: dejai2/docs/
generated: ChatGPT v. 5.2 / manual prompting
edited: Eugene J. Ragasa


**Purpose.**  
This document records the **initial architectural decision** for the `dejai2` GraphRAG system: **roll a thin, custom orchestration layer** rather than adopting a heavy RAG framework (e.g., LangChain). The intent is to freeze *why* this choice was made, not to finalize implementation details.

This document lives in `docs/` and is historical as well as technical.

---

## Decision Summary

**Decision:**  
Implement a **custom, minimal GraphRAG core** with direct control over parsing, retrieval, traversal, and mutation.

**Explicitly rejected as a default:**  
- LangChain-style end-to-end orchestration frameworks

**Permitted as optional utilities:**  
- Small, single-purpose libraries (FAISS, SQLite, BM25, Ollama HTTP)
- Retrieval-focused helpers where they do not dictate control flow

---

## Problem Context

The `dejai2` system requires:

- graph-first retrieval with explicit traversal rules,
- provenance-aware answers with citation and conflict reporting,
- a **mutable Obsidian vault** with additive, reversible machine annotations,
- local-only execution under capital and infrastructure constraints,
- long-term stability suitable for research and documentation.

These requirements conflict with framework-first RAG designs that prioritize speed of assembly over architectural control.

---

## Architectural Positioning

### Thin Core, Owned by dejai2

The following components are **first-class, project-owned code**:

1. Vault parsing and wikilink normalization  
2. Graph construction and traversal policy  
3. Chunking strategy and adjacency handling  
4. Hybrid retrieval logic (seed → expand → rerank)  
5. Vault mutation rules and audit boundaries  
6. Citation, provenance, and conflict reporting  

These define the epistemic behavior of the system and must remain inspectable.

---

## Accepted External Components

The system deliberately relies on **low-level, stable libraries**:

- **SQLite** — persistent graph and metadata store  
- **FAISS** — vector similarity search  
- **Ollama (HTTP API)** — local LLM and embedding execution  
- **Optional**:
  - `rank-bm25` for lexical retrieval
  - `networkx` for non-critical graph utilities

No component may implicitly mutate the vault or control retrieval flow.

---

## Rejected Frameworks (as Defaults)

### LangChain

LangChain is not adopted as a core dependency due to:

- heavy abstraction layers that obscure retrieval logic,
- frequent API and semantic churn,
- poor alignment with graph-first and mutation-aware designs,
- difficulty enforcing auditability and reversibility.

LangChain may be used for **isolated experiments**, but not as infrastructure.

### Framework Lock-In (General)

Any framework that:
- owns control flow,
- hides retrieval policy,
- or performs opaque agent actions

is incompatible with the goals of `dejai2`.

---

## Optional Middle Ground (Non-Binding)

Retrieval-focused libraries (e.g., LlamaIndex) may be evaluated **only** if:

- they do not dictate traversal or mutation logic,
- they can be cleanly isolated behind a project-defined interface,
- they reduce boilerplate without introducing epistemic opacity.

No framework is assumed to be permanent.

---

## Resulting System Shape

```text
Obsidian Vault (mutable)
        ↓
Custom Parser + Chunker
        ↓
FAISS (vectors)      SQLite (graph)
        ↓                  ↓
        └── Hybrid Retrieval (project-owned) ──┘
                          ↓
                    Ollama LLM
                          ↓
            Answer + Citations + Mutation Proposals
```
Control remains in the project, not the framework.

Design Consequences
Advantages

Full transparency of reasoning and retrieval

Stable interfaces over time

Publishable, explainable architecture

Low dependency and infrastructure cost

Vault mutations remain auditable and human-controlled

Costs

Slightly more initial code

Fewer “plug-and-play” features

Slower initial demos

These costs are accepted.

Status

Decision state: recorded

Revisability: allowed with justification

Applies to: dejai2 GraphRAG system

Audience: future maintainers, reviewers, and collaborators

TODO — Development Notes to Be Written

Each item below is intended to become a standalone devnote (implementation-facing, not architectural).

[[dejai2.graphrag.vaultparser.00]] — Markdown parsing, wikilink normalization, edge extraction

[[dejai.dev.graphrag.chunker]] — Chunking strategy, header alignment, code-block handling

[[dejai.dev.graphrag.graph-schema]] — SQLite schema for notes, edges, metadata

[[dejai.dev.graphrag.vector-index]] — FAISS index layout, rebuild policy, normalization

[[dejai.dev.graphrag.hybrid-retrieval]] — Seed → expand → rerank algorithm details

[[dejai.dev.graphrag.context-assembly]] — Context window construction and truncation rules

[[dejai.dev.graphrag.llm-interface]] — Ollama prompt contracts, citation enforcement

[[dejai.dev.graphrag.mutation-ops]] — Allowed vault mutations and formatting rules

[[dejai.dev.graphrag.audit-log]] — Provenance, reversibility, and rollback mechanics

[[dejai.dev.graphrag.diagnostics]] — Retrieval introspection, failure analysis tools

[[dejai.dev.graphrag.config]] — Minimal configuration surface and defaults