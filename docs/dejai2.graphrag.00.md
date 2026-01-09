**Last updated:** 2026-01-09  
**Applies to:** dejai2

**Purpose.**  
This note defines a **local, graph-oriented RAG architecture** for the `dejai2` knowledge base in which the **Obsidian vault is mutable** and participates in a **closed feedback loop** with retrieval and synthesis.

The vault is not a passive corpus. It is an **active, evolving graph** whose structure may be read, annotated, and partially rewritten by downstream tools under explicit guardrails.

This is a **working specification**. Precision and scope will be tightened iteratively.


## [[dejai2.graphrag.01|1. Motivation and Scope]]  

### [[dejai2.graphrag.01.01|1.1 Stylized Facts]]

As the vault grows, manual curation fails. Links become inconsistent, canonical notes drift, and the graph becomes unreadable as a *read interface*. Writing remains effective; reading does not.

### [dejai2.graphrag.01.02]] Problem statement

Given these stylized facts, the core problem is **not** that Obsidian fails as a writing or browsing tool.

The problem is that:

> Obsidian does not provide a mechanism to **maintain, interrogate, or evolve the note graph as a graph** under growth, semantic drift, and long time horizons.

Specifically, there is no layer that can:

- reconstruct the effective graph state,
    
- retrieve reliably across multiple hops,
    
- track provenance and conflict,
    
- or propose controlled, reversible improvements to graph structure.
    

---

### [[dejai2.graphrag.01.03]] Design objective

The objective of GraphRAG in `dejai2` is therefore:

> to introduce a **separate, machine-operated graph maintenance and retrieval layer** that operates _alongside_ Obsidian, without replacing it as the human interface.

This layer must:

- tolerate heterogeneity and drift,
    
- operate on existing obsidianlinks,
    
- support retrieval and traversal at scale,
    
- and allow **optional, human-approved feedback** into the vault.
    

---

### [[dejai2.graphrag.01.04]] Scope and non-scope

**In scope:**

- graph reconstruction from obsidianlinks,
    
- hybrid retrieval (semantic + structural),
    
- provenance-aware synthesis,
    
- optional, reversible vault annotation.
    

**Out of scope:**

- enforcing semantic purity,
    
- replacing Obsidian’s UI,
    
- automatic truth arbitration,
    
- ontology induction.
    

GraphRAG is a **maintenance and retrieval system**, not a knowledge authority.

---

### [[dejai2.graphrag.01.05]] Constraints

The system must be:

- local-only,
    
- low-cost,
    
- rebuildable,
    
- tolerant of messiness,
    
- human-controlled.
    

These constraints are architectural, not optional.

### [[dejai2.graphrag.01.02]] Why RAG instead of manual curation
RAG shifts effort from *organization-time* to *query-time*. Structure is inferred when needed, rather than enforced continuously. This tolerates redundancy, contradiction, and exploratory noise.

### [[dejai2.graphrag.01.03]] Why vector-only RAG is insufficient
Vector similarity answers “what is semantically similar” but cannot answer:
- what is connected,
- what supports what,
- where ideas came from.
This leads to shallow answers and lost provenance.

### [[dejai2.graphrag.01.04]] Role of graph structure in reasoning and provenance
Graph structure enables:
- multi-hop reasoning,
- adjacency-based context,
- explicit provenance tracing.
Vectors seed; graphs explain.

### [[dejai2.graphrag.01.05]] Constraints: local-only, cheap, rebuildable
- Ollama-based LLMs and embeddings only  
- No external APIs  
- All indices disposable and rebuildable  
- Suitable for capital-constrained environments  

---

## [[dejai2.graphrag.02]] — Vault as a Mutable Knowledge Graph

### [[dejai2.graphrag.02.01]] Obsidian vault as a live property graph
The vault is treated simultaneously as:
- a property graph,
- a transaction log of ideas,
- a target for incremental structure injection.

### [[dejai2.graphrag.02.02]] Notes as first-class mutable nodes
Each markdown file is a node whose content may evolve. Mutability is a feature, not a defect.

