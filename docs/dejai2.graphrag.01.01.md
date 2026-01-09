# Stylized Facts
Each stylized fact is expressed as:
- `key`:
- `title`:
- `statement` — observable property of large Obsidian vaults
- `description` — clarification of how the property manifests
- `claim` — a falsifiable proposition derived from the observation

#### SFF v 0.1 SPEC
- A fact is delimited by:
    - `@fact.begin`
    - `@fact.end`
- Inside a fact: `key: value` lines only.
- Multiline values use a `|` marker and end at the next key or `@fact.end`.
- Keys are fixed: `key`, `title`, `statement`, `description`, `claim`.
- No indentation semantics. No markdown semantics.


SFF v1 — STYLIZED FACTS (copy/paste block)

@facts.begin  
version: 1  
domain: dejai2.graphrag  
date: 2026-01-09  
@facts.end

@fact.begin  
key: SF-1  
title: Obsidian remains an effective human interface  
statement: |  
Obsidian remains effective for human authoring, reading, and local navigation as the vault grows.  
description: |  
Users can continue to write, edit, browse, and locally restructure notes with low friction. Markdown, obsidianlinks, headings, and local conventions scale well for individual cognitive workflows.  
claim: |  
Replacing Obsidian’s user interface alone, without introducing an external graph maintenance mechanism, will not improve graph-level retrieval accuracy or provenance tracing.  
@fact.end

@fact.begin  
key: SF-2  
title: The note graph evolves without explicit control  
statement: |  
The note-to-note graph evolves implicitly through local authoring actions rather than deliberate graph management.  
description: |  
Each obsidianlink is created in isolation, with no system-level representation of global graph structure or its evolution over time.  
claim: |  
In the absence of explicit graph maintenance, measurable graph properties (e.g., degree distribution, hub concentration, connected components) will drift monotonically as the vault grows.  
@fact.end

@fact.begin  
key: SF-3  
title: Obsidianlinks encode heterogeneous semantics  
statement: |  
A single obsidianlink syntax is used to encode multiple, incompatible relationship types.  
description: |  
The same link may represent dependency, example, reminder, TODO, conceptual proximity, or historical reference, depending on context.  
claim: |  
Treating obsidianlinks as semantically uniform edges will reduce retrieval precision compared to methods that incorporate structural or contextual differentiation.  
@fact.end

@fact.begin  
key: SF-4  
title: Link semantics drift over time  
statement: |  
The meaning of obsidianlinks changes as notes are edited, split, merged, or repurposed.  
description: |  
Original authorial intent is often not updated when links persist across content evolution.  
claim: |  
Older obsidianlinks will, on average, contribute less to correct retrieval outcomes than more recently created links, controlling for note activity.  
@fact.end

@fact.begin  
key: SF-5  
title: High-degree hubs emerge naturally  
statement: |  
Certain notes accumulate disproportionately many inbound or outbound obsidianlinks.  
description: |  
These notes often act as informal indices, aggregation points, or conceptual dumping grounds.  
claim: |  
Notes with higher graph degree will exhibit lower average semantic specificity than low-degree notes, as measured by retrieval entropy or topic dispersion.  
@fact.end

@fact.begin  
key: SF-6  
title: Hub semantics degrade faster than hub connectivity grows  
statement: |  
As hub notes increase in degree, their interpretability degrades faster than their connectivity improves.  
description: |  
Additional links add marginal reach but disproportionately increase ambiguity and overload.  
claim: |  
Beyond a threshold degree, additional links to a hub note will correlate negatively with retrieval usefulness.  
@fact.end

@fact.begin  
key: SF-7  
title: Local coherence does not imply global navigability  
statement: |  
Individual notes may remain internally coherent while the global graph becomes difficult to traverse meaningfully.  
description: |  
Local editing preserves note quality, but multi-hop navigation and provenance reconstruction degrade.  
claim: |  
Queries requiring multi-hop reasoning will fail at a higher rate than single-hop queries in large vaults without graph-aware retrieval.  
@fact.end

@fact.begin  
key: SF-8  
title: Graph health is not observable within Obsidian  
statement: |  
Obsidian does not expose graph-level diagnostics to the user.  
description: |  
Users cannot directly observe orphaned notes, dead ends, contradictory hubs, or structural decay.  
claim: |  
External graph diagnostics will reveal structural pathologies that are not detectable through manual browsing alone.  
@fact.end

@fact.begin  
key: SF-9  
title: Human-authored and inferred structure are conflated  
statement: |  
All visible structure in Obsidian appears equivalent regardless of origin or reliability.  
description: |  
Intentional links, legacy links, and inferred relationships are not distinguished.  
claim: |  
Separating human-authored structure from machine-inferred structure will reduce accidental corruption of authorial intent during automated augmentation.  
@fact.end

@fact.begin  
key: SF-10  
title: There is no graph maintenance loop  
statement: |  
Obsidian provides no closed loop for analyzing, correcting, and reintegrating graph structure.  
description: |  
Graph changes accumulate without systematic review, evaluation, or feedback.  
claim: |  
Introducing a graph maintenance loop will stabilize or improve retrieval performance over time relative to a static vault.  
@fact.end