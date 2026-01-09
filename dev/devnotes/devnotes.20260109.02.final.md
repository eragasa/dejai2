# devnote — stylized facts: definition, scope, and representation
Date: 2026-01-09  
Status: ACTIVE, coherent, not frozen

## Summary

This dev cycle clarified what a *stylized fact* is, why it is useful across domains, and how it should be represented in a text-first knowledge system (Obsidian + GraphRAG context).

The work deliberately avoided premature formalization (JSON schemas, ontologies, standards) in favor of a **conceptual stabilization** step.

The result is a domain-agnostic definition, a structured outline, and a clear path toward later specialization.

---

## What Was Accomplished

### 1. Conceptual clarification

- Established a **domain-agnostic definition** of a stylized fact:
  - a deliberately simplified textual statement
  - capturing a recurring pattern in system behavior
  - asserting qualitative correctness rather than quantitative accuracy

- Distinguished stylized facts from:
  - laws
  - hypotheses
  - empirical results
  - causal explanations

- Clarified that stylized facts fix **descriptive style** rather than formal mechanism.

---

### 2. Cross-domain grounding

Documented how stylized facts are actually used in practice across domains:

- Economics / social science  
- Natural and physical sciences  
- Engineering and computer systems  
- Qualitative and interpretive fields  

Key conclusion:
- differences across domains are *evidentiary*, not conceptual
- the underlying object is the same: a stabilized qualitative description of behavior

---

### 3. Textual-first framing

Explicitly treated stylized facts as **textual artifacts**, not data objects.

Key points:
- natural language is the correct primary medium
- separation between observation and interpretation is useful but not mandatory
- revision over time is expected and legitimate

This aligns with Obsidian-style knowledge work and avoids false precision.

---

### 4. Formats before schemas

Surveyed **existing formats** before proposing any abstraction:

- narrative prose
- structured labeled text
- informal identifiers
- absence of canonical standards

This prevented schema design from imposing unintended methodological commitments.

---

### 5. Motivation for a general schema

Identified why *some* schema is still useful:

- stylized facts otherwise dissolve into prose
- difficult to reference, compare, revise, or promote
- need to be treated as identifiable artifacts

Constraints were made explicit:
- minimal structure
- text-first
- durable
- extensible

---

### 6. Conceptual schema (not formalized)

Defined the **most general form** of a stylized-fact schema in conceptual terms only:

Core components:
- Identity (stable handle)
- Descriptive content (what pattern is observed)
- Interpretive content (what is inferred or taken away)

Explicit non-requirements:
- no numbers
- no formal falsification
- no causal claims
- no universal scope

This schema is a **conceptual scaffold**, not a standard.

---

### 7. Obsidian-compatible structuring

Converted the outline into a `.md` top note:

- Root note: `[[stylizedfact.00]]`
- All sections and subsections exposed as linkable interfaces:
  - `[[stylizedfacto.XX.YY|X.Y Title]]`

This allows:
- incremental refinement
- later extraction
- GraphRAG compatibility
- promotion without rewriting

---

## What Was Explicitly Deferred

- JSON or YAML schemas
- Pydantic or dataclass finalization
- Domain-specific extensions
- Validation rules
- Tooling and automation

All of these were intentionally postponed until conceptual stability was achieved.

---

## Current State

- Concept: stable enough to use
- Representation: clear and text-first
- Scope: appropriate for Obsidian + research dev
- Risk of overfitting: low
- Risk of premature formalism: avoided

---

## Next Logical Steps (Not Yet Done)

- Decide how stylized facts live alongside other note types
- Define promotion rules (note → canonical → paper)
- Map conceptual schema to a minimal machine representation
- Test schema against real examples from multiple domains
- Integrate with GraphRAG retrieval as atomic units

---

## Meta

This work should be treated as **infrastructure**, not output.

Its value is in enabling later work to be clearer, faster, and less confused — not in being published as-is.