### [[dejai2.graphrag.02.03]] Wikilinks as explicit semantic edges
`[[wikilinks]]` define explicit, human-authored edges. These are privileged over inferred semantics.

### [[dejai2.graphrag.02.04]] Backlinks and derived adjacency
Backlinks and adjacency are derived graph features used for traversal, not authorial intent.

### [[dejai2.graphrag.02.05]] Machine annotations vs human prose
Machine-generated content must never overwrite human prose. It must be explicitly marked, additive, and attributable.

### [[dejai2.graphrag.02.06]] Reversibility and auditability requirements
All machine actions must be:
- visible,
- undoable,
- attributable to a specific operation.

---

## [[dejai2.graphrag.03]] — Chunking and Representational Units

### [[dejai2.graphrag.03.01]] Why chunks are retrieval units, not notes
Notes are too coarse. Chunks provide localized context suitable for retrieval and citation.

### [[dejai2.graphrag.03.02]] Header-bounded chunking
Where possible, chunks align with markdown headers to preserve semantic locality.

### [[dejai2.graphrag.03.03]] Sliding-window fallback strategy
When structure is absent:
- ~400–700 token windows  
- ~20–30% overlap  

Approximation is acceptable.

### [[dejai2.graphrag.03.04]] Code blocks as atomic units
Code blocks are never split. They are treated as indivisible semantic units.

### [[dejai2.graphrag.03.05]] Chunk adjacency and neighborhood windows
Adjacent chunks (±1 or ±2) are used during expansion to restore local continuity.

### [[dejai2.graphrag.03.06]] Ephemeral vs persisted representations
Chunks are ephemeral retrieval units. Notes remain the persisted, authoritative objects.

---

## [[dejai2.graphrag.04]] — Vector Layer (Semantic Seeding)

### [[dejai2.graphrag.04.01]] Role of embeddings in GraphRAG
Embeddings are used to *seed* retrieval, not to determine final context.

### [[dejai2.graphrag.04.02]] Embedding models (Ollama, llama ecosystem)
Baseline:
- `nomic-embed-text` via Ollama  
Model choice is interchangeable.

### [[dejai2.graphrag.04.03]] Chunk-to-vector mapping
Each chunk maps to exactly one vector.

### [[dejai2.graphrag.04.04]] Similarity search as seed generation
Top-k similarity provides candidate entry points into the graph.

### [[dejai2.graphrag.04.05]] Overfetching and recall bias
Overfetching is preferred. Precision is recovered downstream.

### [[dejai2.graphrag.04.06]] Limits of semantic similarity
Semantic similarity cannot capture structure, causality, or argument flow.

---

## [[dejai2.graphrag.05]] — Graph Layer (Structural Expansion)

### [[dejai2.graphrag.05.01]] Graph schema: nodes and edges
Nodes:
- Notes  
Edges:
- `links_to`
- `suggested_link`
- `annotates`
- `derived_from`

### [[dejai2.graphrag.05.02]] Note-level traversal vs chunk-level retrieval
Retrieval operates on chunks; expansion operates on notes.

### [[dejai2.graphrag.05.03]] One-hop and two-hop expansion policies
Traversal depth is intentionally shallow (≤ 2 hops).

### [[dejai2.graphrag.05.04]] Forward links vs backlinks
Both are usable. Neither is privileged by default.

### [[dejai2.graphrag.05.05]] Weighting `.00` notes as hubs (non-authoritative)
`.00` notes may be weighted as high-degree hubs but carry no intrinsic truth.

### [[dejai2.graphrag.05.06]] Containment to prevent graph explosion
Strict limits are imposed to prevent unbounded expansion.

---

## [[dejai2.graphrag.06]] — Hybrid Retrieval Algorithm

### [[dejai2.graphrag.06.01]] Semantic seeding step
Vector similarity produces initial chunk candidates.

### [[dejai2.graphrag.06.02]] Parent note aggregation
Parent notes of seed chunks define expansion roots.

