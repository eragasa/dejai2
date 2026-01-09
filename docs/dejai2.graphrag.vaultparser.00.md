Date: 2026-01-09  
Scope: GraphRAG groundwork — parse an Obsidian-style Markdown vault into a **note graph + chunk index**.  
Non-goal: this is not a “global markdown parser,” not a publishing pipeline, and not a full Obsidian clone.

---

## 1. Purpose

Build a **local, rebuildable** parser that turns a folder of Markdown notes (initially `dejai/docs/` used *as* the vault) into a structured representation suitable for:

- graph retrieval (note-to-note edges via **obsidianlinks**),
- chunk retrieval (header-bounded chunks + adjacency),
- later embedding + indexing (vector layer),
- later mutation workflows (write suggestions elsewhere).

Key principle: **parsing must be deterministic** and output must be disposable.

---

## 2. Inputs and Outputs

### 2.1 Inputs
- `vault_root/` (initially: `dejai/docs/`)
- Markdown files: `**/*.md`
- Optional: ignore patterns (e.g., `.git/`, `_site/`, `node_modules/`, `**/.obsidian/**`)

### 2.2 Outputs (disposable)
Write to a **dropbox folder** (treated as rebuildable cache):

- `notes.jsonl`  
  one line per note (metadata + extracted link targets + structural summary)
- `edges.jsonl`  
  one line per edge (source note → target note, with anchor + type)
- `chunks.jsonl`  
  one line per chunk (chunk id, note id, header path, byte offsets, text)
- `errors.jsonl`  
  non-fatal parse issues and normalization warnings
- `manifest.json`  
  run configuration + vault hash + versions + counts

Optional later:
- `links_unresolved.jsonl` (targets that didn’t resolve to a note)
- `assets.jsonl` (images/PDF refs if you decide to track them)

---

## 3. Definitions

### 3.1 Note
A **note** is one Markdown file.  
Identity is file-path-based plus a stable hash.

### 3.2 Obsidianlink
An **obsidianlink** is an internal link of the form:

- `[[note]]`
- `[[note|alias]]`
- `[[note#heading]]`
- `[[note#heading|alias]]`
- `[[note#^blockid]]` (block references)
- `[[#heading]]` (in-note heading)
- `[[^blockid]]` (in-note block)

We are calling them *obsidianlinks* to keep semantics explicit: **note-to-note links inside the vault**.

### 3.3 Edge
An **edge** is a directed relationship extracted from content:

- `links_to` — explicit obsidianlink
- `embeds` — `![[...]]` (embed)
- `mentions` — (optional later) plain-text mentions / tags, not links

For v0: implement `links_to` and `embeds`.

### 3.4 Chunk
A **chunk** is a retrieval unit created from a note:
- header-bounded by Markdown headings `#..######`
- code blocks treated as atomic segments inside a chunk
- fallback to windowed chunks when a section is too long

---

## 4. Parser Architecture

### 4.1 Pipeline
1. **File discovery**
2. **Read text + basic normalization**
3. **Extract obsidianlinks + embeds**
4. **Chunking**
5. **Resolve link targets to note ids**
6. **Emit notes/edges/chunks + manifest**
7. **Log parse warnings**

### 4.2 Core modules (suggested)
- `VaultScanner` — enumerate `.md` files, ignore filters
- `NoteLoader` — read content, compute hashes, track mtime/size
- `ObsidianLinkExtractor` — find + normalize obsidianlinks + embeds
- `Chunker` — header-bounded chunking + adjacency metadata
- `Resolver` — map link target strings → canonical note ids (best-effort)
- `Emitter` — write JSONL outputs + manifest

---

## 5. Normalization Rules (keep conservative)

### 5.1 Text normalization
- Normalize newlines to `\n`
- Do **not** rewrite Markdown
- Do **not** strip whitespace globally (preserve offsets if you record them)

### 5.2 Path normalization
- Treat vault paths as POSIX-style in outputs
- Canonical note id: relative path from `vault_root`

### 5.3 Link target normalization (best-effort)
Given `[[target#anchor|alias]]`:
- `target_raw`: literal string before `#` (may be empty for in-note)
- `anchor_raw`: heading or `^blockid` (optional)
- `alias_raw`: display alias (optional)

Normalize:
- trim surrounding whitespace
- preserve case for display, but create `target_key` for matching:
  - lowercased
  - spaces normalized
  - optional: replace `_` with space (configurable)
- keep `anchor_raw` unchanged; later you can normalize headings.

Important: do not “get clever.” Favor traceability.

---

## 6. Link Resolution Strategy

Resolution is inherently messy in Obsidian. Do it in tiers:

1. **Exact path match**
   - If link looks like `folder/note`, match `folder/note.md`

2. **Basename match (unique)**
   - `[[note]]` matches any `note.md` by basename if unique

3. **Title match (optional later)**
   - Only if you maintain frontmatter `title:` or first heading.

4. **Unresolved**
   - Keep edge with `target_note_id = null`
   - Emit to `links_unresolved.jsonl` (optional)

Resolution outputs should preserve:
- `source_note_id`
- `target_note_id` (nullable)
- `target_text` (original)
- `anchor` (optional)
- `edge_type` (`links_to` / `embeds`)
- `span` (optional byte offsets) for provenance/debug

---

## 7. Chunking Rules

### 7.1 Header-bounded chunking
- Parse headings `^(#{1,6})\s+(.+)$`
- Each heading starts a section; chunk spans until next heading of same or higher level.
- Store `header_path`: e.g. `["2. Stylized Facts Across Domains", "2.3 Engineering and computer systems"]`

