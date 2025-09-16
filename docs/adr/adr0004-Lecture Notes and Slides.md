# ADR 0004 — Lecture Notes & Slides in $\mathrm{dejai^2}$

## Status
Proposed

## Context
Lectures require two artifacts:
- **Lecture notes** (detailed, reference quality, distributed to students).
- **Lecture slides** (concise, visual, presented in class).

Both should:
- Share a common source (atomic Markdown/LaTeX notes + problem bank).
- Support math typesetting, code execution, and visualizations.
- Export to **PDF** (for Canvas) and **HTML** (for interactive presentation).
- Allow embedding of solver code and plots (students can rerun in Colab/Jupyter).

### Options considered
- **Quarto/Jupyter**
  - Pros: Executable documents (code + math + plots in one place); reproducible; integrates directly with solvers; easy to publish to both HTML and PDF.
  - Cons: Slightly heavier toolchain; less polished design than dedicated slide tools; students may need guidance on rerunning notebooks.
- **Marp (Markdown → Reveal.js/PDF)**
  - Pros: Lightweight Markdown → HTML/PDF; modern look; simple pipeline.
  - Cons: Static — cannot execute code or show live results; requires Node.js tooling.
- **LaTeX Beamer**
  - Pros: Professional academic style; native math support.
  - Cons: Static only; verbose; disconnected from solver code.
- **Keynote/PowerPoint**
  - Pros: Polished visuals.
  - Cons: Manual, not reproducible, disconnected from repo pipeline.

## Decision
- **Primary:**  
  - Use **Quarto/Jupyter notebooks** as the canonical source for lecture notes and slides.  
  - Author in `.qmd` or `.ipynb` with embedded LaTeX math and Python code.  
  - Export lecture notes as **PDF handouts** (detailed, with derivations and worked solutions).  
  - Export slides as **Quarto reveal.js decks** (interactive HTML, PDF for Canvas).  
- **Secondary:**  
  - Permit Marp or Beamer exports if needed for external talks, but not the main teaching format.  
  - Support Colab runtime for student reruns (see ADR-0005).

## Consequences
**Positive**
+ Single source of truth: same notebook generates both notes and slides.  
+ Fully executable: math + code + plots are reproducible.  
+ Easy integration with Colab for students.  
+ Dual exports cover both live presentation and LMS handouts.  

**Negative**
− Quarto/Jupyter toolchain heavier than Marp or Beamer.  
− Less typographic/design flexibility than dedicated slide tools.  
− Some students may find HTML slides unfamiliar vs. static PDFs.  

## Out of Scope
- Highly customized CSS/JS slide theming.  
- Embedding copyrighted textbook text directly.  
- Using Keynote/PowerPoint as part of the official pipeline.

## Milestones
1. Install Quarto CLI and ensure Jupyter kernel setup.  
2. Create base templates: `lectures/template.qmd` for notes + slides.  
3. Script to assemble lectures from note IDs and clicker items into a `.qmd` file.  
4. Export to PDF (notes) and reveal.js HTML/PDF (slides).  
5. Validate Colab compatibility for student labs.

## See Also
- ADR-0001 (Vision & Scope)  
- ADR-0002 (Units Handling)  
- ADR-0003 (Numerical Backend)  
- ADR-0005 (Student Compute Environment)