### [[dejai2.graphrag.06.03]] Graph expansion rules
Include:
- adjacent chunks,
- linked notes,
- optional backlinks.

### [[dejai2.graphrag.06.04]] Reranking expanded candidates
Expanded candidates are re-scored against the query.

### [[dejai2.graphrag.06.05]] Context assembly and truncation
Context is assembled with explicit chunk IDs and paths.

### [[dejai2.graphrag.06.06]] Failure modes and fallback behavior
If support is insufficient, the system must say so.

---

## [[dejai2.graphrag.07]] — LLM Interaction Policy

### [[dejai2.graphrag.07.01]] LLM as synthesizer, not authority
The LLM summarizes; it does not decide truth.

### [[dejai2.graphrag.07.02]] Context-bounded prompting
The LLM must operate strictly within retrieved context.

### [[dejai2.graphrag.07.03]] Citation and provenance requirements
All claims must cite chunk IDs or paths.

### [[dejai2.graphrag.07.04]] Handling contradictions explicitly
Conflicts are reported, not resolved.

### [[dejai2.graphrag.07.05]] Admitting insufficiency
Unsupported queries must return “not found in the vault.”

### [[dejai2.graphrag.07.06]] Model interchangeability (llama, mistral, qwen)
Models are swappable without architectural change.

---

## [[dejai2.graphrag.08]] — Vault Mutation and Feedback Loop

### [[dejai2.graphrag.08.01]] Retrieval → mutation loop
Retrieval may optionally propose vault mutations.

### [[dejai2.graphrag.08.02]] Machine-generated annotations (format)
All machine content lives under explicit headers, e.g.:

```markdown
## machine
- generated_by: dejai2.graphrag
- date: YYYY-MM-DD
- operation: annotate | suggest-links | summarize | cluster
```

### [[dejai2.graphrag.08.03]] Suggested links and confidence scoring

Inferred links are suggestions, not edits.

### [[dejai2.graphrag.08.04]] Evidence packs and context capture

Retrieved context may be appended as evidence packs.

### [[dejai2.graphrag.08.05]] Human approval and rejection paths

All mutations are opt-in and reviewable.

### [[dejai2.graphrag.08.06]] Avoiding silent drift

Silent rewrites are forbidden.

---

## [[dejai2.graphrag.09]] — Role of Canonical (.00) Notes

### [[dejai2.graphrag.09.01]] `.00` notes as interfaces, not truth

They define interfaces, not correctness.

### [[dejai2.graphrag.09.02]] Hub behavior and graph degree

Their influence is empirical, not declarative.

### [[dejai2.graphrag.09.03]] Retrieval frequency as authority signal

Usage determines relevance.

### [[dejai2.graphrag.09.04]] Machine augmentation of `.00` notes

Summaries and link suggestions are allowed.

### [[dejai2.graphrag.09.05]] Explicit non-privileging of canon

No note is immune to contradiction.

### [[dejai2.graphrag.09.06]] Eventual stabilization criteria

Stability emerges from repeated use, not designation.

---

## [[dejai2.graphrag.10]] - Non-Goals and Deferred Work

- No ontologies
- No automatic truth arbitration
- No autonomous rewriting
- No premature optimization
- No replacement of human judgment
---
## [[dejai2.graphrag.11]] - Implementation Roadmap (Deferred)
- Index builder (graph + vectors)
- Query engine
- Diagnostics and introspection
- Graph visualization
- Promotion-from-retrieval heuristics
---

## [[dejai2.graphrag.12]] — Status and Governance

### [[dejai2.graphrag.12.01]] Draft stability and revision policy

This is an evolving spec.

### [[dejai2.graphrag.12.02]] Human-in-the-loop authority

Humans retain final control.

### [[dejai2.graphrag.12.03]] Rebuild and rollback philosophy

All indices are disposable.

### [[dejai2.graphrag.12.04]] Criteria for freezing interfaces

Interfaces freeze only when they stop changing under use.

---