### 7.2 Code block handling
- Treat fenced code blocks as atomic segments:
  - included in chunk text
  - optionally separately recorded as `chunk_type="code"` fragments later
- Do not parse code content.

### 7.3 Chunk size controls
Configurable thresholds:
- `max_chars_per_chunk` (e.g., 4k–12k chars)
- If a header section exceeds max:
  - keep header metadata
  - split using a sliding window with overlap
  - mark `chunk_split=true` and store `split_index`

### 7.4 Adjacency
Emit adjacency metadata:
- `prev_chunk_id` / `next_chunk_id`
- `sibling_chunks` within same note (optional)

This enables neighborhood expansion without graph traversal.

---

## 8. Output Record Shapes (conceptual)

### 8.1 Note record (`notes.jsonl`)
- `note_id` (relative path)
- `path`
- `mtime`
- `size_bytes`
- `sha256` (content hash)
- `title_guess` (basename or first H1)
- `num_links`
- `num_chunks`
- `frontmatter_present` (bool)
- `tags` (optional later)

### 8.2 Edge record (`edges.jsonl`)
- `edge_id` (hash of fields)
- `source_note_id`
- `target_note_id` (nullable)
- `target_text` (raw)
- `anchor` (nullable)
- `alias` (nullable)
- `edge_type` (`links_to` / `embeds`)
- `span_start`, `span_end` (optional)

### 8.3 Chunk record (`chunks.jsonl`)
- `chunk_id` (hash: note_id + offsets + header path + split index)
- `note_id`
- `header_path`
- `level` (heading level)
- `start_offset`, `end_offset` (optional)
- `text`
- `prev_chunk_id`, `next_chunk_id` (optional)

### 8.4 Errors (`errors.jsonl`)
- `note_id`
- `severity` (`warn`/`error`)
- `kind` (e.g., `read_failed`, `bad_utf8`, `unclosed_code_fence`, `link_parse`)
- `message`
- `context` (optional small excerpt)

---

## 9. Configuration

Minimum config file (YAML/JSON) or CLI args:

- `vault_root`
- `output_root`
- `ignore_globs[]`
- `max_chars_per_chunk`
- `chunk_overlap_chars`
- `resolve_basename_links` (bool)
- `casefold_targets` (bool)
- `emit_offsets` (bool)

---

## 10. Failure Modes and Policy

### 10.1 Must not crash the run
- File read errors → emit `errors.jsonl`, skip note
- Bad UTF-8 → decode with replacement, emit warning
- Unbalanced fences → still chunk; emit warning

### 10.2 Determinism
Given the same vault state and config:
- outputs must be identical (modulo timestamps in manifest)

### 10.3 Traceability
Never silently “fix” content.  
Prefer: record raw + record normalized + record unresolved.

---

## 11. Testing Strategy (minimal but real)

### 11.1 Unit tests
- obsidianlink parsing cases:
  - `[[a]]`, `[[a|b]]`, `[[a#h]]`, `[[a#h|b]]`, `[[#h]]`, `[[^x]]`, `[[a#^x]]`, `![[a]]`
- heading parsing + header_path
- chunk splitting logic

### 11.2 Golden fixtures
Create a tiny fixture vault:
- a few notes with collisions (`note.md` in two folders)
- ambiguous links
- long sections
- code fences with `[[...]]` inside (should still count as links or not? decide!)
  - v0 suggestion: **do not extract links from code fences** (configurable)

### 11.3 Integration test
Run parser → validate:
- counts
- that every emitted chunk references an existing note_id
- that resolved edges’ targets exist

---

## 12. Open Decisions (explicit)

- Should link extraction ignore code blocks? (default yes)
- Should link extraction ignore YAML frontmatter? (default yes)
- Do we treat Markdown links `[text](url)` as edges? (default no)
- How aggressive should basename resolution be in the presence of collisions? (default: only if unique)
- Do we canonicalize headings for `#anchor` resolution now or later? (suggest: later)

---

## 13. Initial Implementation Reflecting Your Workflow

- **Vault root**: `dejai/docs/` (used as the Obsidian vault)
- **Output root**: a Dropbox folder (disposable cache)
- Parser should run fast enough for frequent rebuilds; no background daemon required.
- First milestone is correctness + determinism, not optimization.

---

## 14. TODO
- [ ] [[dejai2.dev.graphrag.vaultparser.01|Implement file discovery + ignore rules]]
- [ ] [[dejai2.dev.graphrag.vault-parser.02|Implement obsidianlink + embed extractor]]
- [ ] [[dejai2.dev.graphrag.vault-parser.03|Implement header-bounded chunker + overflow splitting]]
- [ ] [[dejai2.dev.graphrag.vault-parser.04|Implement link resolver (path + unique basename)]]
- [ ] [[dejai2.dev.graphrag.vault-parser.05|Define JSONL record shapes + write emitter + manifest]]
- [ ] [[dejai2.dev.graphrag.vault-parser.06|Create fixture vault + golden tests]]
- [ ] [[dejai2.dev.graphrag.vault-parser.07|Decide policy: links inside code blocks/frontmatter]]
- [ ] [[dejai2.dev.graphrag.vault-parser.08|Add diagnostics: unresolved links report + collision report]]
- [ ] [[dejai2.dev.graphrag.vault-parser.09|Add incremental rebuild option (hash/mtime based)]]
